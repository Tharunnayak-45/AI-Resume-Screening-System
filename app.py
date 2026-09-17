import os
import re
import time


import mysql.connector
from docx import Document
from flask import Flask, flash, redirect, render_template, request, session, url_for
from mysql.connector import Error
from PyPDF2 import PdfReader
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "ai_resume_screening_secret_key")
app.config["UPLOAD_FOLDER"] = os.path.join(app.root_path, "uploads")
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

ALLOWED_EXTENSIONS = {"pdf", "docx"}
DB_CONFIG = {
    "host": os.environ.get("DB_HOST", "localhost"),
    "user": os.environ.get("DB_USER", "root"),
    "password": os.environ.get("DB_PASSWORD", "root"),
    "database": os.environ.get("DB_NAME", "ai_resume_db"),
}

SKILL_ALIASES = {
    "Java": ["java", "core java"],
    "Python": ["python"],
    "C": ["c programming", "c language"],
    "C++": ["c++", "cpp"],
    "HTML": ["html", "html5"],
    "CSS": ["css", "css3"],
    "JavaScript": ["javascript", "js"],
    "React": ["react", "reactjs", "react.js"],
    "JSP": ["jsp", "java server pages"],
    "Servlets": ["servlet", "servlets"],
    "Flask": ["flask"],
    "Django": ["django"],
    "Spring": ["spring", "spring boot", "spring framework"],
    "SQL": ["sql"],
    "MySQL": ["mysql"],
    "PostgreSQL": ["postgresql", "postgres"],
    "Oracle": ["oracle", "oracle database"],
    "MongoDB": ["mongodb", "mongo db"],
    "JDBC": ["jdbc"],
    "Git": ["git"],
    "GitHub": ["github", "git hub"],
    "VS Code": ["vs code", "visual studio code"],
    "Apache Tomcat": ["apache tomcat", "tomcat"],
    "Machine Learning": ["machine learning", "machine-learning", "ml"],
    "NLP": ["nlp", "natural language processing"],
    "Data Structures": ["data structures", "data structure", "dsa"],
    "Algorithms": ["algorithms", "algorithm"],
    "OOP": ["oop", "object oriented programming", "object-oriented programming"],
    "DBMS": ["dbms", "database management system"],
    "Operating Systems": ["operating systems", "operating system", "os"],
    "Computer Networks": ["computer networks", "computer network", "networking", "cn"],
    "Software Testing": ["software testing", "testing", "test cases", "unit testing"],
    "Salesforce": ["salesforce", "salesforce crm"],
    "Linux": ["linux", "linux fundamentals"],
}

ACTION_VERBS = {
    "develop": ["develop", "developed", "developing", "development"],
    "build": ["build", "built", "building"],
    "create": ["create", "created", "creating"],
    "design": ["design", "designed", "designing"],
    "implement": ["implement", "implemented", "implementing"],
    "test": ["test", "tested", "testing"],
    "debug": ["debug", "debugged", "debugging"],
    "integrate": ["integrate", "integrated", "integrating"],
    "manage": ["manage", "managed", "managing"],
    "analyze": ["analyze", "analyzed", "analysing", "analyzing"],
    "optimize": ["optimize", "optimized", "optimizing"],
    "maintain": ["maintain", "maintained", "maintaining"],
    "configure": ["configure", "configured", "configuring"],
}


def get_db_connection():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            return connection
        connection.close()
    except Error as error:
        print("Database connection error:", error)
    return None


