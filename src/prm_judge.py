"""
src/prm_judge.py - Process Reward Model (PRM) step-level judge prompting and evaluation.
"""
from typing import Any
import re


def build_prm_judge_prompt(question: str, preceding_steps: list[str], current_step: str) -> str:
    """Builds the verification prompt asking the judge to classify current_step as VALID or INVALID."""
    # TODO: Build step-verification prompt providing question, prior context, and current step
    raise NotImplementedError("Implement build_prm_judge_prompt")


def parse_judge_decision(judge_output: str) -> tuple[float, str]:
    """Parses raw text from the judge model into a score (+1.0 or -1.0) and rationale."""
    # TODO: Parse decision label VALID/INVALID, safely defaulting to -1.0 on malformed output
    raise NotImplementedError("Implement parse_judge_decision")


def score_reasoning_step(
    judge_model: Any, 
    tokenizer: Any, 
    question: str, 
    preceding_steps: list[str], 
    current_step: str
) -> dict[str, Any]:
    """Executes a single step verification call against the judge model."""
    # TODO: Format prompt, generate verdict with judge model, and parse response
    raise NotImplementedError("Implement score_reasoning_step")

