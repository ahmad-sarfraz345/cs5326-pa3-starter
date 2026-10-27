"""
src/search.py - Search algorithms over reasoning paths and budget-matched decoding.
"""
from typing import Any


def aggregate_path_score(step_scores: list[float], strategy: str = "min") -> float:
    """Aggregates a list of step scores into a scalar path score."""
    # TODO: Implement 'min', 'product', and 'step_penalty'
    raise NotImplementedError("Implement aggregate_path_score")


def run_prm_best_of_n(
    model: Any, 
    judge_model: Any, 
    tokenizer: Any, 
    question: str, 
    n: int = 5, 
    aggregation_strategy: str = "min"
) -> dict[str, Any]:
    """Runs PRM-guided Best-of-N search over N sampled reasoning paths."""
    # TODO: Sample N paths, score all steps with PRM judge, aggregate path score, pick best
    raise NotImplementedError("Implement run_prm_best_of_n")


def run_compute_matched_self_consistency(
    model: Any, 
    tokenizer: Any, 
    question: str, 
    target_calls: int = 15
) -> dict[str, Any]:
    """Runs compute-matched Self-Consistency sampling target_calls candidates."""
    # TODO: Sample target_calls paths and compute majority vote
    raise NotImplementedError("Implement run_compute_matched_self_consistency")