def initialize_database():
    connection = get_db_connection()
    if connection is None:
        print("Could not connect to MySQL.")
        return False
    cursor = connection.cursor()
    statements = [
        """CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            full_name VARCHAR(100) NOT NULL,
            email VARCHAR(150) NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL,
            role VARCHAR(20) NOT NULL DEFAULT 'Candidate',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""",
        """CREATE TABLE IF NOT EXISTS resumes (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            filename VARCHAR(255) NOT NULL,
            extracted_text LONGTEXT,
            skills TEXT,
            uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )""",
        """CREATE TABLE IF NOT EXISTS analysis_results (
            id INT AUTO_INCREMENT PRIMARY KEY,
            resume_id INT NOT NULL,
            resume_score INT NOT NULL,
            text_length INT NOT NULL,
            skills_count INT NOT NULL,
            detected_skills TEXT,
            suggestions TEXT,
            analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (resume_id) REFERENCES resumes(id) ON DELETE CASCADE
        )""",
        """CREATE TABLE IF NOT EXISTS job_descriptions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            job_title VARCHAR(150) NOT NULL,
            company VARCHAR(150),
            location VARCHAR(150),
            description LONGTEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )""",
        """CREATE TABLE IF NOT EXISTS ats_scores (
            id INT AUTO_INCREMENT PRIMARY KEY,
            resume_id INT NOT NULL,
            job_description_id INT,
            overall_score INT NOT NULL,
            skills_score INT DEFAULT 0,
            section_score INT DEFAULT 0,
            contact_score INT DEFAULT 0,
            length_score INT DEFAULT 0,
            action_score INT DEFAULT 0,
            quantified_score INT DEFAULT 0,
            keyword_score INT DEFAULT 0,
            keyword_match_percentage INT DEFAULT 0,
            matched_keywords TEXT,
            missing_keywords TEXT,
            detected_skills TEXT,
            action_verbs TEXT,
            quantified_results TEXT,
            suggestions TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (resume_id) REFERENCES resumes(id) ON DELETE CASCADE,
            FOREIGN KEY (job_description_id) REFERENCES job_descriptions(id) ON DELETE SET NULL
        )""",
    ]
    try:
        for statement in statements:
            cursor.execute(statement)
        connection.commit()
        print("Database tables initialized successfully.")
        return True
    except Error as error:
        connection.rollback()
        print("Database initialization error:", error)
        return False
    finally:
        cursor.close()
        connection.close()


def login_required():
    return "user_id" in session


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def normalize_text(text):
    return re.sub(r"\s+", " ", str(text or "").lower()).strip()


def split_values(value):
    if not value:
        return []
    if isinstance(value, list):
        return value
    return [item.strip() for item in re.split(r"[,|]", str(value)) if item.strip()]


def contains_term(text, term):
    text = normalize_text(text)
    term = normalize_text(term)
    if not text or not term:
        return False
    return re.search(r"(?<![a-z0-9])" + re.escape(term) + r"(?![a-z0-9])", text) is not None


def detect_skills(text):
    return sorted({
        skill for skill, aliases in SKILL_ALIASES.items()
        if any(contains_term(text, alias) for alias in aliases)
    })


def detect_action_verbs(text):
    return sorted({
        verb for verb, variations in ACTION_VERBS.items()
        if any(contains_term(text, variation) for variation in variations)
    })


def detect_quantified_results(text):
    if not text:
        return []
    patterns = [
        r"\b\d+\s*%",
        r"\b\d+\+\b",
        r"\b\d+\s+(?:modules?|pages?|projects?|users?|features?|records?|test cases?|cases?)",
        r"\b\d+\s*(?:months?|years?|days?|weeks?)",
    ]
    results = []
    for pattern in patterns:
        results.extend(re.findall(pattern, str(text), flags=re.IGNORECASE))
    return list(dict.fromkeys(results))[:10]


def extract_text_from_pdf(filepath):
    try:
        reader = PdfReader(filepath)
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    except Exception as error:
        print("PDF extraction error:", error)
        return ""


def extract_text_from_docx(filepath):
    try:
        document = Document(filepath)
        parts = [paragraph.text for paragraph in document.paragraphs if paragraph.text.strip()]
        for table in document.tables:
            for row in table.rows:
                cells = [cell.text.strip() for cell in row.cells if cell.text.strip()]
                if cells:
                    parts.append(" ".join(cells))
        return "\n".join(parts)
    except Exception as error:
        print("DOCX extraction error:", error)
        return ""


def extract_resume_text(filepath):
    extension = os.path.splitext(filepath)[1].lower()
    if extension == ".pdf":
        return extract_text_from_pdf(filepath)
    if extension == ".docx":
        return extract_text_from_docx(filepath)
    return ""


