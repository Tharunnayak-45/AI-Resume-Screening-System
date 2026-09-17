import re


# ============================================================
# TECHNICAL SKILLS DATABASE
# ============================================================

SKILLS = [

    # --------------------------------------------------------
    # PROGRAMMING LANGUAGES
    # --------------------------------------------------------
    "Python",
    "Java",
    "C",
    "C++",
    "C#",
    "JavaScript",
    "TypeScript",
    "PHP",
    "Ruby",
    "Go",
    "Golang",
    "Kotlin",
    "Swift",
    "R",
    "Rust",
    "Dart",
    "Scala",
    "Perl",
    "MATLAB",
    "SQL",
    "PL/SQL",
    "Bash",
    "Shell Scripting",

    # --------------------------------------------------------
    # WEB DEVELOPMENT
    # --------------------------------------------------------
    "HTML",
    "HTML5",
    "CSS",
    "CSS3",
    "Bootstrap",
    "Tailwind CSS",
    "React",
    "React.js",
    "Angular",
    "AngularJS",
    "Vue.js",
    "Vue",
    "Next.js",
    "Nuxt.js",
    "Node.js",
    "Node",
    "Express.js",
    "Express",
    "jQuery",
    "AJAX",
    "JSON",
    "XML",
    "REST API",
    "RESTful API",
    "GraphQL",
    "Web Development",
    "Frontend Development",
    "Backend Development",
    "Full Stack Development",

    # --------------------------------------------------------
    # JAVA TECHNOLOGIES
    # --------------------------------------------------------
    "JSP",
    "Servlets",
    "JDBC",
    "Spring",
    "Spring Boot",
    "Spring MVC",
    "Spring Security",
    "Hibernate",
    "Maven",
    "Gradle",
    "JavaFX",
    "JPA",

    # --------------------------------------------------------
    # PYTHON TECHNOLOGIES
    # --------------------------------------------------------
    "Flask",
    "Django",
    "FastAPI",
    "Pandas",
    "NumPy",
    "Matplotlib",
    "Seaborn",
    "Tkinter",
    "PyQt",
    "BeautifulSoup",
    "Selenium",

    # --------------------------------------------------------
    # DATABASES
    # --------------------------------------------------------
    "MySQL",
    "PostgreSQL",
    "Oracle",
    "MongoDB",
    "SQLite",
    "Microsoft SQL Server",
    "SQL Server",
    "MariaDB",
    "Redis",
    "Cassandra",
    "DynamoDB",
    "Firebase",
    "Firestore",
    "Neo4j",
    "Database Management",
    "Database Design",
    "Database Testing",

    # --------------------------------------------------------
    # DATA STRUCTURES / COMPUTER SCIENCE
    # --------------------------------------------------------
    "Data Structures",
    "Algorithms",
    "Data Structures and Algorithms",
    "DSA",
    "Object Oriented Programming",
    "OOP",
    "DBMS",
    "Operating Systems",
    "Computer Networks",
    "Computer Architecture",
    "Software Engineering",
    "System Design",
    "Distributed Systems",

    # --------------------------------------------------------
    # MACHINE LEARNING / AI
    # --------------------------------------------------------
    "Machine Learning",
    "Deep Learning",
    "Artificial Intelligence",
    "AI",
    "Natural Language Processing",
    "NLP",
    "Computer Vision",
    "Generative AI",
    "Large Language Models",
    "LLM",
    "Neural Networks",
    "Artificial Neural Networks",
    "CNN",
    "Convolutional Neural Networks",
    "RNN",
    "Recurrent Neural Networks",
    "LSTM",
    "Transformers",
    "Reinforcement Learning",
    "Supervised Learning",
    "Unsupervised Learning",
    "Regression",
    "Classification",
    "Clustering",
    "Feature Engineering",
    "Data Preprocessing",
    "Model Training",
    "Model Evaluation",
    "Scikit-learn",
    "TensorFlow",
    "PyTorch",
    "Keras",
    "OpenCV",
    "NLTK",
    "SpaCy",
    "Hugging Face",

    # --------------------------------------------------------
    # DATA SCIENCE / DATA ANALYTICS
    # --------------------------------------------------------
    "Data Science",
    "Data Analysis",
    "Data Analytics",
    "Data Visualization",
    "Exploratory Data Analysis",
    "EDA",
    "Statistics",
    "Statistical Analysis",
    "Power BI",
    "Tableau",
    "Microsoft Excel",
    "Advanced Excel",
    "Apache Spark",
    "PySpark",
    "Hadoop",
    "Apache Kafka",

    # --------------------------------------------------------
    # VERSION CONTROL
    # --------------------------------------------------------
    "Git",
    "GitHub",
    "GitLab",
    "Bitbucket",
    "Version Control",
    "GitHub Actions",

    # --------------------------------------------------------
    # CLOUD TECHNOLOGIES
    # --------------------------------------------------------
    "AWS",
    "Amazon Web Services",
    "EC2",
    "S3",
    "Lambda",
    "RDS",
    "Azure",
    "Microsoft Azure",
    "Azure Functions",
    "Google Cloud",
    "Google Cloud Platform",
    "GCP",
    "Google Compute Engine",
    "Google Cloud Storage",

    # --------------------------------------------------------
    # DEVOPS
    # --------------------------------------------------------
    "Docker",
    "Kubernetes",
    "Jenkins",
    "CI/CD",
    "Continuous Integration",
    "Continuous Deployment",
    "Terraform",
    "Ansible",
    "Prometheus",
    "Grafana",
    "ArgoCD",
    "GitHub Actions",
    "DevOps",

    # --------------------------------------------------------
    # OPERATING SYSTEMS
    # --------------------------------------------------------
    "Linux",
    "Ubuntu",
    "Windows",
    "Unix",
    "CentOS",
    "Red Hat",
    "RHEL",

    # --------------------------------------------------------
    # TESTING / QA
    # --------------------------------------------------------
    "Software Testing",
    "Manual Testing",
    "Automation Testing",
    "Functional Testing",
    "Unit Testing",
    "Integration Testing",
    "System Testing",
    "Regression Testing",
    "Smoke Testing",
    "Sanity Testing",
    "Performance Testing",
    "API Testing",
    "Database Testing",
    "User Acceptance Testing",
    "UAT",
    "Test Case Design",
    "Test Case Execution",
    "Test Automation",
    "Selenium",
    "JUnit",
    "TestNG",
    "Postman",
    "JMeter",
    "Cypress",
    "Playwright",
    "Defect Tracking",
    "Bug Tracking",
    "Debugging",

    # --------------------------------------------------------
    # MOBILE DEVELOPMENT
    # --------------------------------------------------------
    "Android",
    "Android Development",
    "Android Studio",
    "Flutter",
    "React Native",
    "iOS Development",
    "SwiftUI",

    # --------------------------------------------------------
    # SALESFORCE
    # --------------------------------------------------------
    "Salesforce",
    "Salesforce CRM",
    "Apex",
    "Visualforce",
    "Lightning Web Components",
    "LWC",
    "Salesforce Flow",
    "Salesforce Administration",
    "Sales Cloud",
    "Service Cloud",
    "Marketing Cloud",

    # --------------------------------------------------------
    # SAP
    # --------------------------------------------------------
    "SAP",
    "SAP ERP",
    "SAP S/4HANA",
    "SAP ABAP",
    "SAP FICO",
    "SAP MM",
    "SAP SD",
    "SAP HANA",

    # --------------------------------------------------------
    # SERVICENOW
    # --------------------------------------------------------
    "ServiceNow",
    "ServiceNow Administration",
    "ITSM",
    "ITOM",
    "CMDB",

    # --------------------------------------------------------
    # APIS / DEVELOPMENT TOOLS
    # --------------------------------------------------------
    "API Development",
    "REST",
    "SOAP",
    "Postman",
    "Swagger",
    "OpenAPI",
    "Microservices",
    "Web Services",
    "Apache Tomcat",
    "Nginx",
    "Apache HTTP Server",

    # --------------------------------------------------------
    # IDE / DEVELOPMENT ENVIRONMENT
    # --------------------------------------------------------
    "Visual Studio Code",
    "VS Code",
    "Visual Studio",
    "Eclipse",
    "IntelliJ IDEA",
    "PyCharm",
    "Jupyter Notebook",
    "Jupyter",
    "Android Studio",

    # --------------------------------------------------------
    # SECURITY
    # --------------------------------------------------------
    "Cybersecurity",
    "Network Security",
    "Information Security",
    "Ethical Hacking",
    "Penetration Testing",
    "Cryptography",
    "Authentication",
    "Authorization",
    "OAuth",
    "JWT",
    "SSL",
    "TLS",
    "OWASP",
    "Web Security",

    # --------------------------------------------------------
    # BIG DATA
    # --------------------------------------------------------
    "Big Data",
    "Hadoop",
    "Spark",
    "PySpark",
    "Hive",
    "Pig",
    "Kafka",

    # --------------------------------------------------------
    # OTHER TECHNICAL SKILLS
    # --------------------------------------------------------
    "Blockchain",
    "Internet of Things",
    "IoT",
    "Embedded Systems",
    "Arduino",
    "Raspberry Pi",
    "Robotics",
    "MATLAB",
    "Agile",
    "Scrum",
    "JIRA",
    "Confluence",
    "SDLC"
]



