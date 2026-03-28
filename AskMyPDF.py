import platform
if platform.system() == "Linux":
    try:
        __import__("pysqlite3")
        import sys
        sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")
    except ImportError:
        pass

import os
import sys
import tempfile
import streamlit as st
from datetime import datetime

st.set_page_config(
    page_title="AskMyPDF — AI Document Chat",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

:root {
    --glass-bg: rgba(255, 255, 255, 0.04);
    --glass-bg-hover: rgba(255, 255, 255, 0.08);
    --glass-border: rgba(255, 255, 255, 0.08);
    --glass-border-hover: rgba(255, 255, 255, 0.15);
    --accent: #7C6AFF;
    --accent-glow: rgba(124, 106, 255, 0.3);
    --accent-soft: rgba(124, 106, 255, 0.12);
    --text-primary: #F0EEF6;
    --text-secondary: rgba(240, 238, 246, 0.55);
    --text-muted: rgba(240, 238, 246, 0.35);
    --surface-dark: #0A0A10;
    --surface-card: rgba(15, 14, 24, 0.65);
    --user-bubble: rgba(124, 106, 255, 0.12);
    --user-bubble-border: rgba(124, 106, 255, 0.2);
    --assistant-bubble: rgba(255, 255, 255, 0.03);
    --assistant-bubble-border: rgba(255, 255, 255, 0.06);
    --success: #34D399;
    --warning: #FBBF24;
    --danger: #F87171;
    --radius: 16px;
    --radius-sm: 10px;
    --radius-xs: 6px;
    --transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

* { font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important; }

.stApp {
    background: var(--surface-dark) !important;
    background-image:
        radial-gradient(ellipse 80% 60% at 20% 10%, rgba(124, 106, 255, 0.06) 0%, transparent 60%),
        radial-gradient(ellipse 60% 50% at 80% 90%, rgba(99, 102, 241, 0.04) 0%, transparent 55%),
        radial-gradient(ellipse 40% 40% at 50% 50%, rgba(139, 92, 246, 0.03) 0%, transparent 50%) !important;
}

section[data-testid="stSidebar"] {
    background: rgba(10, 10, 16, 0.75) !important;
    backdrop-filter: blur(40px) saturate(1.5) !important;
    -webkit-backdrop-filter: blur(40px) saturate(1.5) !important;
    border-right: 1px solid var(--glass-border) !important;
}

section[data-testid="stSidebar"] .stMarkdown p,
section[data-testid="stSidebar"] .stMarkdown li,
section[data-testid="stSidebar"] .stMarkdown span {
    color: var(--text-secondary) !important;
    font-size: 0.85rem !important;
}

header[data-testid="stHeader"] { background: transparent !important; }
footer { display: none !important; }
#MainMenu { display: none !important; }

.block-container {
    max-width: 900px !important;
    padding: 2rem 1.5rem 6rem !important;
}

.glass-card {
    background: var(--glass-bg);
    backdrop-filter: blur(24px) saturate(1.3);
    -webkit-backdrop-filter: blur(24px) saturate(1.3);
    border: 1px solid var(--glass-border);
    border-radius: var(--radius);
    padding: 1.5rem;
    transition: var(--transition);
}
.glass-card:hover {
    background: var(--glass-bg-hover);
    border-color: var(--glass-border-hover);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
}

.hero-title {
    font-size: 2.2rem;
    font-weight: 700;
    letter-spacing: -0.03em;
    background: linear-gradient(135deg, #F0EEF6 0%, #7C6AFF 50%, #A78BFA 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.25rem;
    line-height: 1.2;
}
.hero-sub {
    color: var(--text-muted);
    font-size: 0.9rem;
    font-weight: 300;
    letter-spacing: 0.02em;
}

.stat-row {
    display: flex;
    gap: 0.75rem;
    flex-wrap: wrap;
    margin-top: 0.75rem;
}
.stat-pill {
    background: var(--accent-soft);
    border: 1px solid rgba(124, 106, 255, 0.15);
    color: #C4B5FD;
    font-size: 0.72rem;
    font-weight: 500;
    padding: 0.35rem 0.8rem;
    border-radius: 100px;
    letter-spacing: 0.03em;
    text-transform: uppercase;
}

.chat-user {
    background: var(--user-bubble);
    border: 1px solid var(--user-bubble-border);
    border-radius: var(--radius) var(--radius) 4px var(--radius);
    padding: 1rem 1.25rem;
    margin: 0.5rem 0;
    color: var(--text-primary);
    font-size: 0.9rem;
    line-height: 1.6;
    max-width: 85%;
    margin-left: auto;
    animation: slideInRight 0.35s ease-out;
}
.chat-assistant {
    background: var(--assistant-bubble);
    backdrop-filter: blur(12px);
    border: 1px solid var(--assistant-bubble-border);
    border-radius: var(--radius) var(--radius) var(--radius) 4px;
    padding: 1rem 1.25rem;
    margin: 0.5rem 0;
    color: var(--text-primary);
    font-size: 0.9rem;
    line-height: 1.7;
    max-width: 85%;
    animation: slideInLeft 0.35s ease-out;
}
.chat-label {
    font-size: 0.65rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 0.4rem;
    opacity: 0.5;
}
.chat-user .chat-label { color: #A78BFA; text-align: right; }
.chat-assistant .chat-label { color: #94A3B8; }

.chat-time {
    font-size: 0.6rem;
    color: var(--text-muted);
    margin-top: 0.4rem;
    opacity: 0.6;
}
.chat-user .chat-time { text-align: right; }

.typing-indicator {
    display: flex;
    align-items: center;
    gap: 0.35rem;
    padding: 0.8rem 1.25rem;
    background: var(--assistant-bubble);
    border: 1px solid var(--assistant-bubble-border);
    border-radius: var(--radius) var(--radius) var(--radius) 4px;
    max-width: 100px;
}
.typing-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: var(--text-muted);
    animation: bounce 1.4s ease-in-out infinite;
}
.typing-dot:nth-child(2) { animation-delay: 0.2s; }
.typing-dot:nth-child(3) { animation-delay: 0.4s; }

.welcome-card {
    background: linear-gradient(135deg, rgba(124, 106, 255, 0.08) 0%, rgba(99, 102, 241, 0.04) 100%);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(124, 106, 255, 0.12);
    border-radius: var(--radius);
    padding: 2.5rem;
    text-align: center;
    margin: 2rem 0;
}
.welcome-icon {
    font-size: 3rem;
    margin-bottom: 1rem;
    filter: drop-shadow(0 0 20px var(--accent-glow));
}
.welcome-title {
    font-size: 1.3rem;
    font-weight: 600;
    color: var(--text-primary);
    margin-bottom: 0.5rem;
}
.welcome-text {
    color: var(--text-secondary);
    font-size: 0.85rem;
    line-height: 1.6;
    max-width: 400px;
    margin: 0 auto;
}

.chip-row {
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
    justify-content: center;
    margin-top: 1.25rem;
}
.chip {
    background: var(--glass-bg);
    border: 1px solid var(--glass-border);
    color: var(--text-secondary);
    font-size: 0.75rem;
    padding: 0.45rem 1rem;
    border-radius: 100px;
    cursor: pointer;
    transition: var(--transition);
}
.chip:hover {
    background: var(--accent-soft);
    border-color: rgba(124, 106, 255, 0.2);
    color: #C4B5FD;
}

section[data-testid="stFileUploader"] {
    background: var(--glass-bg) !important;
    border: 1px dashed var(--glass-border) !important;
    border-radius: var(--radius) !important;
    padding: 0.5rem !important;
    transition: var(--transition) !important;
}
section[data-testid="stFileUploader"]:hover {
    border-color: var(--accent) !important;
    background: var(--accent-soft) !important;
}

div[data-testid="stChatInput"] {
    background: transparent !important;
}
div[data-testid="stChatInput"] textarea {
    background: rgba(255, 255, 255, 0.04) !important;
    backdrop-filter: blur(20px) !important;
    border: 1px solid var(--glass-border) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--text-primary) !important;
    font-size: 0.88rem !important;
    padding: 0.75rem 1rem !important;
    transition: var(--transition) !important;
}
div[data-testid="stChatInput"] textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 2px var(--accent-glow) !important;
}

.stButton > button {
    background: var(--accent-soft) !important;
    color: #C4B5FD !important;
    border: 1px solid rgba(124, 106, 255, 0.2) !important;
    border-radius: var(--radius-sm) !important;
    font-weight: 500 !important;
    font-size: 0.8rem !important;
    padding: 0.5rem 1.2rem !important;
    transition: var(--transition) !important;
}
.stButton > button:hover {
    background: rgba(124, 106, 255, 0.22) !important;
    border-color: var(--accent) !important;
    box-shadow: 0 4px 16px var(--accent-glow) !important;
    transform: translateY(-1px) !important;
}

.stSpinner > div { border-top-color: var(--accent) !important; }

::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.08); border-radius: 10px; }
::-webkit-scrollbar-thumb:hover { background: rgba(255,255,255,0.15); }

