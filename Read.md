# 📚 AI Study Buddy

An intelligent study assistant powered by **Google Gemini 1.5 Flash** + **LangChain** + **Streamlit**.

## ✨ Features

| Feature | Description |
|---|---|
| 📝 **Smart Summary** | Structured TL;DR + key concepts + takeaways |
| 🃏 **Flashcards** | Interactive flip cards with shuffle & navigation |
| 🎯 **Quiz** | Multiple-choice quiz with instant scoring |
| 💬 **Chat Tutor** | Ask anything — grounded in your uploaded material |
| 🔍 **Raw Text** | View and download extracted content |

## 🚀 Quick Start

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Get a free Google Gemini API key
Visit → https://aistudio.google.com/app/apikey

### 3. Run the app
```bash
streamlit run app.py
```

### 4. Use the app
1. Paste your **Gemini API key** in the sidebar
2. **Upload** a PDF or TXT file (notes, textbook chapter, etc.)
3. Choose a tab: Summary / Flashcards / Quiz / Chat Tutor
4. Click **Generate** and study smarter 🎓

## 📁 Supported File Types
- `.pdf` — Textbooks, lecture slides exported as PDF, papers
- `.txt` — Plain text notes, markdown files (rename to .txt)

## 🛠 Tech Stack
- **LangChain** — LLM orchestration & prompt chaining
- **Google Generative AI (Gemini 1.5 Flash)** — Fast, capable LLM
- **pdfplumber** — Reliable PDF text extraction
- **Streamlit** — Interactive UI framework

## 📐 Architecture

```
User uploads PDF/TXT
        ↓
  Text Extraction (pdfplumber / utf-8)
        ↓
  Chunking (first 12k chars for prompting)
        ↓
  LangChain PromptTemplate + LLMChain
        ↓
  Google Gemini 1.5 Flash API
        ↓
  Parsed Output → Summary / Cards / Quiz / Chat
```

## 💡 Tips
- For large documents, only the first ~12,000 characters are sent to the LLM (configurable in `chunk_text()`)
- The Chat Tutor uses the first 8,000 characters as context
- Flashcard and quiz counts are adjustable via sidebar sliders