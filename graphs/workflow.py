import os
from langfuse.langchain import CallbackHandler
from typing import TypedDict, Literal
from langgraph.graph import StateGraph, END, START
from langgraph.checkpoint.memory import MemorySaver
from .states import MCState
from .nodes import (methodcomp_claims_extraction,
                    methodcomp_claims_verification,
                    calculate_factualness_score)
from .configuration import GraphConfig

def method_component_factual_evaluation():
    workflow = StateGraph(MCState, config_schema=GraphConfig)
    workflow.add_node(methodcomp_claims_extraction)
    workflow.add_node(methodcomp_claims_verification)
    workflow.add_node(calculate_factualness_score)

    workflow.add_edge(START, "methodcomp_claims_extraction")
    workflow.add_edge("methodcomp_claims_extraction","methodcomp_claims_verification")
    workflow.add_edge("methodcomp_claims_verification", "calculate_factualness_score")
    workflow.add_edge("calculate_factualness_score",END)

    if os.environ.get("LANGFUSE_TRACING") == "true":
        langfuse_handler = CallbackHandler()
        return workflow.compile().with_config({"callbacks": [langfuse_handler]})
    else:
        return workflow.compile().with_config({"callbacks": []})