@keyframes slideInRight {
    from { opacity: 0; transform: translateX(20px); }
    to   { opacity: 1; transform: translateX(0); }
}
@keyframes slideInLeft {
    from { opacity: 0; transform: translateX(-20px); }
    to   { opacity: 1; transform: translateX(0); }
}
@keyframes bounce {
    0%, 60%, 100% { transform: translateY(0); }
    30% { transform: translateY(-4px); }
}
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to   { opacity: 1; transform: translateY(0); }
}
.fade-in { animation: fadeIn 0.5s ease-out; }

hr {
    border: none !important;
    border-top: 1px solid var(--glass-border) !important;
    margin: 1rem 0 !important;
}

.sidebar-brand {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    padding: 0.5rem 0 1rem;
}
.sidebar-brand-icon {
    font-size: 1.6rem;
    filter: drop-shadow(0 0 8px var(--accent-glow));
}
.sidebar-brand-text {
    font-size: 1.1rem;
    font-weight: 700;
    color: var(--text-primary);
    letter-spacing: -0.02em;
}
.sidebar-brand-tag {
    font-size: 0.55rem;
    color: var(--accent);
    text-transform: uppercase;
    letter-spacing: 0.1em;
    font-weight: 600;
}

.status-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    font-size: 0.7rem;
    font-weight: 500;
    padding: 0.3rem 0.7rem;
    border-radius: 100px;
    letter-spacing: 0.02em;
}
.status-ready {
    background: rgba(52, 211, 153, 0.1);
    color: var(--success);
    border: 1px solid rgba(52, 211, 153, 0.2);
}
.status-waiting {
    background: rgba(251, 191, 36, 0.1);
    color: var(--warning);
    border: 1px solid rgba(251, 191, 36, 0.2);
}

