import streamlit as st
from crawler import extract_text_from_url
from processor import chunk_text
from vector_store import get_vector_store
from qa_chain import create_qa_chain

st.set_page_config(page_title="AI Website Chatbot")
st.title("AI-Powered Website Chatbot")

url = st.text_input("Enter Website URL")

if st.button("Index Website"):
    with st.spinner("Crawling website..."):
        data, error = extract_text_from_url(url)
        if error:
            st.error(error)
        else:
            docs = chunk_text(data["text"], {"source": url, "title": data["title"]})
            vector_store = get_vector_store(docs)
            vector_store.persist()
            st.success("Website indexed successfully")

if "qa_chain" not in st.session_state:
    try:
        vector_store = get_vector_store()
        st.session_state.qa_chain = create_qa_chain(vector_store)
    except:
        st.warning("Please index a website first")

query = st.chat_input("Ask a question")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = ""

if query and "qa_chain" in st.session_state:
    answer = st.session_state.qa_chain(
        query,
        st.session_state.chat_history
    )
    st.session_state.chat_history += f"\nUser: {query}\nAI: {answer}\n"
    st.chat_message("assistant").write(answer)
