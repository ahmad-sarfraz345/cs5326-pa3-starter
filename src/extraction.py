"""
src/extraction.py - Step and answer extraction utilities.
"""


def parse_steps(completion_text: str) -> list[str]:
    """
    Parses completion text and returns a list of individual step strings.
    Must tolerate markdown decoration around labels (e.g. '**Step 1:**', '### Step 2:')
    and strip leftover '*' or '#' from captured text.
    """
    # TODO: Implement robust regex step extraction
    raise NotImplementedError("Implement parse_steps in src/extraction.py")


def extract_answer(completion_text: str) -> int | None:
    """
    Extracts the final numeric integer from the completion.
    
    Required Behaviors:
      - 'Final Answer: 18' -> 18
      - 'Final Answer: $1,234' -> 1234
      - 'Final Answer: 18.00' -> 18
      - 'Final Answer: 18.5' -> None (non-integer)
      - 'Final Answer: -5' -> -5
      - 'Final Answer: 18 dollars.' -> 18
      - '**Final Answer:** 18' -> 18
      - 'final answer 18' (case-insensitive, colon optional) -> 18
      - Multiple 'Final Answer' lines -> use the LAST one
      - No 'Final Answer' present -> None
      - Empty string or None-like garbage -> None, and never raise
    """
    # TODO: Implement robust regex answer extraction
    raise NotImplementedError("Implement extract_answer in src/extraction.py")
