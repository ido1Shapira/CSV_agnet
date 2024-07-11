import os
from typing import List

import pandas as pd
from dotenv import load_dotenv
from langchain.agents import AgentExecutor
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from langchain_experimental.agents.agent_toolkits.pandas.base import create_pandas_dataframe_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel

from src.agent.prompt import get_prompt

# Setting up the api key
load_dotenv()
API_KEY: str | None = os.environ.get('GOOGLE_API_KEY', None)


class AgentInput(BaseModel):
    input: str
    chat_history: List[BaseMessage]


class Agent:
    def __init__(self,
                 filename: str,
                 temperature: float = 0.5,
                 model_name: str = 'gemini-1.5-flash'):
        llm_chat = ChatGoogleGenerativeAI(temperature=temperature,
                                          google_api_key=API_KEY,
                                          model=model_name)
        df = pd.read_csv(filename)
        self.chat_history = []
        self.agent_executor: AgentExecutor = create_pandas_dataframe_agent(llm_chat, df,
                                                                           allow_dangerous_code=True,
                                                                           verbose=True)

    def run(self, user_input: str) -> str:
        agent_input = {
            "input": get_prompt(user_input),
            "chat_history": self.chat_history
        }
        response = self.agent_executor.invoke(agent_input)
        agent_output = response["output"]
        self.chat_history.extend(
            [
                HumanMessage(content=user_input),
                AIMessage(content=agent_output),
            ])
        return agent_output
