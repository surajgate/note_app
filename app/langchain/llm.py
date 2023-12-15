from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.agents.agent_types import AgentType
from langchain.llms.openai import OpenAI
from langchain.sql_database import SQLDatabase
import os
import time
# openai_api_key : str = "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"
openai_api_key = os.environ.get("OPENAI_API_KEY")
print(openai_api_key)
if not openai_api_key:
    raise ValueError(
        "OpenAI API key is not provided. Set the OPENAI_API_KEY environment variable.")

db = SQLDatabase.from_uri("postgresql://postgres:root@localhost/pms_db"
                          )
toolkit = SQLDatabaseToolkit(db=db, llm=OpenAI(temperature=0))

agent_executor = create_sql_agent(
    llm=OpenAI(
        api_key=openai_api_key, temperature=0),
    toolkit=toolkit,
    verbose=True,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
)


def llm_question_response(question: str):
    print(question)
    time.sleep(20)
    response = agent_executor.run(f"{question}")
    return response