def calculate_section_score(text):
    sections = (
        "summary", "objective", "skills", "education", "experience",
        "internship", "projects", "certifications", "achievements",
    )
    normalized = normalize_text(text)
    found = sum(1 for section in sections if contains_term(normalized, section))
    return min(int((found / len(sections)) * 22), 22)


def calculate_contact_score(text):
    text = str(text or "")
    score = 0
    if re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text):
        score += 2
    if re.search(r"(?:\+91[\s-]?)?[6-9]\d{9}", text):
        score += 2
    if re.search(r"linkedin\.com", text, re.IGNORECASE):
        score += 1
    if re.search(r"github\.com", text, re.IGNORECASE):
        score += 1
    return min(score, 6)


def calculate_length_score(text):
    length = len(str(text or ""))
    if 1500 <= length <= 5000:
        return 10
    if 1000 <= length < 1500:
        return 8
    if 500 <= length < 1000:
        return 6
    if length > 5000:
        return 8
    return 4


def calculate_action_score(action_verbs):
    count = len(action_verbs)
    if count >= 10:
        return 10
    if count >= 7:
        return 8
    if count >= 4:
        return 7
    if count >= 2:
        return 5
    return 2 if count else 0


def calculate_quantified_score(results):
    count = len(results)
    if count >= 8:
        return 7
    if count >= 5:
        return 5
    if count >= 3:
        return 4
    if count >= 1:
        return 2
    return 0


def analyze_job_keywords(resume_text, job_title="", job_description=""):
    required_skills = detect_skills(f"{job_title or ''} {job_description or ''}")
    resume_skills = detect_skills(resume_text)
    if not required_skills:
        return {
            "keyword_score": 25,
            "keyword_match_percentage": 100,
            "matched_keywords": [],
            "missing_keywords": [],
        }
    matched = [skill for skill in required_skills if skill in resume_skills]
    missing = [skill for skill in required_skills if skill not in resume_skills]
    percentage = int(len(matched) / len(required_skills) * 100)
    return {
        "keyword_score": int(percentage / 100 * 25),
        "keyword_match_percentage": percentage,
        "matched_keywords": matched,
        "missing_keywords": missing,
    }


def calculate_resume_score(text):
    detected_skills = detect_skills(text)
    action_verbs = detect_action_verbs(text)
    quantified_results = detect_quantified_results(text)
    total = (
        min(20, len(detected_skills))
        + calculate_section_score(text)
        + calculate_contact_score(text)
        + calculate_length_score(text)
        + calculate_action_score(action_verbs)
        + calculate_quantified_score(quantified_results)
    )
    return {
        "resume_score": min(total, 75),
        "text_length": len(str(text or "")),
        "skills_count": len(detected_skills),
        "detected_skills": detected_skills,
        "action_verbs": action_verbs,
        "quantified_results": quantified_results,
    }


def generate_suggestions(text, detected_skills, action_verbs, quantified_results):
    suggestions = []
    if len(detected_skills) < 8:
        suggestions.append("Add more relevant technical skills.")
    if len(action_verbs) < 5:
        suggestions.append("Use stronger action verbs such as developed, implemented, designed and optimized.")
    if len(quantified_results) < 3:
        suggestions.append("Add measurable results using numbers, percentages, modules or project metrics.")
    if not re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", str(text or "")):
        suggestions.append("Add a professional email address.")
    if not re.search(r"linkedin\.com", str(text or ""), re.IGNORECASE):
        suggestions.append("Add your LinkedIn profile.")
    if not re.search(r"github\.com", str(text or ""), re.IGNORECASE):
        suggestions.append("Add your GitHub profile.")
    return suggestions or ["Your resume contains good ATS-friendly content. Continue tailoring keywords for each job description."]


@app.route("/")
def home():
    return render_template("index.html")



