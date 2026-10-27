"""
src/generation.py - Prompt formatting and baseline generation routines.
"""
from typing import Any
import torch


def format_generation_prompt(question: str) -> str:
    """Builds a zero-shot prompt enforcing step-structured reasoning."""
    # TODO: Build prompt instructing the model to output Step 1: ..., Step 2: ..., Final Answer: <int>
    raise NotImplementedError("Implement format_generation_prompt")


def generate_greedy(model: Any, tokenizer: Any, question: str) -> dict[str, Any]:
    """Generates a single greedy reasoning path at temperature=0."""
    # TODO: Perform deterministic greedy autoregressive generation
    raise NotImplementedError("Implement generate_greedy")


def generate_self_consistency(
    model: Any, 
    tokenizer: Any, 
    question: str, 
    n: int = 5, 
    temperature: float = 0.7
) -> dict[str, Any]:
    """Samples N diverse reasoning paths and aggregates their final answers via majority vote."""
    # TODO: Sample N completions, extract answers, and compute majority vote
    raise NotImplementedError("Implement generate_self_consistency")

