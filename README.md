# CSE Core Subject Personalized Chatbot

A RAG (Retrieval-Augmented Generation) chatbot built for Computer Science Engineering students. It answers questions from CSE core subject books using FAISS vector search and Groq's LLaMA 3.1 model, with answers personalized to each student's semester and preferred style.

---

## Features

- **RAG pipeline** — retrieves relevant content from CSE textbooks before generating answers
- **Personalized responses** — tailors answers based on student name, semester, and answer style (Exam Oriented / Conceptual / Short Notes)
- **Fast inference** — powered by Groq's LLaMA 3.1 8B Instant model
- **Pre-built FAISS index** — no need to re-embed documents on every run
- **Streamlit UI** — clean, interactive web interface

---

## Books Indexed

| Subject | File |
|---|---|
| Data Structures & Algorithms | `DSA-Book.pdf` |
| Computer Networks | `CN-Book.pdf` |
| Computer Graphics | `CG-Book.pdf` |
| Cloud Computing | `CC-Book.pdf` |
| Blockchain | `Blockchain-Book.pdf` |

---

## Tech Stack

| Component | Library / Service |
|---|---|
| UI | Streamlit |
| LLM | Groq — LLaMA 3.1 8B Instant |
| Embeddings | `sentence-transformers/all-MiniLM-L6-v2` |
| Vector Store | FAISS |
| Orchestration | LangChain |
| PDF Parsing | PyPDF |

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/your-username/CSE-Chatbot.git
cd CSE-Chatbot
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add your Groq API key

Create a `.env` file in the project root:

```
GROQ_API_KEY=your_groq_api_key_here
```

Get a free API key at [console.groq.com](https://console.groq.com).

### 5. Build the FAISS index (first time only)

Open and run all cells in `notebook/chatbot.ipynb`. This reads the PDFs from `books/`, generates embeddings, and saves the FAISS index to `faiss_index/`.

### 6. Run the app

```bash
streamlit run app.py
```

---

## Project Structure

```
CSE-Chatbot/
├── app.py                  # Streamlit app
├── requirements.txt        # Python dependencies
├── .env                    # Groq API key (not committed)
├── books/                  # Source PDF textbooks
│   ├── DSA-Book.pdf
│   ├── CN-Book.pdf
│   ├── CG-Book.pdf
│   ├── CC-Book.pdf
│   └── Blockchain-Book.pdf
├── faiss_index/            # Pre-built FAISS vector index
│   ├── index.faiss
│   └── index.pkl
└── notebook/
    └── chatbot.ipynb       # Index-building notebook
```

---

## How It Works

1. PDFs are parsed and split into chunks.
2. Chunks are embedded using `all-MiniLM-L6-v2` and stored in a FAISS index.
3. At query time, the top-2 most relevant chunks are retrieved.
4. The student's profile (name, semester, answer style) is prepended to the query.
5. Groq's LLaMA 3.1 model generates an answer grounded in the retrieved context.

---

## License

MIT
