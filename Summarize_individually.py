import streamlit as st
import os

from paperreader.models.controller import Controller

st.set_page_config(
    page_title="Article summarizer",
    layout="wide",
)

st.session_state.setdefault("controller", Controller())

st.title("Article summarizer")

def render_upload_articles():
    controller = st.session_state.controller
    with st.form("my-form", clear_on_submit=True):
        uploaded_articles = st.file_uploader(
            label="Upload one or more files",
            accept_multiple_files=True,
            key="article_uploader"
        )
        st.write(uploaded_articles)
        submitted = st.form_submit_button(
            "Add new uploaded articles",
            disabled=False
        )

        if submitted:
            for i, uploaded_file in enumerate(uploaded_articles):
                bytes_data = uploaded_file.read()
                _, suffix = os.path.splitext(uploaded_file.name)
                controller.add_article_from_bytes(
                    bytes_data=bytes_data,
                    filetype=suffix,
                    title=uploaded_file.name
                )

                with st.spinner('Summarizing article...'):
                    article = controller.articles[i]
                    if not article.is_summarized():
                        article.summarize()


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
            st.markdown(f"## {article.title}")
            st.write(article.summary)
