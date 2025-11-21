import os
from dotenv import load_dotenv
load_dotenv()

from utility.chain import ChainLoader
from config import (
    CLAIMS_EXTRACTION_PROMPT, 
    CLAIMS_VERIFICATION_PROMPT,
    EVAL_COMPETENCY_PROMPT,
    EVAL_LEARNER_BG_PROMPT,
    EVAL_KNOWLEDGE_DOMAIN_PROMPT,
    EVAL_WHOISTHISFOR_PROMPT)

def get_claims_extraction_chain(config=None):
    chain = ChainLoader.load_chain(prompt_name=CLAIMS_EXTRACTION_PROMPT,
                                   partial_variables={},
                                   parser=None,
                                   config=config)
    return chain

def get_claims_verification_chain(config=None):
    chain = ChainLoader.load_chain(prompt_name=CLAIMS_VERIFICATION_PROMPT,
                                   partial_variables={},
                                   parser=None,
                                   config=config)
    return chain

def get_learner_background_feedback_chain(config=None):
    chain = ChainLoader.load_chain(prompt_name=EVAL_LEARNER_BG_PROMPT,
                                   partial_variables={},
                                   parser=None,
                                   config=config)
    return chain

def get_knowledge_background_feedback_chain(config=None):
    chain = ChainLoader.load_chain(prompt_name=EVAL_KNOWLEDGE_DOMAIN_PROMPT,
                                   partial_variables={},
                                   parser=None,
                                   config=config)
    return chain

def get_whoisthisfor_feedback_chain(config=None):
    chain = ChainLoader.load_chain(prompt_name=EVAL_WHOISTHISFOR_PROMPT,
                                   partial_variables={},
                                   parser=None,
                                   config=config)
    return chain

def get_competency_feedback_chain(config=None):
    chain = ChainLoader.load_chain(prompt_name=EVAL_COMPETENCY_PROMPT,
                                   partial_variables={},
                                   parser=None,
                                   config=config)
    return chain