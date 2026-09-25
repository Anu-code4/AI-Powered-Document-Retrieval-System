from pathlib import Path

import requests
import streamlit as st

API_URL = "http://127.0.0.1:8000"


def show_confidence(confidence):
    if confidence is None:
        return
    if confidence >= 0.80:
        st.success(f"🟢 High Confidence ({confidence:.2f})")
    elif confidence >= 0.50:
        st.warning(f"🟡 Medium Confidence ({confidence:.2f})")
    else:
        st.error(f"🔴 Low Confidence ({confidence:.2f})")


def show_sources(sources):
    if not sources:
        return
    st.markdown("##### 📚 Sources")
    for source in sources:
        st.markdown(f"- `{source}`")


st.set_page_config(
    page_title="AI-Powered Document Retrieval System",
    page_icon="🤖",
    layout="wide",
)

css = Path(__file__).parent / "styles.css"
if css.exists():
    st.markdown(f"<style>{css.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)

st.session_state.setdefault("messages", [])

with st.sidebar:
    st.title("🤖 AI-Powered Document Retrieval System")
    st.caption("Production RAG Assistant")
    st.divider()

    files = st.file_uploader(
        "📂 Upload PDF / DOCX",
        type=["pdf", "docx"],
        accept_multiple_files=True,
    )

    if st.button("📤 Upload & Index"):
        if not files:
            st.warning("Please select at least one document.")
        else:
            payload = [("files", (f.name, f.getvalue(), f.type)) for f in files]
            with st.spinner("📤 Uploading & Indexing Documents..."):
                r = requests.post(f"{API_URL}/upload", files=payload, timeout=300)
            if r.ok:
                st.toast("Documents indexed successfully! 🎉")
                st.success("Documents indexed successfully.")
                st.balloons()
            else:
                st.error(r.text)

    st.divider()

    if st.button("🗑 Clear Chat"):
        st.session_state.messages = []
        st.rerun()

col1, col2 = st.columns([8, 2])
with col1:
    st.title("🤖 AI-Powered Document Retrieval System")
    st.caption("Intelligent Document Assistant")
with col2:
    st.success("🟢 Ready")

st.divider()

try:
    docs = requests.get(f"{API_URL}/documents", timeout=30).json()
    if docs:
        st.subheader("📂 Indexed Documents")
        for doc in docs:
            c1, c2 = st.columns([5, 1])
            with c1:
                icon = "📝" if doc["type"] == "DOCX" else "📄"
                st.write(f"{icon} **{doc['filename']}**")
                st.caption(f"{doc['size_kb']} KB")
            with c2:
                if st.button("🗑", key=doc["filename"]):
                    if requests.delete(f"{API_URL}/documents/{doc['filename']}", timeout=300).ok:
                        st.toast("Document deleted.")
                        st.rerun()
except Exception:
    st.caption("Unable to load documents.")

if not st.session_state.messages:
    st.info(
        "### 👋 Welcome\n\n1. Upload PDF/DOCX documents.\n2. Click Upload & Index.\n3. Ask questions about your documents."
    )

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message["role"] == "assistant":
            show_confidence(message.get("confidence"))
            show_sources(message.get("sources", []))

if prompt := st.chat_input("Ask anything about your documents..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            with st.spinner("🧠 Generating answer..."):
                data = requests.post(
                    f"{API_URL}/chat",
                    json={"question": prompt},
                    timeout=120,
                ).json()
            answer = data.get("answer", "No answer returned.")
            confidence = data.get("confidence")
            sources = data.get("sources", [])
        except Exception as e:
            answer, confidence, sources = f"❌ {e}", None, []

        st.markdown(answer)
        show_confidence(confidence)
        show_sources(sources)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
            "confidence": confidence,
            "sources": sources,
        }
    )

st.divider()
st.caption("🚀 AI-Powered Document Retrieval System | FastAPI • Streamlit • Hybrid RAG • CrossEncoder • BM25 • FAISS")