def extract_skills(text):
    """
    Extract technical skills that are actually present
    in the uploaded resume text.
    """

    if not text:
        return []

    text = text.lower()

    # Normalize common variations
    text = text.replace("nodejs", "node.js")
    text = text.replace("node js", "node.js")

    text = text.replace("reactjs", "react.js")
    text = text.replace("react js", "react.js")

    text = text.replace("angular js", "angularjs")

    text = text.replace("springboot", "spring boot")
    text = text.replace("spring-boot", "spring boot")

    text = text.replace("machine-learning", "machine learning")

    text = text.replace("deep-learning", "deep learning")

    text = text.replace("artificial-intelligence", "artificial intelligence")

    text = text.replace("natural-language-processing",
                        "natural language processing")

    text = text.replace("scikit learn", "scikit-learn")

    text = text.replace("power-bi", "power bi")

    text = text.replace("ci cd", "ci/cd")

    # Store detected skills
    detected_skills = []

    # Check every skill
    for skill in SKILLS:

        skill_lower = skill.lower()

        # Create safe regular expression
        pattern = r"(?<!\w)" + re.escape(skill_lower) + r"(?!\w)"

        # Check whether skill exists in resume
        if re.search(pattern, text):

            # Avoid duplicate skills
            if skill not in detected_skills:
                detected_skills.append(skill)

    return detected_skills

def get_skills_string(text):
    """
    Return detected skills as a comma-separated string.
    Useful for storing skills in MySQL.
    """

    skills = extract_skills(text)

    return ", ".join(skills)


if __name__ == "__main__":

    sample_resume = """
    I am a Computer Science student with experience in Python,
    Java, HTML, CSS, JavaScript, Flask, MySQL and Machine Learning.

    I have worked with Pandas, NumPy, Scikit-learn and GitHub.
    I also have knowledge of Data Structures, OOP and DBMS.
    """

    detected = extract_skills(sample_resume)

    print("Detected Technical Skills:")
    print("--------------------------------")

    for skill in detected:
        print(skill)

    print("\nTotal Skills:", len(detected))