CLAIMS_EXTRACTION_PROMPT = "agent-spark-eval-claim_extraction"
CLAIMS_VERIFICATION_PROMPT = "agent-spark-eval-claim_verification"

EVAL_LEARNER_BG_PROMPT = "agent-spark-eval-learner_background"
EVAL_KNOWLEDGE_DOMAIN_PROMPT = "agent-spark-eval-knowledge_domain"

EVAL_WHOISTHISFOR_PROMPT = "agent-spark-eval-whoisthisfor"
EVAL_WHOISTHISFOR_WEIGHT = {
    "profile_concisability_result": 2,
    "need_concisability_result": 2,
    "format_criteria_result": 1
}

EVAL_COMPETENCY_PROMPT = "agent-spark-eval-competency"
EVAL_COMPETENCY_WEIGHT = {
    "concisability_result": 1,
    "alignment_result": 1,
    "action_verb_criteria_result": 1,
    "format_criteria_result": 1
}

EVAL_OVERVIEW_ASSE_PROMPT = "agent-spark-eval-overview_assessment"
EVAL_ARTIFACT_ASSE_PROMPT = "agent-spark-eval-artifact_assessment"
EVAL_REFLECTION_ASSE_PROMPT = "agent-spark-eval-reflection_assessment"

EVAL_METHOD_COMP_PROMPT = "agent-spark-eval-mrthod_component"
EVAL_KEY_METHOD_PROMPT = "agent-spark-eval-key_method"
EVAL_DESCRIPTION_PROMPT = "agent-spark-eval-description"