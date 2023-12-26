import streamlit as st
import tempfile
import os

from paperreader.llm import chat_model_gpt_4_turbo as llm
from langchain.prompts import PromptTemplate
from langchain.document_loaders import PyMuPDFLoader

st.set_page_config(
    page_title="Article summarizer",
    layout="wide",
)

st.title("Article summarizer")

uploaded_articles = st.file_uploader(
    label="Upload one or more files",
    accept_multiple_files=True,
    key="article_uploader")

if uploaded_articles:
    for i, uploaded_file in enumerate(uploaded_articles):
        bytes_data = uploaded_file.read()
        with tempfile.TemporaryDirectory() as temp_dir:
            _, suffix = os.path.splitext(uploaded_file.name)
            temp_path = os.path.join(temp_dir, f"temp{suffix}")
            with open(temp_path, mode="wb") as f:
                f.write(bytes_data)
        
            prompt_template = PromptTemplate.from_template(
                'Please summarize this article.\n\nArticle:""""{article}\n\nSummary:"""'
            )
            loader = PyMuPDFLoader(temp_path)
            docs = loader.load()
            article = "\n\n".join([f"## Page {i+1}\n"+ doc.page_content for i, doc in enumerate(docs)])
            st.markdown(f"# Article {i+1}: {uploaded_file.name}")
            with st.spinner('Summarizing article...'):
                summary = llm.predict(prompt_template.format(article=article))
                st.write(summary)