@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    full_name = request.form.get("full_name", "").strip()
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "").strip()
    if not full_name or not email or not password:
        flash("Please fill all fields.", "danger")
        return render_template("register.html")
    connection = get_db_connection()
    if connection is None:
        flash("Database connection failed.", "danger")
        return render_template("register.html")
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
        if cursor.fetchone():
            flash("Email already registered.", "warning")
            return render_template("register.html")
        cursor.execute(
            "INSERT INTO users (full_name, email, password, role) VALUES (%s, %s, %s, %s)",
            (full_name, email, password, "Candidate"),
        )
        connection.commit()
        flash("Registration successful. Please login.", "success")
        return redirect(url_for("login"))
    except Error as error:
        connection.rollback()
        print("Registration error:", error)
        flash("Registration failed.", "danger")
        return render_template("register.html")
    finally:
        cursor.close()
        connection.close()


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "").strip()
    connection = get_db_connection()
    if connection is None:
        flash("Database connection failed.", "danger")
        return render_template("login.html")
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        if user and user["password"] == password:
            session["user_id"] = user["id"]
            session["full_name"] = user["full_name"]
            session["email"] = user["email"]
            session["role"] = user["role"]
            return redirect(url_for("dashboard"))
        flash("Invalid email or password.", "danger")
    except Error as error:
        print("Login error:", error)
        flash("Login failed.", "danger")
    finally:
        cursor.close()
        connection.close()
    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    if not login_required():
        return redirect(url_for("login"))
    connection = get_db_connection()
    resumes = []
    jobs = []
    if connection is not None:
        cursor = connection.cursor(dictionary=True)
        try:
            cursor.execute(
                """SELECT r.id, r.filename, r.uploaded_at, ar.resume_score, ar.skills_count
                   FROM resumes r LEFT JOIN analysis_results ar ON r.id = ar.resume_id
                   WHERE r.user_id = %s ORDER BY r.uploaded_at DESC""",
                (session["user_id"],),
            )
            resumes = cursor.fetchall()
            cursor.execute(
                """SELECT id, job_title AS title, company, location, description
                   FROM job_descriptions WHERE user_id = %s ORDER BY id DESC""",
                (session["user_id"],),
            )
            jobs = cursor.fetchall()
        except Error as error:
            print("Dashboard error:", error)
        finally:
            cursor.close()
            connection.close()
    return render_template("dashboard.html", resumes=resumes, jobs=jobs)


@app.route("/upload-resume", methods=["GET", "POST"])
def upload_resume():
    if not login_required():
        return redirect(url_for("login"))
    if request.method == "GET":
        return render_template("upload_resume.html")
    uploaded_file = request.files.get("resume")
    if not uploaded_file or not uploaded_file.filename:
        flash("Please select a resume file.", "warning")
        return redirect(url_for("upload_resume"))
    if not allowed_file(uploaded_file.filename):
        flash("Only PDF and DOCX files are allowed.", "danger")
        return redirect(url_for("upload_resume"))

    filename = secure_filename(uploaded_file.filename)
    unique_filename = f"{int(time.time())}_{filename}"
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], unique_filename)
    try:
        uploaded_file.save(filepath)
        extracted_text = extract_resume_text(filepath)
        if not extracted_text.strip():
            flash("Could not extract text from the resume.", "danger")
            return redirect(url_for("upload_resume"))
        connection = get_db_connection()
        if connection is None:
            flash("Database connection failed.", "danger")
            return redirect(url_for("upload_resume"))
        cursor = connection.cursor()
        try:
            analysis = calculate_resume_score(extracted_text)
            suggestions = generate_suggestions(
                extracted_text,
                analysis["detected_skills"],
                analysis["action_verbs"],
                analysis["quantified_results"],
            )
            cursor.execute(
                "INSERT INTO resumes (user_id, filename, extracted_text, skills) VALUES (%s, %s, %s, %s)",
                (session["user_id"], unique_filename, extracted_text, ", ".join(analysis["detected_skills"])),
            )
            resume_id = cursor.lastrowid
            cursor.execute(
                """INSERT INTO analysis_results
                   (resume_id, resume_score, text_length, skills_count, detected_skills, suggestions)
                   VALUES (%s, %s, %s, %s, %s, %s)""",
                (
                    resume_id,
                    analysis["resume_score"],
                    analysis["text_length"],
                    analysis["skills_count"],
                    ", ".join(analysis["detected_skills"]),
                    " | ".join(suggestions),
                ),
            )
            connection.commit()
            session["resume_id"] = resume_id
            flash("Resume uploaded successfully.", "success")
            return redirect(url_for("analyze_resume"))
        except Error as error:
            connection.rollback()
            print("Resume upload database error:", error)
            flash("Could not save resume.", "danger")
            return redirect(url_for("upload_resume"))
        finally:
            cursor.close()
            connection.close()
    except Exception as error:
        print("Resume processing error:", error)
        flash("Error while processing resume.", "danger")
        return redirect(url_for("upload_resume"))
    finally:
        if os.path.exists(filepath) and "resume_id" not in session:
            try:
                os.remove(filepath)
            except OSError:
                pass


