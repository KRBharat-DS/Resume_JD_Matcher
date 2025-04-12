# Resume_JD_Matcher
An AI-powered resume and job description matcher using BERT &amp; Streamlit

# Resume-JD Matcher Agent

An intelligent tool to match resumes with job descriptions using semantic similarity powered by BERT. Built for quick evaluation of resume fitment, it helps users understand how well a resume aligns with a given job description.

---

## 🚀 Features

- 🔍 **BERT-Based Semantic Matching** using `all-MiniLM-L6-v2` for high-speed, meaningful comparisons.
- 📄 **PDF Resume Parsing** using PyMuPDF.
- 🌐 **JD Text Input** via upload or manual text entry (URL input coming soon).
- 📊 **Similarity Score** shown as a percentage.
- 🔑 **Common Keyword/N-Gram Matching** (currently simple overlap; to be enhanced).
- 🖥️ **Streamlit Interface** for easy interaction.
- 🛠️ **Batch File for One-Click Startup** on Windows.

---

## 🏗️ Project Structure

```
resume-jd-matcher/
├── app/
│   └── streamlit_app.py         # Streamlit frontend logic
│
├── src/
│   └── utils.py                # Resume parsing, JD extraction, BERT similarity
│
├── models/                     # (Optional) Pre-trained models if needed
│
├── data/                       # (Optional) Example resumes and JDs
│
├── run_app.bat                 # Batch file to activate env and launch app
├── requirements.txt            # Python dependencies
└── README.md                   # Project documentation
```

---

## 💻 Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/resume-jd-matcher.git
   cd resume-jd-matcher
   ```

2. **Create & Activate Conda Environment**
   ```bash
   conda create -n resume_agent python=3.10
   conda activate resume_agent
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run App (Option 1: Streamlit CLI)**
   ```bash
   streamlit run app/streamlit_app.py
   ```

5. **Run App (Option 2: Batch File)**
   On Windows, double-click `run_app.bat` for automatic launch.

---

## 📈 Coming Soon

- ✅ **Improved Keyword Extraction** using TF-IDF or spaCy NER.
- ✅ **Gap Analysis**: Skills/Experience mismatch checker.
- ✅ **Resume Improvement Suggestions**.
- ✅ **RAG-based Similar Job/Company Insights**.
- 📎 **PDF Report Generation**.

---

## 🧠 How It Works

- Text from the resume and JD are extracted.
- The BERT model (`all-MiniLM-L6-v2`) encodes both texts.
- Cosine similarity is computed to produce a match score.

---

## 👨‍💻 Author

Created by [Your Name] as part of an AI Agent Capstone Project.

Feel free to contribute, fork, or raise issues!

