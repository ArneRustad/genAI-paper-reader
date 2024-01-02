import tempfile
import os

from pydantic.v1 import BaseModel, Field
from typing import List

from paperreader.llm import chat_model_gpt_4_turbo as llm
# from langchain.prompts import PromptTemplate
from langchain.document_loaders import PyMuPDFLoader

from paperreader.chains.summarize_article import (
    chain as summarize_article_chain,
    SummariesExtractionSchema,
)

class Article(BaseModel):
    title: str = Field(default=None)
    documents: List = Field(default=None)
    summaries_obj: SummariesExtractionSchema = Field(default=None)
    
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
    
    def to_markdown(self):
        text = "# Article"
        text += "\n\n".join(
            [f"## Page {i+1}\n"+ doc.page_content for i, doc in enumerate(self.documents)]
        )
        return text
            
    
    def summarize(self):
        self.summaries_obj = summarize_article_chain.invoke(
            self.to_markdown()
        )
    
    def is_summarized(self):
        return self.summaries_obj is not None


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
    
    def _summarize_articles(self, article_indices):
        articles = [self.articles[i] for i in article_indices]
        texts = [article.to_markdown() for article in articles]
        summaries_objects = summarize_article_chain.batch(texts)
        for article, summaries_obj in zip(articles, summaries_objects):
            article.summaries_obj = summaries_obj
    
    def summarize_articles(self, overwrite=False):
        if overwrite:
            article_indices = range(len(self.articles))
        else:
            article_indices = [
                i for i, article in enumerate(self.articles)
                if not article.is_summarized()
            ]
        self._summarize_articles(article_indices=article_indices)