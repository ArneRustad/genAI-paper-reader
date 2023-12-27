from langchain.schema.runnable import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from paperreader.utils.prompts import prompt_template_from_name
from paperreader.llm import chat_model_gpt_4_turbo as llm

prompt_template = prompt_template_from_name("SummarizeBriefly")

chain = (
    {"article": RunnablePassthrough()}
    | prompt_template
    | llm
    | StrOutputParser()
)
