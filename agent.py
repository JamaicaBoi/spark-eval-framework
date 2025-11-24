from langchain.agents import create_agent,AgentState
from langchain.tools import tool
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

from dotenv import load_dotenv
from pydantic import BaseModel
load_dotenv()

import sys, datetime, json
from pathlib import Path



project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from config import (
    EVAL_LEARNER_BG_PROMPT,
    EVAL_LEARNER_BG_OUTPUT,
    EVAL_KNOWLEDGE_DOMAIN_PROMPT,
    LEARNER_BG_SYSTEM_PROMPT,
    KNOWLEDGE_DOMAIN_SYSTEM_PROMPT,
    EVAL_KNOWLEDGE_DOMAIN_OUTPUT
)
from utility.web_search_tool import tavily_search

llm = ChatOpenAI(
    model="gpt-5-mini",
    temperature=0.1,
)

tools = [tavily_search]
tool_instruction = "There is a tool that you can decide to use while the assessing process. include with: \n"
for idx,item in enumerate(tools):
    tool_instruction += f"{idx+1}. <{item.name}>: \n{item.description}\n"

learner_agent = create_agent(
    model=llm,
    system_prompt=LEARNER_BG_SYSTEM_PROMPT +'\n' + tool_instruction,
    tools=tools,
    response_format = EVAL_LEARNER_BG_OUTPUT,
    name='learner_agent'
)

knowledge_bg_agent = create_agent(
    model=llm,
    system_prompt=KNOWLEDGE_DOMAIN_SYSTEM_PROMPT +'\n' + tool_instruction,
    tools=tools,
    response_format = EVAL_KNOWLEDGE_DOMAIN_OUTPUT,
    name='knowledge_bg_agent'
)