# 🤖 AI Resume Screening and Job Recommendation System

An intelligent web-based application that analyzes resumes, extracts relevant skills, calculates an ATS-style resume score, and recommends suitable job opportunities based on the candidate's skills and job requirements.

The system provides a simple and modern interface for candidates to upload their resumes and understand how well their profile matches available job opportunities.

## 🌐 Live Demo

🚀 **Try the application:**
https://ai-resume12.vercel.app/

> **Note:** The live deployment demonstrates the application interface and functionality. Features that require a local MySQL database or local file storage may require additional cloud configuration for production use.

## 🚀 Features

### 📄 Resume Upload & Parsing

* Upload resumes in **PDF** or **DOCX** format.
* Automatically extract text from uploaded resumes.
* Analyze resume content without manually entering information.

### 🧠 AI-Based Resume Analysis

* Detect technical skills from resume content.
* Identify important resume sections.
* Detect action-oriented words.
* Identify quantified achievements and results.

### 📊 ATS Resume Scoring

The system calculates an ATS-style score based on:

* Skills
* Resume sections
* Contact information
* Resume length
* Action verbs
* Quantified results
* Job keywords

The final score is calculated on a **0–100 scale**.

### 🎯 Job Matching

* Compare resume skills with job requirements.
* Identify matching skills.
* Identify missing skills.
* Calculate keyword matching percentage.
* Compare resume content with a target job description using **TF-IDF and cosine similarity**.

### 💼 Job Recommendations

Recommend relevant job opportunities based on detected resume skills.

### 📋 Resume Improvement Suggestions

Provides suggestions based on the resume analysis results.

### 🔐 User Authentication

* User registration
* Secure login
* Password hashing
* Session-based authentication
* Logout functionality

## 🛠️ Technology Stack

### 💻 Languages

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge\&logo=python\&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge\&logo=javascript\&logoColor=black)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge\&logo=html5\&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge\&logo=css3\&logoColor=white)
![SQL](https://img.shields.io/badge/SQL-336791?style=for-the-badge\&logo=postgresql\&logoColor=white)

### ⚙️ Frameworks & Backend

![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge\&logo=flask\&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-7952B3?style=for-the-badge\&logo=bootstrap\&logoColor=white)

### 🗄️ Database

![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge\&logo=mysql\&logoColor=white)

### 🧠 AI / Machine Learning

![Scikit Learn](https://img.shields.io/badge/Scikit--Learn-F7931E?style=for-the-badge\&logo=scikit-learn\&logoColor=white)
![NLP](https://img.shields.io/badge/NLP-8A2BE2?style=for-the-badge\&logo=googletranslate\&logoColor=white)

### 📄 Resume Processing

![PyPDF2](https://img.shields.io/badge/PyPDF2-FF6F00?style=for-the-badge)
![Python DOCX](https://img.shields.io/badge/python--docx-2B579A?style=for-the-badge\&logo=microsoftword\&logoColor=white)

### 🔧 Tools

![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge\&logo=git\&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge\&logo=github\&logoColor=white)
![VS Code](https://img.shields.io/badge/VS%20Code-007ACC?style=for-the-badge\&logo=visualstudiocode\&logoColor=white)
![Vercel](https://img.shields.io/badge/Vercel-000000?style=for-the-badge\&logo=vercel\&logoColor=white)

## 📂 Project Structure

```text
AI-Resume-Screening/
│
├── app.py
│
├── templates/
│   ├── index.html
│   ├── register.html
│   ├── login.html
│   ├── dashboard.html
│   ├── upload_resume.html
│   ├── resume_analysis.html
│   ├── jobs.html
│   └── 404.html
│
├── uploads/
│
├── database/
│
├── nlp/
│   ├── resume_parser.py
│   ├── text_processor.py
│   ├── skill_extractor.py
│   └── job_matcher.py
│
├── requirements.txt
│
└── README.md
```

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Tharunnayak-45/AI-Resume-Screening.git
```

### 2. Open the Project

```bash
cd AI-Resume-Screening
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

### 4. Activate the Virtual Environment

**Windows:**

```bash
venv\Scripts\activate
```

**macOS / Linux:**

```bash
source venv/bin/activate
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

## 🗄️ Database Configuration

Make sure MySQL Server is installed and running.

Create the database:

```sql
CREATE DATABASE ai_resume_db;
```

Configure your MySQL connection in `app.py`.

Example:

```python
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "YOUR_MYSQL_PASSWORD",
    "database": "ai_resume_db"
}
```

## ▶️ Running the Application

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5000/
```

## 🔄 Application Workflow

```text
Register / Login
       ↓
Upload Resume
       ↓
PDF / DOCX Text Extraction
       ↓
Resume Content Analysis
       ↓
Skill Detection
       ↓
ATS Score Calculation
       ↓
Target Job Comparison
       ↓
Keyword Matching
       ↓
Missing Skill Detection
       ↓
Job Recommendations
       ↓
Resume Improvement Suggestions
```

## 📊 ATS Scoring Model

| Category            | Maximum Score |
| ------------------- | ------------: |
| Skills              |            20 |
| Resume Sections     |            22 |
| Contact Information |             6 |
| Resume Length       |            10 |
| Action Verbs        |            10 |
| Quantified Results  |             7 |
| Job Keywords        |            25 |
| **Total**           |       **100** |

The score is an **ATS-style resume analysis indicator** and does not represent an actual employer hiring decision.

## 🧠 Job Matching

The system uses **TF-IDF** to represent resume and job-description text and **cosine similarity** to measure textual similarity.

```text
Resume
   +
Job Description
   ↓
TF-IDF Vectorization
   ↓
Cosine Similarity
   ↓
Matching Score
```

It also compares detected skills to identify:

* Matched Skills
* Missing Skills

## 🔮 Future Enhancements

* Advanced NLP-based resume parsing
* Named Entity Recognition
* Improved skill extraction
* Semantic embeddings
* Advanced job recommendation algorithms
* Recruiter dashboard
* Multiple resume comparison
* Resume builder
* Job API integration
* Cloud database integration
* Production deployment

## 📌 Limitations

* Resume extraction quality depends on document formatting.
* Image-only PDFs require OCR for reliable text extraction.
* Skill detection currently uses predefined skill patterns.
* ATS scoring is an analytical heuristic.
* Job recommendations depend on the available job dataset.

## 👨‍💻 Developer

**Mudavath Tharun**

B.Tech Computer Science and Engineering
Vidya Jyothi Institute of Technology (VJIT), Hyderabad

### Profiles

* LinkedIn: https://www.linkedin.com/in/mudavaththarun45
* GitHub: https://github.com/Tharunnayak-45
* Portfolio: https://tharunportfolio-nayak.vercel.app/

### 🌐 Live Project

**AI Resume Screening:**
https://ai-resume12.vercel.app/

## ⭐ Project Overview

This project combines **Web Development, Python, Database Management, NLP, and Machine Learning concepts** to create a practical resume analysis and job recommendation platform.

```text
Frontend
   ↓
Flask Backend
   ↓
MySQL Database
   ↓
Resume Processing
   ↓
NLP / ML
   ↓
ATS Scoring
   ↓
Job Matching
   ↓
Recommendations
```

## 📜 License

This project is created for **educational and portfolio purposes**.
