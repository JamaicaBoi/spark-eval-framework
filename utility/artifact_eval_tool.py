from langchain.tools import tool
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

from dotenv import load_dotenv
from pydantic import BaseModel
load_dotenv()

import sys, datetime, json
from pathlib import Path

# Add project root to sys.path (works on any OS)
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from config import (
    CLAIMS_EXTRACTION_PROMPT,
    CLAIMS_EXTRACTION_OUTPUT,
    CLAIMS_VERIFICATION_PROMPT,
    CLAIMS_VERIFICATION_OUTPUT,
    EVAL_COMPETENCY_OUTPUT,
    EVAL_COMPETENCY_PROMPT,
    EVAL_COMPETENCY_WEIGHT,
    EVAL_METHOD_COMP_OUTPUT,
    EVAL_METHOD_COMP_PROMPT,
    EVAL_METHOD_COMP_WEIGHT,
    EVAL_WHOISTHISFOR_PROMPT,
    EVAL_WHOISTHISFOR_OUTPUT,
    EVAL_WHOISTHISFOR_WEIGHT,
    EVAL_KEY_METHOD_PROMPT,
    EVAL_KEY_METHOD_OUTPUT,
    EVAL_KEY_METHOD_WEIGHT,
    EVAL_DESCRIPTION_PROMPT,
    EVAL_DESCRIPTION_OUTPUT,
    EVAL_DESCRIPTION_WEIGHT,
    EVAL_OVERVIEW_ASSE_PROMPT,
    EVAL_OVERVIEW_ASSE_OUTPUT,
    EVAL_OVERVIEW_ASSE_WEIGHT,
    EVAL_MAIN_ASSE_PROMPT,
    EVAL_MAIN_ASSE_OUTPUT,
    EVAL_MAIN_ASSE_WEIGHT,
    EVAL_REFLECTION_ASSE_PROMPT,
    EVAL_REFLECTION_ASSE_OUTPUT,
    EVAL_REFLECTION_ASSE_WEIGHT
)
from utility.web_search_tool import brave_search,jina_reader_fetch

llm = ChatOpenAI(
    name="evaluation model",
    model="gpt-5-mini",
    temperature=0,
)

async def methodcomp_claims_extraction(method_component: str, reference:str) -> dict:
    ## Extract Claim
    prompt = PromptTemplate.from_template(
        template=CLAIMS_EXTRACTION_PROMPT,
        template_format="jinja2"
    )
    complie_prompt = prompt.format(method_component=method_component,reference=reference)
    structure_llm = llm.with_structured_output(CLAIMS_EXTRACTION_OUTPUT, method='json_schema')
    extracted_result = await structure_llm.ainvoke(complie_prompt)
    return extracted_result

async def methodcomp_claims_verification(extracted_result:dict) -> dict:
    ## Grouped source
    grouped = {}
    for claim in extracted_result['claims']:
        claim['support'] = 'no'
        src = claim['source']
        if src not in grouped:
            grouped[src] = []
        grouped[src].append(claim)

     ## verifiy Claim
    verify_prompt = PromptTemplate.from_template(
        template=CLAIMS_VERIFICATION_PROMPT,
        template_format="jinja2"
    )
    structure_verify_llm = llm.with_structured_output(CLAIMS_VERIFICATION_OUTPUT, method='json_schema')

    for source in grouped.keys():
        if source == '':
            continue
        web_url = brave_search(source,limit=1)
        ref_content = jina_reader_fetch(web_url[0]['link'])
        formatted_verify_prompt = verify_prompt.format(ref_content=ref_content,claims=grouped[source])
        verifed_result = await structure_verify_llm.ainvoke(formatted_verify_prompt)
        for verified_claim in verifed_result['verifications']:
            item = next((x for x in extracted_result['claims'] if x['id'] == verified_claim['id']), None)
            if item:
                item['support'] = verified_claim['result']

    return extracted_result

