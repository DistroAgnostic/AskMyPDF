## 🧠📄 AskMyPDF – Chat with Any PDF Using LangChain

> Your personal AI assistant that reads, understands, and chats with your PDF documents – powered by LangChain.

![AskMyPDF Banner](https://img.shields.io/badge/Powered%20By-Google%20Gemini-blue?logo=google)
![LangChain](https://img.shields.io/badge/Built%20With-LangChain-purple)
![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-red?logo=streamlit)

---

### 🚀 Features

* 🔍 **Ask Anything** – Chat with any PDF as if it’s your research assistant.
* 🧠 **Google Gemini 2.5 Flash** – Fast, context-aware responses.
* 📄 **PDF Parsing** – Intelligent PDF document splitting and parsing.
* 🧬 **Vector Embedding** – Uses `embedding-001` from Google for semantic understanding.
* 🔗 **RAG Architecture** – Combines retrieval + generation using LangChain.

---

### 💡 Use Cases

* Academic Paper Summarization
* Legal Document Analysis
* Corporate Report Review
* Code Documentation Q\&A
* Book/Manuals Exploration

---

### 🛠️ Tech Stack

| Tool                                                                                          | Purpose          |
| --------------------------------------------------------------------------------------------- | ---------------- |
| [Streamlit](https://streamlit.io/)                                                            | Frontend UI      |
| [LangChain](https://www.langchain.com/)                                                       | RAG Logic        |
| [Google Generative AI](https://makersuite.google.com/app)                                     | LLM & Embeddings |
| [Chroma](https://www.trychroma.com/)                                                          | Vector DB        |
| [PyPDFLoader](https://python.langchain.com/docs/modules/data_connection/document_loaders/pdf) | PDF Parsing      |

---

### 📦 Installation

```bash
git clone https://github.com/yourusername/pdf-whisperer.git
cd pdf-whisperer
pip install -r requirements.txt
```

---

### 🔑 Setup

1. Create a `.env` file in the root directory:

```env
GOOGLE_API_KEY=your_google_api_key_here
```

2. Replace the path in the code with your PDF file path:

```python
loader = PyPDFLoader(r'/path/to/your/document.pdf')
```

---

### 🧪 Run the App

```bash
streamlit run app.py
```

---

<!-- ### 💬 Screenshot

*(Add a screenshot here of the Streamlit chat interface in action)*

---
-->

### 📘 Example Query

> **User:** "Summarize the conclusion section."
> **Assistant:** "The conclusion highlights that..."

---

### 🚧 To-Do

* [ ] Upload multiple PDFs
* [x] Memory-enabled chat
* [ ] Save chat history
* [ ] Shareable links to sessions

---

### 🖤 Contributing

Pull requests are welcome! For major changes, open an issue first to discuss what you’d like to change.

---

### 📄 License

MIT License © 2025
