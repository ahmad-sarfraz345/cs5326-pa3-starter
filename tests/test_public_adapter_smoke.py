"""
CS 5326: Public Smoke Tests for submission_adapter.py.
Can be executed with either:
    python tests/test_public_adapter_smoke.py
or:
    pytest -v tests/test_public_adapter_smoke.py
"""
import math
import sys
import os

# Ensure repository root is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import submission_adapter as adapter


def test_format_step_prompt():
    q = "Janet has 16 eggs. She eats 3 and bakes with 4. How many eggs are left?"
    prompt = adapter.format_step_prompt(q)
    assert isinstance(prompt, str)
    assert q in prompt
    assert "Step" in prompt
    assert "Final Answer" in prompt


def test_parse_steps():
    text = (
        "Here is my step by step thought process:\n"
        "Step 1: Janet starts with 16 eggs.\n"
        "Step 2: She uses 3 + 4 = 7 eggs.\n"
        "Step 3: Remaining eggs are 16 - 7 = 9.\n"
        "Final Answer: 9"
    )
    steps = adapter.parse_steps(text)
    assert isinstance(steps, list)
    assert len(steps) == 3
    assert "starts with 16 eggs" in steps[0]
    assert "uses 3 + 4 = 7 eggs" in steps[1]
    assert "16 - 7 = 9" in steps[2]


def test_extract_answer_clean():
    text = "Step 1: 5 + 5 = 10\nFinal Answer: 10"
    assert adapter.extract_answer(text) == 10


def test_extract_answer_formatting_variants():
    # Dollar signs
    assert adapter.extract_answer("Step 1: calc\nFinal Answer: $18") == 18
    # Commas in large numbers
    assert adapter.extract_answer("Step 1: calc\nFinal Answer: 140,000") == 140000
    # Negative integers
    assert adapter.extract_answer("Step 1: calc\nFinal Answer: -42") == -42
    # Punctuation / extra trailing text
    assert adapter.extract_answer("Step 1: calc\nFinal Answer: 25.") == 25


def test_extract_answer_malformed():
    assert adapter.extract_answer("I think the answer is 42.") is None
    assert adapter.extract_answer("") is None
    assert adapter.extract_answer("Final Answer: none") is None


def test_compute_majority_vote_unanimous():
    answers = [18, 18, 18, 18, 18]
    assert adapter.compute_majority_vote(answers) == 18


def test_compute_majority_vote_clear_winner():
    answers = [12, 18, 18, 18, 24]
    assert adapter.compute_majority_vote(answers) == 18


def test_compute_majority_vote_with_nones():
    answers = [None, 15, None, 15, 20]
    assert adapter.compute_majority_vote(answers) == 15


def test_compute_majority_vote_all_nones():
    assert adapter.compute_majority_vote([None, None, None]) is None
    assert adapter.compute_majority_vote([]) is None


def test_compute_majority_vote_tie_breaking():
    # 10 appears before 20; both have 2 votes. Must pick 10 deterministically.
    answers = [10, 20, 10, 20]
    assert adapter.compute_majority_vote(answers) == 10
    
    # 20 appears before 10; both have 2 votes. Must pick 20 deterministically.
    answers = [20, 10, 10, 20]
    assert adapter.compute_majority_vote(answers) == 20


def test_build_prm_judge_prompt():
    q = "What is 2 + 2?"
    preceding = ["Step 1: Let x = 2."]
    curr = "Step 2: 2 + 2 = 4."
    prompt = adapter.build_prm_judge_prompt(q, preceding, curr)
    assert isinstance(prompt, str)
    assert q in prompt
    assert preceding[0] in prompt
    assert curr in prompt
    assert "VALID" in prompt
    assert "INVALID" in prompt


def test_parse_judge_decision_valid():
    output = "Decision: VALID\nRationale: The arithmetic 3 + 4 = 7 is completely correct."
    score, rationale = adapter.parse_judge_decision(output)
    assert score == 1.0
    assert "arithmetic" in rationale.lower()


def test_parse_judge_decision_invalid():
    output = "Decision: INVALID\nRationale: The student computed 16 - 7 = 8 which is incorrect."
    score, rationale = adapter.parse_judge_decision(output)
    assert score == -1.0
    assert "incorrect" in rationale.lower()


def test_parse_judge_decision_fallback():
    # Garbled or incomplete output must safely default to -1.0
    score, rationale = adapter.parse_judge_decision("I am not sure about this.")
    assert score == -1.0


def test_aggregate_path_score_min():
    # Sound path
    assert adapter.aggregate_path_score([1.0, 1.0, 1.0], strategy="min") == 1.0
    # One flawed step
    assert adapter.aggregate_path_score([1.0, -1.0, 1.0], strategy="min") == -1.0
    # Empty path
    assert adapter.aggregate_path_score([], strategy="min") == -1.0


def test_aggregate_path_score_product():
    # All valid steps should have high product
    score_clean = adapter.aggregate_path_score([1.0, 1.0, 1.0], strategy="product")
    # Path with flawed step should have drastically lower product
    score_flawed = adapter.aggregate_path_score([1.0, -1.0, 1.0], strategy="product")
    assert score_clean > score_flawed
    assert score_flawed > 0.0


def test_aggregate_path_score_penalty():
    score_clean = adapter.aggregate_path_score([1.0, 1.0, 1.0], strategy="step_penalty")
    score_flawed = adapter.aggregate_path_score([1.0, -1.0, 1.0], strategy="step_penalty")
    assert abs(score_clean - 1.0) < 1e-5
    # 1/3 * (1 - 1 + 1) - 2.0 * 1 = 1/3 - 2 = -1.6667
    assert score_flawed < 0.0


def test_select_best_path():
    candidates = [
        {"steps": ["s1", "s2"], "step_scores": [1.0, -1.0], "answer": 12}, # Flawed
        {"steps": ["s1", "s2", "s3"], "step_scores": [1.0, 1.0, 1.0], "answer": 18}, # Clean
        {"steps": ["s1"], "step_scores": [-1.0], "answer": 24}, # Flawed
    ]
    winner = adapter.select_best_path(candidates, aggregation_strategy="min")
    assert winner["answer"] == 18
    assert winner["path_score"] == 1.0


if __name__ == "__main__":
    test_funcs = [v for k, v in list(globals().items()) if k.startswith("test_") and callable(v)]
    passed = 0
    failed = 0
    print(f"Running {len(test_funcs)} public adapter smoke tests...")
    for fn in test_funcs:
        try:
            fn()
            print(f"  [PASS] {fn.__name__}")
            passed += 1
        except Exception as e:
            print(f"  [FAIL] {fn.__name__}: {e}")
            failed += 1
    print("=" * 45)
    print(f"Test Summary: {passed} passed, {failed} failed.")
    if failed > 0:
        sys.exit(1)
    else:
        print("ALL TESTS PASSED SUCCESSFULLY!")
