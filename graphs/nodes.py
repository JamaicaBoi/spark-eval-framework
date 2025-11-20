from langchain_core.runnables.config import RunnableConfig
from langgraph.types import Command
from typing import TypedDict, Literal
from langchain_core.messages import RemoveMessage
import os,json,datetime

from utility.web_search_tool import brave_search,jina_reader_fetch
from graphs.states import MCState
from graphs.chains import (
    get_claims_extraction_chain,
    get_claims_verification_chain
)

def methodcomp_claims_extraction(mc_state: MCState, config: RunnableConfig) -> MCState:
    extraction_chain = get_claims_extraction_chain(config)
    method_comp = mc_state['micro_credentials']['method_component']['components']
    ref = mc_state['micro_credentials']['method_component']['reference']

    claims = extraction_chain.invoke({"method component": method_comp, "reference": ref})["claims"]
    for claim in claims:
        claim.setdefault("support", "no")

    # write the claims into the eval_score portion of the state
    mc_state['eval_score'] = {"claims": claims}
    return mc_state

def methodcomp_claims_verification(mc_state: MCState, config: RunnableConfig) -> MCState:
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
        verified_claims = verification_chain.invoke({"ref content": ref_content, "claims": grouped[source]})['verifications']
        for verified_claim in verified_claims:
            item = next((x for x in claims if x["id"] == verified_claim["id"]), None)
            if item:
                item["support"] = verified_claim["result"]

    mc_state['eval_score'] = {"claims": claims}
    return mc_state


def calculate_factualness_score(mc_state: MCState, config: RunnableConfig) -> MCState:
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


