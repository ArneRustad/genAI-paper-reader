
import os
from dotenv import load_dotenv
load_dotenv()

# Defining different callbacks for LLM
from langchain.chat_models import ChatOpenAI

# Initializing LLM with callbacks
base_chat_model = llm = ChatOpenAI(
    temperature=0,
    model=os.environ["OPENAI_API_MODEL_GPT4"]
)

chat_model_gpt_4_turbo = llm = ChatOpenAI(
    temperature=0,
    model=os.environ["OPENAI_API_MODEL_GPT4_TURBO"]
)
