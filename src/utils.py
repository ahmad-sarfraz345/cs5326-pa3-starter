"""
src/utils.py - Model loading, generation constants, seed management, and factories.
"""
from typing import Any, Callable

# Global random seed specified by course policy
GLOBAL_SEED = 5326

# Sampling & decoding hyperparameter configurations
GREEDY_GEN_KWARGS = {
    "do_sample": False,
    "max_new_tokens": 512,
}

SAMPLING_GEN_KWARGS = {
    "do_sample": True,
    "temperature": 0.7,
    "top_p": 1.0,
    "top_k": 0,
    "repetition_penalty": 1.0,
    "max_new_tokens": 512,
}

JUDGE_GEN_KWARGS = {
    "do_sample": False,
    "max_new_tokens": 96,
}


def set_seed_for_problem(problem_index: int) -> None:
    """
    Sets a deterministic seed for problem_index (5326 + problem_index).
    Guarantees reproducibility and safe resumability after interruptions.
    """
    try:
        import transformers
        transformers.set_seed(GLOBAL_SEED + problem_index)
    except ImportError:
        import random
        random.seed(GLOBAL_SEED + problem_index)


def load_models(generator_device: str = "cuda:0", judge_device: str = "cuda:1"):
    """
    Loads Qwen2.5-1.5B-Instruct in float16 (Generator) and
    Qwen2.5-7B-Instruct in 4-bit NF4 (Judge).
    
    Hardware Mapping:
      - Kaggle GPU T4x2: generator on cuda:0, judge on cuda:1.
      - Single GPU: both models placed on cuda:0.
      - Warning: Never use device_map="auto" across two GPUs for a single model!
    """
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

    num_gpus = torch.cuda.device_count() if torch.cuda.is_available() else 0
    if num_gpus < 2:
        g_dev = "cuda:0" if num_gpus == 1 else "cpu"
        j_dev = "cuda:0" if num_gpus == 1 else "cpu"
    else:
        g_dev = generator_device
        j_dev = judge_device

    # 1. Generator: Qwen/Qwen2.5-1.5B-Instruct in float16 (~3.1 GB VRAM)
    gen_id = "Qwen/Qwen2.5-1.5B-Instruct"
    gen_tokenizer = AutoTokenizer.from_pretrained(gen_id)
    if gen_tokenizer.pad_token_id is None:
        gen_tokenizer.pad_token_id = gen_tokenizer.eos_token_id

    gen_device_map = {"": g_dev} if g_dev != "cpu" else None
    gen_model = AutoModelForCausalLM.from_pretrained(
        gen_id,
        torch_dtype=torch.float16 if g_dev != "cpu" else torch.float32,
        device_map=gen_device_map,
    )
    if g_dev == "cpu":
        gen_model = gen_model.to("cpu")

    # 2. Judge: Qwen/Qwen2.5-7B-Instruct in 4-bit NF4 (~5.5 GB VRAM)
    judge_id = "Qwen/Qwen2.5-7B-Instruct"
    judge_tokenizer = AutoTokenizer.from_pretrained(judge_id)
    if judge_tokenizer.pad_token_id is None:
        judge_tokenizer.pad_token_id = judge_tokenizer.eos_token_id

    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.float16,
        bnb_4bit_use_double_quant=True,
    )
    judge_device_map = {"": j_dev} if j_dev != "cpu" else None
    judge_model = AutoModelForCausalLM.from_pretrained(
        judge_id,
        quantization_config=bnb_config if j_dev != "cpu" else None,
        torch_dtype=torch.float16 if j_dev != "cpu" else torch.float32,
        device_map=judge_device_map,
    )
    if j_dev == "cpu":
        judge_model = judge_model.to("cpu")

    return gen_model, gen_tokenizer, judge_model, judge_tokenizer


def make_hf_generate_fn(model: Any, tokenizer: Any) -> Callable[[str, int, dict], list[dict]]:
    """
    Factory creating a GenerateFn conforming to submission_adapter contract.
    Applies the Qwen chat template to raw instruction prompts.
    """
    def generate_fn(prompt: str, num_samples: int, gen_kwargs: dict) -> list[dict]:
        import torch
        messages = [{"role": "user", "content": prompt}]
        formatted_prompt = tokenizer.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True
        )
        inputs = tokenizer(formatted_prompt, return_tensors="pt")
        inputs = {k: v.to(model.device) for k, v in inputs.items()}
        prompt_len = inputs["input_ids"].shape[1]

        kwargs = dict(gen_kwargs)
        if num_samples > 1 and kwargs.get("do_sample", True):
            kwargs["num_return_sequences"] = num_samples

        with torch.no_grad():
            output_ids = model.generate(**inputs, **kwargs)

        results = []
        for i in range(output_ids.shape[0]):
            gen_tokens = output_ids[i][prompt_len:]
            text = tokenizer.decode(gen_tokens, skip_special_tokens=True)
            results.append({"text": text, "num_tokens": len(gen_tokens)})
        return results

    return generate_fn


def make_hf_judge_fn(judge_model: Any, judge_tokenizer: Any) -> Callable[[str], dict]:
    """
    Factory creating a JudgeFn conforming to submission_adapter contract.
    Applies the Qwen chat template to raw judge prompts.
    """
    def judge_fn(judge_prompt: str) -> dict:
        import torch
        messages = [{"role": "user", "content": judge_prompt}]
        formatted = judge_tokenizer.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True
        )
        inputs = judge_tokenizer(formatted, return_tensors="pt")
        inputs = {k: v.to(judge_model.device) for k, v in inputs.items()}
        prompt_len = inputs["input_ids"].shape[1]

        with torch.no_grad():
            output_ids = judge_model.generate(**inputs, **JUDGE_GEN_KWARGS)
        gen_tokens = output_ids[0][prompt_len:]
        text = judge_tokenizer.decode(gen_tokens, skip_special_tokens=True)
        return {"text": text, "num_tokens": len(gen_tokens)}

    return judge_fn
