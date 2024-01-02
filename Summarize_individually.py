import streamlit as st
import os
from dotenv import load_dotenv
load_dotenv()

from paperreader.models.controller import Controller

st.set_page_config(
    page_title="Article summarizer",
    layout="wide",
)

st.session_state.setdefault("controller", Controller())
st.session_state.setdefault("article_uploader_version", 0)

st.title("Article summarizer")

def render_upload_articles():
    controller = st.session_state.controller
    uploaded_articles = st.file_uploader(
        label="Upload one or more files",
        accept_multiple_files=True,
        key=f"article_uploader_{st.session_state.article_uploader_version}",
        type=["pdf"]
    )

    if uploaded_articles:
        st.session_state.article_uploader_version += 1

        for i, uploaded_file in enumerate(uploaded_articles):
            bytes_data = uploaded_file.read()
            _, suffix = os.path.splitext(uploaded_file.name)
            controller.add_article_from_bytes(
                bytes_data=bytes_data,
                filetype=suffix,
                title=uploaded_file.name
            )
        
        with st.spinner("Summarizing articles..."):
            controller.summarize_articles(overwrite=False)
        st.rerun()


controller = st.session_state.controller
if len(controller.articles) == 0:
    render_upload_articles()
else:
    tabs = st.tabs(
        ["Add new article(s)"] +
        [f"Article {i+1}" for i in range(len(controller.articles))]
    )
    with tabs[0]:
        render_upload_articles()

    article_tabs = tabs[1:]
    for article_tab, article in zip(article_tabs, controller.articles):
        with article_tab:
            if article.is_summarized():
                st.markdown(f"## {article.summaries_obj.title}")
                st.markdown(f"### Very brief summary")
                st.write(article.summaries_obj.summary_brief)
                st.markdown(f"### Brief summary")
                st.write(article.summaries_obj.summary)
                st.markdown(f"### Long summary")
                st.write(article.summaries_obj.summary_long)
            else:
                summarize_button = st.button(label="Summarize article")
                if summarize_button:
                    with st.spinner("Summarizing article..."):
                        article.summarize()
                    st.rerun()