async def calculate_factualness_score(verified_claims:dict) -> dict:
    count_with_source = sum(1 for item in verified_claims['claims'] if item['source'] != '')
    count_support = sum(1 for item in verified_claims['claims'] if item['source'] == "yes")
    count_claims = len(verified_claims['claims'])
    try:
        groundness_score = count_with_source/count_claims
    except:
        groundness_score = 0.0
    try:
        faithfulness_score = count_support/count_with_source
    except:
        faithfulness_score = 0.0
    
    result = {
        "claims": [c for c in verified_claims['claims']],
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
    elif artifact_name == "method component":
        weight = EVAL_METHOD_COMP_WEIGHT
    elif artifact_name == "key method":
        weight = EVAL_KEY_METHOD_WEIGHT
    elif artifact_name == "description":
        weight = EVAL_DESCRIPTION_WEIGHT
    elif artifact_name == "overview assessment":
        weight = EVAL_OVERVIEW_ASSE_WEIGHT
    elif artifact_name == "main assessment":
        weight = EVAL_MAIN_ASSE_WEIGHT
    elif artifact_name == "reflection assessment":
        weight = EVAL_REFLECTION_ASSE_WEIGHT
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
async def whoisthisfor_feedback_graph(whoisthisfor:str) -> dict:
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
async def competency_feedback_graph(whoisthisfor:str,competency:str) -> dict:
    prompt = PromptTemplate.from_template(
        template=EVAL_COMPETENCY_PROMPT,
        template_format="jinja2"
    )
    complie_prompt = prompt.format(whoisthisfor=whoisthisfor,competency=competency)
    structure_llm = llm.with_structured_output(EVAL_COMPETENCY_OUTPUT,method='json_schema')
    dimension_feedback = await structure_llm.ainvoke(complie_prompt)

    result = await calculate_dimension_weight(artifact_name='competency',feedback=dimension_feedback)
    return result

# @tool
async def method_component_feedback_graph(whoisthisfor:str,competency:str,artifact_assessment:str,method_component:str) -> dict:
    prompt = PromptTemplate.from_template(
        template=EVAL_METHOD_COMP_PROMPT,
        template_format="jinja2"
    )
    complie_prompt = prompt.format(whoisthisfor=whoisthisfor,competency=competency,artifact_assessment=artifact_assessment, method_component=method_component)
    structure_llm = llm.with_structured_output(EVAL_METHOD_COMP_OUTPUT,method='json_schema')
    dimension_feedback = await structure_llm.ainvoke(complie_prompt)

    result = await calculate_dimension_weight(artifact_name='method component',feedback=dimension_feedback)
    return result

# @tool
async def key_method_feedback_graph(method_component:str, key_method:str) -> dict:
    prompt = PromptTemplate.from_template(
        template=EVAL_KEY_METHOD_PROMPT,
        template_format="jinja2"
    )
    complie_prompt = prompt.format(method_component=method_component, key_method=key_method)
    structure_llm = llm.with_structured_output(EVAL_KEY_METHOD_OUTPUT,method='json_schema')
    dimension_feedback = await structure_llm.ainvoke(complie_prompt)

    result = await calculate_dimension_weight(artifact_name='key method',feedback=dimension_feedback)
    return result

# @tool
async def mc_description_feedback_graph(competency:str, key_method:str, description:str) -> dict:
    prompt = PromptTemplate.from_template(
        template=EVAL_DESCRIPTION_PROMPT,
        template_format="jinja2"
    )
    complie_prompt = prompt.format(competency=competency, key_method=key_method, description=description)
    structure_llm = llm.with_structured_output(EVAL_DESCRIPTION_OUTPUT,method='json_schema')
    dimension_feedback = await structure_llm.ainvoke(complie_prompt)

    result = await calculate_dimension_weight(artifact_name='description',feedback=dimension_feedback)
    return result

# @tool
async def overview_assessment_feedback_graph(competency:str, overview_assessment:str) -> dict:
    prompt = PromptTemplate.from_template(
        template=EVAL_OVERVIEW_ASSE_PROMPT,
        template_format="jinja2"
    )
    complie_prompt = prompt.format(competency=competency, assessment=overview_assessment)
    structure_llm = llm.with_structured_output(EVAL_OVERVIEW_ASSE_OUTPUT,method='json_schema')
    dimension_feedback = await structure_llm.ainvoke(complie_prompt)

    result = await calculate_dimension_weight(artifact_name='overview assessment',feedback=dimension_feedback)
    return result

# @tool
async def main_assessment_feedback_graph(competency:str,overview_assessment:str, main_assessment:str) -> dict:
    prompt = PromptTemplate.from_template(
        template=EVAL_MAIN_ASSE_PROMPT,
        template_format="jinja2"
    )
    complie_prompt = prompt.format(competency=competency, overview_assessment=overview_assessment, assessment=main_assessment)
    structure_llm = llm.with_structured_output(EVAL_MAIN_ASSE_OUTPUT,method='json_schema')
    dimension_feedback = await structure_llm.ainvoke(complie_prompt)

    result = await calculate_dimension_weight(artifact_name='main assessment',feedback=dimension_feedback)
    return result

# @tool
async def reflection_assessment_feedback_graph(competency:str,main_assessment:str, reflection_assessment:str) -> dict:
    prompt = PromptTemplate.from_template(
        template=EVAL_REFLECTION_ASSE_PROMPT,
        template_format="jinja2"
    )
    complie_prompt = prompt.format(competency=competency, artifact_assessment=main_assessment, assessment=reflection_assessment)
    structure_llm = llm.with_structured_output(EVAL_REFLECTION_ASSE_OUTPUT,method='json_schema')
    dimension_feedback = await structure_llm.ainvoke(complie_prompt)

    result = await calculate_dimension_weight(artifact_name='reflection assessment',feedback=dimension_feedback)
    return result


    
