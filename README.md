# 📚 English Learning Assistant Web App

![Flask](https://img.shields.io/badge/Framework-Flask-blue?logo=flask)
![Gemini LLM](https://img.shields.io/badge/AI-Gemini_LLMs-green?logo=google)
![Architecture](https://img.shields.io/badge/Architecture-MVC-orange)

---

## 📝 Description

A simple yet powerful **Flask** web application designed to help students and learners **check and improve their English practice work**.  
It evaluates three skills — **Listening**, **Reading**, and **Writing** — by integrating **Gemini LLMs** for intelligent feedback.  
Supports both **text-based** and **image-based** submissions for maximum convenience.

> 🚀 Focused on fast deployment without user authentication, using a lightweight MVC structure.

---

## ✨ Features

- 📖 **Skill Evaluation**: Listening | Reading | Writing.
- 📝 **Model Answer Comparison**: Input reference answers to enhance checking accuracy.
- 🖼️ **Image Input**: Upload images of handwritten/printed answers (OCR supported).
- 🤖 **AI-Powered Analysis**: Powered by Gemini LLMs for deep feedback and suggestion generation.
- ⚡ **Simple Usage**: No login, no complex setup — ready to use instantly.
- 🛠️ **MVC Architecture**: Organized cleanly into Model, View, and Controller layers.

---

## 🛠 Tech Stack

| Component         | Technology                                 |
| ----------------- | ------------------------------------------ |
| Backend Framework | Flask (Python)                             |
| AI Integration    | Gemini LLMs API                            |
| Frontend          | HTML + CSS + JavaScript (Jinja2 templates) |
| Architecture      | MVC                                        |

---

## 📂 Project Structure

```bash
/project_root
│
├── app/
│   ├── AI/              # Setup LLMs
│   ├── extentions/      # Setup extentions
│   ├── static/          # Frontend assets (CSS, JS, images)
│   ├── templates/       # Jinja2 HTML templates
│   ├── controllers/     # Route handlers (views)
│   └── __init__.py      # Initialize the application
├── entry.py             # Main Flask application entry
├── config.py            # Config for Flask application
├── requirements.txt     # Python dependencies
├── README.md            # Project documentation
└── .env                 # Environment variables (NOT included in repo)

```

## 🚀 Installation Guide

1. Clone the repo:

```bash
git clone https://github.com/ZanhNe/english-checking
cd english-checking
```

2. Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required packages:

```bash
pip install -r requirements.txt
```

4. Set environment variables:

```bash
GEMINI_API_KEY=your_gemini_api_key_here
ELEVENLAB_API_KEY=your_ocr_api_key_here   # (if OCR service is used)
```

5. Run the Flask app:

```bash
flask run
python entry.py # If you have trouble with flask run
```

6. Access the application at http://127.0.0.1:5000
