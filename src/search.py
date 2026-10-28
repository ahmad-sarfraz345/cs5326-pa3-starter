"""
src/search.py - Path aggregation, Best-of-N selection, and compute-matched search.
"""
from typing import Any, Callable

GenerateFn = Callable[[str, int, dict], list[dict]]
JudgeFn = Callable[[str], dict]


def aggregate_path_score(
    step_scores: list[float], 
    strategy: str = "min", 
    penalty_lambda: float = 2.0
) -> float:
    """
    Aggregates a list of step scores (+1.0 or -1.0) into a scalar trajectory score.
    
    Rules:
      - An empty list returns -1.0 for every strategy.
      - 'min': min(step_scores).
      - 'product': p_t = clamp((r_t + 1)/2, 0.01, 0.99); returns the raw product.
      - 'step_penalty': mean(step_scores) - penalty_lambda * count(r_t == -1.0).
      - An unknown strategy raises ValueError.
    """
    # TODO: Implement step score aggregation rules
    raise NotImplementedError("Implement aggregate_path_score in src/search.py")


def select_best_path(
    candidate_paths: list[dict[str, Any]], 
    aggregation_strategy: str = "min", 
    penalty_lambda: float = 2.0
) -> dict[str, Any]:
    """
    Selects the winning candidate path from candidate_paths.
    
    Selection & Tie-Breaking Rules:
      1. Compute path_score for each candidate with aggregate_path_score.
         A candidate with an empty step_scores list gets -1.0.
      2. Eligibility: if at least one candidate has a non-None answer, candidates
         with answer=None are excluded. If all answers are None, all remain eligible.
      3. Find maximum path_score among eligible candidates (tolerance 1e-9).
         The tied set is all eligible candidates within tolerance of the maximum.
      4. If the tied set has more than one candidate, compute compute_majority_vote
         over their answers. Return the lowest-index candidate in the tied set whose
         answer equals the vote. If the vote is None, return the lowest-index tied candidate.
      5. Returns a shallow COPY of the chosen dict with two added keys:
         'path_score' (float) and 'num_tied' (int, size of the tied set).
         Does not mutate the inputs.
    """
    # TODO: Implement Best-of-N candidate selection and majority tie-breaking
    raise NotImplementedError("Implement select_best_path in src/search.py")


def run_prm_best_of_n(
    generate_fn: GenerateFn, 
    judge_fn: JudgeFn, 
    question: str, 
    n: int = 5, 
    aggregation_strategy: str = "min", 
    penalty_lambda: float = 2.0, 
    candidates: list[dict[str, Any]] | None = None
) -> dict[str, Any]:
    """
    Executes PRM-guided Best-of-N search over candidate trajectories.
    
    If candidates is provided (shared candidate pool), does NOT sample new paths.
    Otherwise, samples n candidates using run_self_consistency.
    Every candidate has all steps scored by judge_fn (no early stopping).
    Selects the winning candidate via select_best_path.
    """
    # TODO: Implement PRM Best-of-N search pipeline
    raise NotImplementedError("Implement run_prm_best_of_n in src/search.py")


def run_compute_matched_self_consistency(
    generate_fn: GenerateFn, 
    question: str, 
    target_calls: int = 15, 
    existing_candidates: list[dict[str, Any]] | None = None
) -> dict[str, Any]:
    """
    Executes compute-matched Self-Consistency with target_calls total paths.
    If existing_candidates are supplied, samples only the deficit:
    target_calls - len(existing_candidates).
    """
    # TODO: Implement compute-matched Self-Consistency sampling
    raise NotImplementedError("Implement run_compute_matched_self_consistency in src/search.py")
