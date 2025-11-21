from graphs.workflow import (
    method_component_factual_evaluation,
    learner_background_feedback_graph,
    artifact_feedback_graph
)

method_factual_graph = method_component_factual_evaluation()
learner_bg_graph = learner_background_feedback_graph()

whoisthisfor_feedback_graph = artifact_feedback_graph(artifact="whoisthisfor")
competency_feedback_graph = artifact_feedback_graph(artifact="competency")
