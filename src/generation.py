"""
src/generation.py - Prompt formatting and baseline generation routines.
"""
from typing import Any, Callable

GenerateFn = Callable[[str, int, dict], list[dict]]


def format_step_prompt(question: str) -> str:
    """
    Formats the raw problem question into a prompt that instructs the 
    model to emit numbered steps ('Step 1: ...') and 'Final Answer: <int>'.
    
    Returns a raw instruction string (no chat template applied).
    """
    # TODO: Build zero-shot prompt enforcing step-structured reasoning
    raise NotImplementedError("Implement format_step_prompt in src/generation.py")


def compute_majority_vote(answers: list[int | None]) -> int | None:
    """
    Given a list of extracted answers, returns the majority answer.
    Ignores None values. Breaks ties deterministically in favor of the answer
    that appeared earliest in the list.
    """
    # TODO: Implement deterministic majority voting
    raise NotImplementedError("Implement compute_majority_vote in src/generation.py")


def run_greedy(generate_fn: GenerateFn, question: str) -> dict[str, Any]:
    """
    Executes greedy decoding for a single question using generate_fn.
    Must call generate_fn with num_samples=1 and gen_kwargs containing do_sample=False.
    """
    # TODO: Implement greedy baseline decoding
    raise NotImplementedError("Implement run_greedy in src/generation.py")


def run_self_consistency(
    generate_fn: GenerateFn, 
    question: str, 
    n: int = 5, 
    temperature: float = 0.7
) -> dict[str, Any]:
    """
    Samples n diverse reasoning trajectories and aggregates candidate answers via majority vote.
    """
    # TODO: Implement Self-Consistency sampling and majority voting
    raise NotImplementedError("Implement run_self_consistency in src/generation.py")
