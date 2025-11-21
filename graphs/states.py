from typing import TypedDict, List, Dict

from pydantic_core.core_schema import typed_dict_field

class MethodComponent(TypedDict):
    components: str
    reference: str

class MCAssessment(TypedDict):
    overview: str
    artifact: str
    artifact_rubric: str
    reflect: str

class MicroCredential(TypedDict):
    whoisthisfor_statement: str
    competency_statement: str
    assessment: MCAssessment
    method_component: MethodComponent

class Claim(TypedDict):
    id: int
    claim: str
    source: str
    support: str

class DimensionFeedback(TypedDict):
    artifact: str
    feedback: dict
    total_score: float

class EvalState(TypedDict):
    claims: List[Claim]
    method_groundness_score:float
    method_faithfulness_score:float
    dim_feedback: DimensionFeedback

class MCState(TypedDict):
    learner_background: str
    knowledge_background: str
    micro_credentials: MicroCredential
    eval_score: EvalState

