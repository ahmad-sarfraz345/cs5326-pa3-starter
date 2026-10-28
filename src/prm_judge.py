"""
src/prm_judge.py - PRM judge prompt construction, parsing, and step scoring.
"""
from typing import Any, Callable

JudgeFn = Callable[[str], dict]


def build_prm_judge_prompt(question: str, preceding_steps: list[str], current_step: str) -> str:
    """
    Builds the verification prompt for the PRM judge to classify current_step
    as VALID or INVALID given the problem question and preceding_steps.
    
    Judge Semantics (Local Validity):
      The judge evaluates current_step ASSUMING ALL PRECEDING STEPS ARE CORRECT.
      A step is VALID if its arithmetic is sound and it follows logically from the
      problem statement plus preceding steps as written. An error in an earlier step
      does NOT make subsequent steps invalid by itself.
      
    Expected Output Format:
      Verdict: VALID
      Rationale: <one sentence>
      (or 'Verdict: INVALID').
    """
    # TODO: Build PRM step verification prompt enforcing local validity semantics
    raise NotImplementedError("Implement build_prm_judge_prompt in src/prm_judge.py")


def parse_judge_decision(judge_output: str) -> tuple[float, str]:
    r"""
    Parses the judge model's raw text completion.
    
    Rules:
      1. If a line matches /verdict\\s*:\\s*\\**\\s*(VALID|INVALID)\\b/i, use it.
         If several exist, use the first.
      2. Otherwise, if the standalone word INVALID or phrase 'NOT VALID' appears
         (case-insensitive, word boundaries) -> -1.0.
      3. Otherwise, if the standalone word VALID appears -> +1.0.
      4. Otherwise -> -1.0 (unparseable defaults to INVALID).
      
      Warning: A naive '"VALID" in text' check is wrong because "INVALID" contains "VALID".
      
      Rationale: The text after 'Rationale:' up to the first sentence end or newline, stripped.
      If absent, returns empty string "".
    """
    # TODO: Implement robust judge output decision parser
    raise NotImplementedError("Implement parse_judge_decision in src/prm_judge.py")


def score_path(judge_fn: JudgeFn, question: str, steps: list[str]) -> dict[str, Any]:
    """
    Sequentially scores each step in a reasoning path using judge_fn.
    Step t is judged with preceding_steps = steps[:t].
    """
    # TODO: Implement sequential step scoring loop
    raise NotImplementedError("Implement score_path in src/prm_judge.py")
