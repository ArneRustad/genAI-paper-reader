import tempfile
import os

from pydantic.v1 import BaseModel, Field
from typing import List

from paperreader.llm import chat_model_gpt_4_turbo as llm
# from langchain.prompts import PromptTemplate
from langchain.document_loaders import PyMuPDFLoader

from paperreader.chains.summarize_article import (
    chain as summarize_article_chain
)

class Article(BaseModel):
    title: str = Field(default=None)
    documents: List = Field(default=None)
    summary: str = Field(default=None)
    
    @classmethod
    def from_bytes(
        cls,
        bytes_data,
        filetype,
        title=None,
    ):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = os.path.join(temp_dir, f"temp.{filetype}")
            with open(temp_path, mode="wb") as f:
                f.write(bytes_data)

            loader = PyMuPDFLoader(temp_path)

            article = cls(
                documents=loader.load(),
                title=title
            )
            return article
            
    
    def summarize(self):
        # prompt_template = PromptTemplate.from_template(
        #     'Please summarize this article.\n\nArticle:""""{article}\n\nSummary:"""'
        # )
        article = "\n\n".join(
            [f"## Page {i+1}\n"+ doc.page_content for i, doc in enumerate(self.documents)]
        )
        # self.summary = llm.predict(prompt_template.format(article=article))
        self.summary = summarize_article_chain.invoke(
            article
        )
    
    def is_summarized(self):
        return self.summary is not None


class Controller(BaseModel):
    articles: List[Article] = Field(default_factory=list)

    def add_article(self, article):
        self.articles.append(article)
    
    def add_article_from_bytes(
        self,
        **kwargs
    ):
        article = Article.from_bytes(**kwargs)
        self.add_article(article)
