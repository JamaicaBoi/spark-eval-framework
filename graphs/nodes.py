from re import split
from langchain_core.runnables.config import RunnableConfig
from langgraph.types import Command
from typing import TypedDict, Literal
from langchain_core.messages import RemoveMessage
import os,json,datetime

from config import EVAL_COMPETENCY_WEIGHT, EVAL_WHOISTHISFOR_WEIGHT
from utility.web_search_tool import brave_search,jina_reader_fetch
from graphs.states import MCState
from graphs.chains import (
    get_claims_extraction_chain,
    get_claims_verification_chain,
    get_competency_feedback_chain,
    get_knowledge_background_feedback_chain,
    get_learner_background_feedback_chain,
    get_whoisthisfor_feedback_chain
)

async def methodcomp_claims_extraction(mc_state: MCState, config: RunnableConfig) -> MCState:
    extraction_chain = get_claims_extraction_chain(config)
    method_comp = mc_state['micro_credentials']['method_component']['components']
    ref = mc_state['micro_credentials']['method_component']['reference']

    result = await extraction_chain.ainvoke({"method component": method_comp, "reference": ref})
    claims = result["claims"]
    for claim in claims:
        claim.setdefault("support", "no")

    # write the claims into the eval_score portion of the state
    mc_state['eval_score'] = {"claims": claims}
    return mc_state

async def methodcomp_claims_verification(mc_state: MCState, config: RunnableConfig) -> MCState:
    verification_chain = get_claims_verification_chain(config)
    claims = mc_state['eval_score']['claims']
    grouped = {}
    for claim in claims:
        src = claim["source"]
        if src not in grouped:
            grouped[src] = []
        grouped[src].append(claim)

    for source in grouped.keys():
        if source == '':
            continue
        web_url = brave_search(source,limit=1)
        ref_content = jina_reader_fetch(web_url[0]['link'])
        result = await verification_chain.ainvoke({"ref content": ref_content, "claims": grouped[source]})
        verified_claims = result['verifications']
        for verified_claim in verified_claims:
            item = next((x for x in claims if x["id"] == verified_claim["id"]), None)
            if item:
                item["support"] = verified_claim["result"]

    mc_state['eval_score'] = {"claims": claims}
    return mc_state


async def calculate_factualness_score(mc_state: MCState, config: RunnableConfig) -> MCState:
    claims = mc_state['eval_score']['claims']
    count_with_source = sum(1 for item in claims if item["source"] != '')
    count_support = sum(1 for item in claims if item["support"] == "yes")
    count_claims = len(claims)
    try:
        groundness_score = count_with_source/count_claims
    except:
        groundness_score = 0.0
    try:
        faithfulness_score = count_support/count_with_source
    except:
        faithfulness_score = 0.0
    
    mc_state['eval_score'] = {"claims": claims, "method_faithfulness_score": faithfulness_score, "method_groundness_score": groundness_score}

    result = {
        "claims": claims,
        "groundness_score": mc_state.get('eval_score')['method_groundness_score'],
        "faithfulness_score": mc_state.get('eval_score')['method_faithfulness_score'],
        "method_component": mc_state.get('micro_credentials')['method_component']['components'],
        "reference": mc_state.get('micro_credentials')['method_component']['reference']
    }

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"result/{timestamp}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4, ensure_ascii=False)

    return mc_state

async def learner_background_feedback(mc_state: MCState, config: RunnableConfig) -> dict:
    feedback_chain = get_learner_background_feedback_chain(config)
    feedback = await feedback_chain.ainvoke({"learner background": mc_state["learner_background"]})
    mc_state["eval_score"]["dim_feedback"] = {'artifact': 'learner_bg', 'feedback':feedback}
    return mc_state

async def knowledge_background_feedback(mc_state: MCState, config: RunnableConfig) -> dict:
    feedback_chain = get_knowledge_background_feedback_chain(config)
    feedback = await feedback_chain.ainvoke({"teaching domain": mc_state["knowledge_background"]})
    mc_state["eval_score"]["dim_feedback"] = {'artifact': 'knowledge_bg', 'feedback':feedback}
    return mc_state

async def whoisthisfor_feedback(mc_state: MCState, config: RunnableConfig) -> dict:
    feedback_chain = get_whoisthisfor_feedback_chain(config)
    feedback = await feedback_chain.ainvoke({"who is this for": mc_state["micro_credentials"]["whoisthisfor_statement"]})
    mc_state["eval_score"]["dim_feedback"] = {'artifact': 'whoisthisfor', 'feedback':feedback}
    return mc_state

async def competency_feedback(mc_state: MCState, config: RunnableConfig) -> MCState:
    feedback_chain = get_competency_feedback_chain(config)
    feedback = await feedback_chain.ainvoke({
        "who is this for": mc_state["micro_credentials"]["whoisthisfor_statement"],
        "competency": mc_state["micro_credentials"]["competency_statement"]})
    mc_state["eval_score"]["dim_feedback"] = {'artifact': 'competency', 'feedback':feedback}
    return mc_state

async def calculate_dimension_weight(mc_state: MCState, config: RunnableConfig):
    artifact_name = mc_state['eval_score']['dim_feedback']['artifact']
    artifact_feedback = mc_state['eval_score']['dim_feedback']['feedback']
    if artifact_name == "whoisthisfor":
        weight = EVAL_WHOISTHISFOR_WEIGHT
    elif artifact_name == "competency":
        weight = EVAL_COMPETENCY_WEIGHT
    
    total_score = 0
    total_weight = 0
    dimension_result = []
    for dimension in weight.keys():
        total_score += int(artifact_feedback[dimension]) * weight[dimension]
        total_weight += weight[dimension]
        dimension_result.append(
            {
                "dimension": "_".join(dimension.split("_")[:-1]),
                "result": artifact_feedback[dimension],
                "explanation": artifact_feedback["_".join(dimension.split("_")[:-1])+"_explanation"]
            }
        )

    total_score = (total_score/total_weight) * 10
    mc_state["eval_score"]['dim_feedback'] = {
        'total_score': total_score,
        'feedback': dimension_result,
        'artifact': artifact_name
    }
    return mc_state