.stAlert {
    background: var(--glass-bg) !important;
    border: 1px solid var(--glass-border) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--text-secondary) !important;
}

details {
    background: var(--glass-bg) !important;
    border: 1px solid var(--glass-border) !important;
    border-radius: var(--radius-sm) !important;
}
details summary {
    color: var(--text-secondary) !important;
    font-size: 0.82rem !important;
}

div[data-testid="stToast"] {
    background: var(--surface-card) !important;
    backdrop-filter: blur(20px) !important;
    border: 1px solid var(--glass-border) !important;
    border-radius: var(--radius-sm) !important;
}
</style>
""", unsafe_allow_html=True)


if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None
if "rag_chain" not in st.session_state:
    st.session_state.rag_chain = None
if "pdf_name" not in st.session_state:
    st.session_state.pdf_name = None
if "pdf_pages" not in st.session_state:
    st.session_state.pdf_pages = 0
if "pdf_chunks" not in st.session_state:
    st.session_state.pdf_chunks = 0
if "processed" not in st.session_state:
    st.session_state.processed = False



def get_api_key():
    """Get API key from secrets or environment."""
    try:
        return st.secrets["GOOGLE_API_KEY"]
    except Exception:
        key = os.environ.get("GOOGLE_API_KEY")
        if key:
            return key
        return None


def process_pdf(uploaded_file, api_key):
    """Load PDF, split text, build FAISS index with rate-limit-safe batching."""
    import time
    from langchain_community.document_loaders import PyPDFLoader
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    from langchain_google_genai import GoogleGenerativeAIEmbeddings
    from langchain_community.vectorstores import FAISS

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    try:
        loader = PyPDFLoader(tmp_path)
        pages = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=80,
            separators=["\n\n", "\n", ". ", " ", ""],
        )
        docs = text_splitter.split_documents(pages)

        embeddings = GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-001",
            google_api_key=api_key,
        )

        BATCH_SIZE = 5
        DELAY_BETWEEN_BATCHES = 1.5  # seconds
        MAX_RETRIES = 3

        vectorstore = None
        progress = st.progress(0, text="Embedding document chunks...")

        for i in range(0, len(docs), BATCH_SIZE):
            batch = docs[i : i + BATCH_SIZE]
            pct = min((i + BATCH_SIZE) / len(docs), 1.0)
            progress.progress(pct, text=f"Embedding chunks {i+1}–{min(i+BATCH_SIZE, len(docs))} of {len(docs)}...")

            for attempt in range(MAX_RETRIES):
                try:
                    if vectorstore is None:
                        vectorstore = FAISS.from_documents(batch, embeddings)
                    else:
                        vectorstore.add_documents(batch)
                    break
                except Exception as e:
                    if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                        wait = 2 ** (attempt + 1)
                        progress.progress(pct, text=f"Rate limited — waiting {wait}s before retry...")
                        time.sleep(wait)
                    else:
                        raise

            if i + BATCH_SIZE < len(docs):
                time.sleep(DELAY_BETWEEN_BATCHES)

        progress.empty()
        return vectorstore, len(pages), len(docs)
    finally:
        os.unlink(tmp_path)


def build_rag_chain(vectorstore, api_key):
    """Build the RAG chain with a rich prompt template using LCEL."""
    from langchain_google_genai import ChatGoogleGenerativeAI
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.runnables import RunnablePassthrough
    from langchain_core.output_parsers import StrOutputParser

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=api_key,
        temperature=0.3,
    )

    prompt = ChatPromptTemplate.from_template(
        "You are a brilliant, articulate AI assistant specialized in understanding "
        "and analyzing PDF documents. You answer questions based ONLY on the provided "
        "context. If the context doesn't contain enough information, say so honestly.\n\n"
        "Guidelines:\n"
        "• Be precise and cite specific parts of the document when possible\n"
        "• Use bullet points or numbered lists for clarity when appropriate\n"
        "• If asked for a summary, be thorough but concise\n"
        "• Format your response with proper markdown for readability\n\n"
        "───── DOCUMENT CONTEXT ─────\n{context}\n"
        "────────────────────────────\n\n"
        "Question: {input}\n\n"
        "Answer:"
    )

    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 5},
    )

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    rag_chain = (
        {"context": retriever | format_docs, "input": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    class RAGWrapper:
        def __init__(self, chain):
            self.chain = chain
        def invoke(self, inputs):
            return {"answer": self.chain.invoke(inputs["input"])}

    return RAGWrapper(rag_chain)


with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <span class="sidebar-brand-icon">✦</span>
        <div>
            <div class="sidebar-brand-text">AskMyPDF</div>
            <div class="sidebar-brand-tag">AI Document Intelligence</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    if st.session_state.processed:
        st.markdown(
            '<span class="status-badge status-ready">● Document Ready</span>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<span class="status-badge status-waiting">○ Awaiting Document</span>',
            unsafe_allow_html=True,
        )

    st.markdown("")

    uploaded_file = st.file_uploader(
        "Upload your PDF",
        type="pdf",
        help="Supports any PDF up to 50 MB",
        label_visibility="visible",
    )

    api_key = get_api_key()

    if uploaded_file is not None:
        file_changed = (st.session_state.pdf_name != uploaded_file.name)

        if file_changed or not st.session_state.processed:
            if not api_key:
                st.error("⚠ API key not found. Add `GOOGLE_API_KEY` to `.streamlit/secrets.toml`.")
            else:
                with st.spinner("Analyzing document..."):
                    try:
                        vectorstore, n_pages, n_chunks = process_pdf(uploaded_file, api_key)
                        rag_chain = build_rag_chain(vectorstore, api_key)

                        st.session_state.vectorstore = vectorstore
                        st.session_state.rag_chain = rag_chain
                        st.session_state.pdf_name = uploaded_file.name
                        st.session_state.pdf_pages = n_pages
                        st.session_state.pdf_chunks = n_chunks
                        st.session_state.processed = True
                        st.session_state.chat_history = []

                        st.toast("✦ Document processed successfully!", icon="✅")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Failed to process PDF: {str(e)}")

    if st.session_state.processed:
        st.markdown("---")
        st.markdown(f"""
        <div class="glass-card" style="padding: 1rem;">
            <div style="font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.08em;
                        color: var(--text-muted); margin-bottom: 0.6rem; font-weight: 600;">
                Document Info
            </div>
            <div style="font-size: 0.82rem; color: var(--text-primary); margin-bottom: 0.5rem;
                        word-break: break-all;">
                📄 {st.session_state.pdf_name}
            </div>
            <div class="stat-row">
                <span class="stat-pill">{st.session_state.pdf_pages} pages</span>
                <span class="stat-pill">{st.session_state.pdf_chunks} chunks</span>
                <span class="stat-pill">{len(st.session_state.chat_history) // 2} chats</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    if st.session_state.chat_history:
        st.markdown("")
        if st.button("🗑  Clear Chat History", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()

    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 0.5rem 0;">
        <div style="font-size: 0.65rem; color: var(--text-muted); line-height: 1.6;">
            Powered by <strong style="color: var(--accent);">Gemini</strong> ×
            <strong style="color: var(--accent);">LangChain</strong><br>
            Built with ♥
        </div>
    </div>
    """, unsafe_allow_html=True)


st.markdown("""
<div class="fade-in">
    <div class="hero-title">AskMyPDF</div>
    <div class="hero-sub">Upload a document. Ask anything. Get intelligent answers.</div>
</div>
""", unsafe_allow_html=True)

st.markdown("")

if not st.session_state.processed:
    st.markdown("""
    <div class="welcome-card fade-in">
        <div class="welcome-icon">📑</div>
        <div class="welcome-title">No document loaded yet</div>
        <div class="welcome-text">
            Upload a PDF from the sidebar to begin.<br>
            I'll analyze every page, build a smart index, and you can
            have a conversation with your document.
        </div>
        <div class="chip-row" style="margin-top: 1.5rem;">
            <span class="chip">📊 Research Papers</span>
            <span class="chip">📋 Reports</span>
            <span class="chip">📖 Textbooks</span>
            <span class="chip">📝 Legal Docs</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

else:
    def set_query(q):
        st.session_state.suggested_query = q

    if "suggested_query" not in st.session_state:
        st.session_state.suggested_query = None

    if not st.session_state.chat_history:
        st.markdown(f"""
        <div class="welcome-card fade-in" style="margin-bottom: 0.5rem;">
            <div class="welcome-icon">💬</div>
            <div class="welcome-title">Ready to chat with your document</div>
            <div class="welcome-text">
                <strong>{st.session_state.pdf_name}</strong> is loaded and indexed.
                Ask me anything about it!
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<div style='text-align: center; margin-bottom: 1rem; color: var(--text-muted); font-size: 0.8rem;'>Suggestions</div>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            st.button("📝 Summarize the document", on_click=set_query, args=("Summarize the document",), use_container_width=True)
        with col2:
            st.button("🔍 Key findings", on_click=set_query, args=("What are the key findings?",), use_container_width=True)
        with col3:
            st.button("❓ What is the main topic?", on_click=set_query, args=("What is the main topic discussed in this document?",), use_container_width=True)

    for msg in st.session_state.chat_history:
        role = msg["role"]
        content = msg["content"]
        timestamp = msg.get("time", "")

        if role == "user":
            st.markdown(f"""
            <div class="chat-user">
                <div class="chat-label">You</div>
                {content}
                <div class="chat-time">{timestamp}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="chat-assistant">
                <div class="chat-label">AskMyPDF</div>
                {content}
                <div class="chat-time">{timestamp}</div>
            </div>
            """, unsafe_allow_html=True)

    query = st.chat_input("Ask anything about your document...")

    active_query = query or st.session_state.suggested_query

    if active_query:
        st.session_state.suggested_query = None

        now = datetime.now().strftime("%I:%M %p")

        st.session_state.chat_history.append({
            "role": "user",
            "content": active_query,
            "time": now,
        })

        st.markdown(f"""
        <div class="chat-user">
            <div class="chat-label">You</div>
            {active_query}
            <div class="chat-time">{now}</div>
        </div>
        """, unsafe_allow_html=True)

        with st.spinner(""):
            st.markdown("""
            <div class="typing-indicator">
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
            </div>
            """, unsafe_allow_html=True)

            try:
                response = st.session_state.rag_chain.invoke({"input": active_query})
                answer = response["answer"]
            except Exception as e:
                answer = f"⚠ Something went wrong: {str(e)}"

        st.session_state.chat_history.append({
            "role": "assistant",
            "content": answer,
            "time": datetime.now().strftime("%I:%M %p"),
        })

        st.rerun()
