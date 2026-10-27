"""
src/extraction.py - Regular Expression Parsing for Steps and Answers.
"""
import re


def parse_reasoning_steps(completion_text: str) -> list[str]:
    """Extracts individual 'Step i: ...' text blocks into a list of strings."""
    # TODO: Implement robust regex pattern to capture Step 1, Step 2, etc.
    raise NotImplementedError("Implement parse_reasoning_steps")


def extract_final_answer(completion_text: str) -> int | None:
    """Extracts the final numeric integer following 'Final Answer:'."""
    # TODO: Implement regex matching for integers, handling commas and currency symbols.
    raise NotImplementedError("Implement extract_final_answer")