@app.route("/analyze-resume")
def analyze_resume():
    if not login_required():
        return redirect(url_for("login"))
    resume_id = session.get("resume_id")
    if not resume_id:
        flash("Please upload a resume first.", "warning")
        return redirect(url_for("upload_resume"))
    connection = get_db_connection()
    if connection is None:
        flash("Database connection failed.", "danger")
        return redirect(url_for("dashboard"))
    cursor = connection.cursor(dictionary=True)
    result = None
    try:
        cursor.execute(
            """SELECT r.*, ar.resume_score, ar.text_length, ar.skills_count,
                      ar.detected_skills, ar.suggestions
               FROM resumes r LEFT JOIN analysis_results ar ON r.id = ar.resume_id
               WHERE r.id = %s AND r.user_id = %s LIMIT 1""",
            (resume_id, session["user_id"]),
        )
        result = cursor.fetchone()
    except Error as error:
        print("Resume analysis database error:", error)
    finally:
        cursor.close()
        connection.close()
    if not result:
        flash("Resume analysis not found.", "danger")
        return redirect(url_for("dashboard"))
    detected_skills = split_values(result.get("detected_skills") or result.get("skills"))
    resume_score = int(result.get("resume_score") or 0)
    return render_template(
        "resume_analysis.html",
        resume=result,
        resume_score=resume_score,
        overall_score=resume_score,
        text_length=result.get("text_length", 0),
        skills_count=result.get("skills_count", len(detected_skills)),
        detected_skills=detected_skills,
        skills=detected_skills,
        suggestions=split_values(result.get("suggestions")),
        job_title="",
        company="",
        location="",
        job_description="",
        skills_score=min(20, len(detected_skills)),
        section_score=calculate_section_score(result.get("extracted_text", "")),
        contact_score=calculate_contact_score(result.get("extracted_text", "")),
        length_score=calculate_length_score(result.get("extracted_text", "")),
        action_score=calculate_action_score(detect_action_verbs(result.get("extracted_text", ""))),
        quantified_score=calculate_quantified_score(detect_quantified_results(result.get("extracted_text", ""))),
        keyword_score=0,
        keyword_match_percentage=0,
        matched_keywords=[],
        missing_keywords=[],
        action_verbs=detect_action_verbs(result.get("extracted_text", "")),
        quantified_results=detect_quantified_results(result.get("extracted_text", "")),
    )


@app.route("/jobs")
def jobs():
    if not login_required():
        return redirect(url_for("login"))
    connection = get_db_connection()
    jobs_list = []
    if connection is not None:
        cursor = connection.cursor(dictionary=True)
        try:
            cursor.execute(
                "SELECT id, job_title AS title, company, location, description FROM job_descriptions WHERE user_id = %s ORDER BY created_at DESC",
                (session["user_id"],),
            )
            jobs_list = cursor.fetchall()
        except Error as error:
            print("Jobs error:", error)
        finally:
            cursor.close()
            connection.close()
    return render_template("jobs.html", jobs=jobs_list)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/resume_analysis")
def resume_analysis_compatibility():
    return redirect(url_for("analyze_resume"))


@app.route("/resume_analysis.html")
def resume_analysis_html_compatibility():
    return redirect(url_for("analyze_resume"))


@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404


@app.errorhandler(413)
def file_too_large(error):
    flash("File is too large. Maximum size is 10 MB.", "danger")
    return redirect(url_for("upload_resume"))


if __name__ == "__main__":
    initialize_database()
    app.run(debug=True, host="127.0.0.1", port=5000)
