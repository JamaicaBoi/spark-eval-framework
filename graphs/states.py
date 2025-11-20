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

class EvalState(TypedDict):
    claims: List[Claim]
    method_groundness_score:float
    method_faithfulness_score:float

class MCState(TypedDict):
    course_name: str
    course_description: str
    learning_outcomes: List[str]
    knowledge_level: str
    learner_profile: str
    micro_credentials: MicroCredential

    eval_score: EvalState
    feedback: List[Dict]
    loop_limit: int
    current_loop: int
