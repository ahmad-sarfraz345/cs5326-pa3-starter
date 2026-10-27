"""
src/utils.py - Model loading, JSONL file utilities, and metrics bookkeeping.
"""
import json
from typing import Any
import torch


def load_quantized_qwen_model(model_id: str = "Qwen/Qwen2.5-7B-Instruct"):
    """Loads Qwen 2.5 7B Instruct in 4-bit NF4 precision for Kaggle T4 or local GPU."""
    from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
    
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.float16,
        bnb_4bit_use_double_quant=True
    )
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        quantization_config=bnb_config,
        device_map="auto"
    )
    return model, tokenizer


def load_gsm8k_dataset(path: str = "data/gsm8k_test_50.jsonl") -> list[dict[str, Any]]:
    """Loads the fixed 50-problem benchmark from disk."""
    problems = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                problems.append(json.loads(line))
    return problems

