# NLP-LLM Resume Assessment

A full-stack web application that parses, analyzes, and optimizes resumes using Natural Language Processing (NLP) and Large Language Models (LLMs). The tool extracts structured data from PDF resumes, compares them against job descriptions, provides actionable improvement suggestions, and generates ATS-friendly PDF resumes.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [How It Works](#how-it-works)
- [Configuration](#configuration)
- [Screenshots](#screenshots)

---

## Overview

Applying for jobs is competitive. This tool helps job seekers optimize their resumes by:

- Automatically parsing PDF resumes into structured data
- Comparing resume content against a specific job description
- Detecting weak verbs, filler words, and repetitive language
- Suggesting stronger, more impactful alternatives
- Rewriting responsibilities to be concise and metrics-driven (ATS-friendly)
- Generating a clean, professionally formatted PDF resume

Built as a term project combining NLP techniques with modern LLM capabilities (Google Gemini).

---

## Features

### Resume Parsing
- Extracts text from uploaded PDF resumes
- Identifies and separates resume sections (Personal Info, Education, Work Experience, Projects, Skills)
- Uses Google Gemini LLM to extract structured JSON from complex sections
- Uses spaCy NER for personal information extraction (name, location)
- Regex-based extraction for email, phone, LinkedIn, and GitHub

### Job Description Analysis
- Parses a job description to extract required skills
- Uses spaCy entity ruler with a custom skill pattern dataset
- Compares extracted job skills against resume skills

### Grammar & Language Analysis
- **Weak Verb Detection** — Flags weak verbs (e.g., "helped", "worked", "used") and suggests stronger alternatives
- **Filler Word Detection** — Detects common filler phrases (e.g., "responsible for", "in order to", "worked with")
- **Repetitive Verb Detection** — Identifies overused action verbs across bullet points
- **Consistency Checks** — Validates capitalization consistency for job titles and institutions
- **Tone Checks** — Flags informal language (e.g., "stuff", "things", "awesome")
- **Bullet Point Length Validation** — Ensures responsibilities are concise and meaningful

### LLM-Powered Rewriting
- One-click rewriting of individual responsibilities via Google Gemini
- Rewrites are optimized to be 20–30 words, ATS-friendly, and include quantifiable metrics
- Custom prompt engineering for professional resume language

### PDF Generation
- Converts structured resume JSON to a LaTeX document
- Compiles LaTeX to a professional, clean PDF via `pdflatex`
- Handles special character escaping for LaTeX compatibility
- Stores generated PDFs with unique UUIDs

### Interactive Web Interface
- Upload resume and enter job description on one page
- View and edit all parsed resume data inline
- Receive real-time suggestions organized by category
- Trigger LLM rewrites for individual bullet points
- Download the final generated PDF

---

## Tech Stack

| Category | Technology |
|---|---|
| Backend | Python 3, Flask 3.0.3 |
| NLP | spaCy 3.7.5, NLTK 3.8.1 |
| LLM | Google Gemini API (`gemini-1.0-pro-latest`) |
| PDF Parsing | PyPDF2 3.0.1 |
| PDF Generation | LaTeX / pdflatex |
| Frontend | HTML5, Bootstrap 4.5.2, Tailwind CSS, Vanilla JS |
| Data Validation | Pydantic 2.8.2 |
| Environment | python-dotenv 1.0.1 |

---

## Project Structure

```
NLP-LLM-Resume-assessment/
│
├── app/                                   # Flask web application
│   ├── __init__.py                        # App factory and configuration
│   ├── controllers/
│   │   └── resume_parser_controller.py    # API routes and request handlers
│   ├── models/
│   │   └── resume.py                      # Resume data model
│   ├── templates/
│   │   ├── upload_resume.html             # Resume upload form
│   │   └── result.html                    # Results and analysis UI
│   ├── static/
│   │   └── rewrite.png                    # UI asset
│   └── newoutput/                         # Generated PDFs storage
│
├── resume_parser/                         # Core NLP parsing modules
│   ├── resume_parser.py                   # Parsing orchestrator
│   ├── personal_info_extractor.py         # Name, email, phone, LinkedIn, GitHub
│   ├── education_extractor.py             # Education extraction (Gemini LLM)
│   ├── work_experience_extractor.py       # Work experience extraction (Gemini LLM)
│   ├── projects_extractor.py              # Projects extraction (Gemini LLM)
│   ├── skills_extractor.py                # Skills extraction (spaCy NER)
│   ├── gemini.py                          # Google Gemini API integration
│   ├── kw.py                              # Weak verb detection and suggestions
│   ├── filler.py                          # Filler words, consistency, tone analysis
│   ├── repetitive_verbs.py                # Overused verb detection
│   └── LaTeXGen.py                        # LaTeX/PDF resume generation
│
├── job_parser/
│   └── job_parser.py                      # Job description skill extraction
│
├── data/
│   └── skill_patterns.jsonl               # spaCy skill entity patterns
│
├── config/
│   └── config.py                          # Flask configuration
│
├── uploads/                               # Uploaded resume PDFs
├── run.py                                 # Application entry point
├── requirements.txt                       # Python dependencies
└── .gitignore
```

---

## Installation

### Prerequisites

- Python 3.10+
- `pdflatex` installed and available in system PATH (for PDF generation)
- Google Gemini API key

### Steps

1. **Clone the repository**

```bash
git clone https://github.com/your-username/NLP-LLM-Resume-assessment.git
cd NLP-LLM-Resume-assessment
```

2. **Create and activate a virtual environment**

```bash
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate
```

3. **Install Python dependencies**

```bash
pip install -r requirements.txt
```

4. **Download spaCy language model**

```bash
python -m spacy download en_core_web_sm
```

5. **Set up environment variables**

Create a `.env` file in the project root:

```
gemini_api=YOUR_GOOGLE_GEMINI_API_KEY
```

6. **Run the application**

```bash
python run.py
```

7. **Open in browser**

```
http://localhost:5000
```

---

## Usage

1. **Upload Resume** — Upload your resume as a PDF file on the home page
2. **Enter Job Description** — Paste the job description text into the provided field
3. **View Parsed Data** — The app displays all extracted resume data in structured form
4. **Analyze Resume** — Click "Recheck" to run grammar, language, and content analysis
5. **Review Suggestions** — Browse suggestions organized by category (verbs, fillers, tone, etc.)
6. **Rewrite Bullets** — Click "Rewrite" on any responsibility to get an LLM-improved version
7. **Edit Inline** — Manually edit any section of the parsed resume
8. **Generate PDF** — Click "Generate PDF" to create a professionally formatted, downloadable PDF

---

## API Endpoints

| Method | Route | Description |
|---|---|---|
| `GET` | `/` | Display resume upload form |
| `POST` | `/` | Upload PDF and parse resume |
| `POST` | `/api/JD` | Extract skills from job description |
| `POST` | `/api/recheck` | Run full resume analysis |
| `POST` | `/api/rewrite` | Rewrite a responsibility using Gemini |
| `POST` | `/API/generate_pdf` | Generate PDF from resume JSON |
| `GET` | `/download/<filename>` | Download generated PDF |
| `GET` | `/pdfs` | List all generated PDFs |

---

## How It Works

### Resume Parsing Pipeline

```
Upload PDF
    ↓
Extract text (PyPDF2)
    ↓
Identify sections (regex)
    ↓
Extract data per section:
  ├── Personal Info  → regex + spaCy NER
  ├── Education      → Google Gemini LLM
  ├── Work Exp       → Google Gemini LLM
  ├── Projects       → Google Gemini LLM
  └── Skills         → spaCy EntityRuler
    ↓
Return structured JSON
```

### Analysis Pipeline

```
Resume JSON + Job Description
    ↓
Job skill extraction (spaCy + skill_patterns.jsonl)
    ↓
Resume analysis:
  ├── Weak verb detection       (kw.py)
  ├── Filler word detection     (filler.py)
  ├── Repetitive verb counting  (repetitive_verbs.py)
  ├── Consistency checks        (filler.py)
  ├── Tone checks               (filler.py)
  └── Bullet point length       (controller)
    ↓
Return suggestions array
```

### PDF Generation Pipeline

```
Resume JSON
    ↓
Escape LaTeX special characters
    ↓
Generate .tex file from template
    ↓
Compile with pdflatex
    ↓
Save PDF with UUID filename
    ↓
Return download URL
```

---

## Configuration

| Setting | Location | Description |
|---|---|---|
| `SECRET_KEY` | `config/config.py` | Flask secret key |
| `UPLOAD_FOLDER` | `config/config.py` | Directory for uploaded PDFs |
| `GENERATED_FOLDER` | `config/config.py` | Directory for generated files |
| `gemini_api` | `.env` | Google Gemini API key |

---

## Resume JSON Structure

The application works with the following resume data structure:

```json
{
  "Personal Info": {
    "Name": "string",
    "Phone": "string",
    "Email": "string",
    "LinkedIn": "string",
    "GitHub": "string",
    "Location": "string"
  },
  "Education": [
    {
      "Institution": "string",
      "Location": "string",
      "Degree": "string",
      "Start Year": "string",
      "End Year": "string"
    }
  ],
  "Work Experience": [
    {
      "job_title": "string",
      "company": "string",
      "date_range": "string",
      "location": "string",
      "responsibilities": ["string"]
    }
  ],
  "Projects": [
    {
      "Project_title": "string",
      "Project_description": "string",
      "Project_links": "string",
      "Project_dates": "string",
      "project_skills": "string"
    }
  ],
  "Skills": "string"
}
```

---

## Notes

- `pdflatex` must be installed on the server for PDF generation to work
- The Gemini API key is required for LLM-powered extraction and rewriting features
- Resume parsing accuracy depends on the formatting and structure of the uploaded PDF
- Only PDF file format is accepted for resume uploads

---

*Built as a term project — Summer 2024*
