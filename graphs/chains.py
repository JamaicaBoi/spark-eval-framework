import os
from dotenv import load_dotenv
load_dotenv()

from utility.chain import ChainLoader
from config import CLAIMS_EXTRACTION_PROMPT, CLAIMS_VERIFICATION_PROMPT

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