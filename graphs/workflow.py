import os
from langfuse.langchain import CallbackHandler
from typing import TypedDict, Literal
from langgraph.graph import StateGraph, END, START
from langgraph.checkpoint.memory import MemorySaver
from .states import MCState
from .nodes import (calculate_dimension_weight, competency_feedback, learner_background_feedback, methodcomp_claims_extraction,
                    methodcomp_claims_verification,
                    calculate_factualness_score, whoisthisfor_feedback)
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

def learner_background_feedback_graph():
    workflow = StateGraph(MCState, config_schema=GraphConfig)
    workflow.add_node(learner_background_feedback)

    workflow.add_edge(START, "learner_background_feedback")
    workflow.add_edge("learner_background_feedback",END)

    if os.environ.get("LANGFUSE_TRACING") == "true":
        langfuse_handler = CallbackHandler()
        return workflow.compile().with_config({"callbacks": [langfuse_handler]})
    else:
        return workflow.compile().with_config({"callbacks": []})

def artifact_feedback_graph(artifact:str):
    workflow = StateGraph(MCState, config_schema=GraphConfig)
    workflow.add_node(calculate_dimension_weight)

    if artifact == "whoisthisfor":
        artifact_node = "whoisthisfor_feedback"
        workflow.add_node(whoisthisfor_feedback)
    elif artifact == "competency":
        artifact_node = "competency_feedback"
        workflow.add_node(competency_feedback)
    else:
        print("error, wrong artifact selection")
        return None
        
    workflow.add_edge(START, artifact_node)
    workflow.add_edge(artifact_node, "calculate_dimension_weight")
    workflow.add_edge("calculate_dimension_weight",END)

    if os.environ.get("LANGFUSE_TRACING") == "true":
        langfuse_handler = CallbackHandler()
        return workflow.compile().with_config({"callbacks": [langfuse_handler]})
    else:
        return workflow.compile().with_config({"callbacks": []})
