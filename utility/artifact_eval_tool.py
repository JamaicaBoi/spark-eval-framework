from re import template
from langchain.tools import tool
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

from dotenv import load_dotenv
from pydantic import BaseModel
load_dotenv()

import sys, datetime, json
sys.path.append("/Users/peerawat/Documents/GitHub/spark-eval-framework/")

from config import (
    CLAIMS_EXTRACTION_PROMPT,
    CLAIMS_VERIFICATION_PROMPT,
    EVAL_COMPETENCY_OUTPUT,
    EVAL_COMPETENCY_PROMPT,
    EVAL_COMPETENCY_WEIGHT,
    EVAL_WHOISTHISFOR_PROMPT,
    EVAL_WHOISTHISFOR_OUTPUT,
    EVAL_WHOISTHISFOR_WEIGHT
)
from utility.output_schema import ExtractFactualClaimsOutput,ClaimVerification
from utility.web_search_tool import brave_search,jina_reader_fetch

llm = ChatOpenAI(
    name="evaluation model",
    model="gpt-5-mini",
    temperature=0,
)

async def methodcomp_claims_extraction(method_component: str, reference:str) -> ExtractFactualClaimsOutput:
    ## Extract Claim
    prompt = PromptTemplate.from_template(
        template=CLAIMS_EXTRACTION_PROMPT,
        template_format="jinja2"
    )
    complie_prompt = prompt.format(method_component=method_component,reference=reference)
    structure_llm = llm.with_structured_output(ExtractFactualClaimsOutput)
    extracted_result = await structure_llm.ainvoke(complie_prompt)
    return extracted_result

async def methodcomp_claims_verification(extracted_result:ExtractFactualClaimsOutput) -> ExtractFactualClaimsOutput:
    ## Grouped source
    grouped = {}
    for claim in extracted_result.claims:
        claim.support = 'no'
        src = claim.source
        if src not in grouped:
            grouped[src] = []
        grouped[src].append(claim)

     ## verifiy Claim
    verify_prompt = PromptTemplate.from_template(
        template=CLAIMS_VERIFICATION_PROMPT,
        template_format="jinja2"
    )
    structure_verify_llm = llm.with_structured_output(ClaimVerification)

    for source in grouped.keys():
        if source == '':
            continue
        web_url = brave_search(source,limit=1)
        ref_content = jina_reader_fetch(web_url[0]['link'])
        formatted_verify_prompt = verify_prompt.format(ref_content=ref_content,claims=grouped[source])
        verifed_result = await structure_verify_llm.ainvoke(formatted_verify_prompt)
        for verified_claim in verifed_result.verifications:
            item = next((x for x in extracted_result.claims if x.id == verified_claim.id), None)
            if item:
                item.support = verified_claim.result

    return extracted_result

async def calculate_factualness_score(verified_claims:ExtractFactualClaimsOutput) -> dict:
    count_with_source = sum(1 for item in verified_claims.claims if item.source != '')
    count_support = sum(1 for item in verified_claims.claims if item.support == "yes")
    count_claims = len(verified_claims.claims)
    try:
        groundness_score = count_with_source/count_claims
    except:
        groundness_score = 0.0
    try:
        faithfulness_score = count_support/count_with_source
    except:
        faithfulness_score = 0.0
    
    result = {
        "claims": [c for c in verified_claims.claims],
        "groundness_score": groundness_score,
        "faithfulness_score": faithfulness_score,
    }
    return result

async def calculate_dimension_weight(artifact_name:str,feedback:dict) -> dict:
    artifact_feedback = feedback
    if artifact_name == "whoisthisfor":
        weight = EVAL_WHOISTHISFOR_WEIGHT
    elif artifact_name == "competency":
        weight = EVAL_COMPETENCY_WEIGHT
    else:
        return {}
    
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
    result = {
        'total_score': total_score,
        'dimension_result': feedback
    }
    return result

# ================================================ #

# @tool(description="Evaluates the factual accuracy of a given method component based on a reference.")
async def method_component_factualness_evaluation(method_component: str, reference:str) -> dict:
    extracted_claims = await methodcomp_claims_extraction(method_component=method_component,reference=reference)
    verified_claims = await methodcomp_claims_verification(extracted_result=extracted_claims)
    result = await calculate_factualness_score(verified_claims=verified_claims)
    return result

# @tool
async def whoisthisfor_feedback(whoisthisfor:str) -> dict:
    prompt = PromptTemplate.from_template(
        template=EVAL_WHOISTHISFOR_PROMPT,
        template_format="jinja2"
    )
    complie_prompt = prompt.format(whoisthisfor=whoisthisfor)
    structure_llm = llm.with_structured_output(EVAL_WHOISTHISFOR_OUTPUT,method='json_schema')
    dimension_feedback = await structure_llm.ainvoke(complie_prompt)

    result = await calculate_dimension_weight(artifact_name='whoisthisfor',feedback=dimension_feedback)
    return result

# @tool
async def competency_feedback(whoisthisfor:str,competency:str) -> dict:
    prompt = PromptTemplate.from_template(
        template=EVAL_COMPETENCY_PROMPT,
        template_format="jinja2"
    )
    complie_prompt = prompt.format(whoisthisfor=whoisthisfor,competency=competency)
    structure_llm = llm.with_structured_output(EVAL_COMPETENCY_OUTPUT,method='json_schema')
    dimension_feedback = await structure_llm.ainvoke(complie_prompt)

    result = await calculate_dimension_weight(artifact_name='competency',feedback=dimension_feedback)
    return result



    
