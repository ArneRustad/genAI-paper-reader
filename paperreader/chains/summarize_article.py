from langchain.schema.runnable import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain.utils.openai_functions import convert_pydantic_to_openai_function  # noqa E501
from langchain.output_parsers.openai_functions import PydanticOutputFunctionsParser  # noqa E501

from paperreader.utils.prompts import prompt_template_from_name
from paperreader.llm import chat_model_gpt_4_turbo as llm

from pydantic.v1 import BaseModel, Field

class SummariesExtractionSchema(BaseModel):
    """Schema for the summaries extraction."""
    title: str = Field(
        description="Title of article"
    )
    summary_brief: str = Field(
        description="Summarize the article in maximum three sentences."
    )
    summary: str = Field(
        description="Summary of the article in two or three paragraphs."
    )
    summary_long: str = Field(
        description="A long summary of the article. Approximately 1-2 pages. For the main results, please include quantitative numbers."
    )

prompt_template = prompt_template_from_name("SummarizeBriefly")

functions = [convert_pydantic_to_openai_function(SummariesExtractionSchema)]  # noqa E501

chain = (
    {"article": RunnablePassthrough()}
    | prompt_template
    | llm.bind(
        functions=functions,
        function_call={"name": "SummariesExtractionSchema"}
    )
    | PydanticOutputFunctionsParser(
        pydantic_schema=SummariesExtractionSchema,
    )
)
