# CS 5326: Advanced Generative AI and Agents
## Programming Assignment 3: Search over Reasoning and Step-Level Process Reward Models

**Design and Lead:** Muhammad Ahmad Sarfraz

---

### Overview
This assignment explores **test-time compute** and **reasoning search** without modifying model parameters. You will implement:
1. **Step-Structured Generation & Baseline Decoders:** Prompting schema enforcing numbered reasoning steps, robust regex answer parser, greedy decoding ($N=1$), and Self-Consistency majority voting ($N=5$).
2. **Process Reward Model (PRM) Step-Level Verifier:** Step-by-step verification judge that evaluates whether intermediate reasoning steps are `VALID` or `INVALID`.
3. **Path Aggregation Strategies:** Designing rules ($\min$-pooling, product of validity, and step error penalty) to score complete reasoning trajectories.
4. **PRM-Guided Best-of-$N$ Search ($N=5$):** Ranking sampled paths using process rewards and selecting the most sound candidate.
5. **Compute-Matched Self-Consistency ($N_{\text{SC}} \approx 15$):** Comparing whether spending test-time compute on step verification beats pure brute-force sampling at equal compute budget.
6. **Benchmark Evaluation:** Running all configurations across the fixed 50-problem GSM8K subset (`data/gsm8k_test_50.jsonl`).

For complete mathematical definitions, grading rubrics, and instructions, please refer to the assignment manual (`PA3.pdf`) released on the course LMS.

---

### Repository Structure
```
cs5326-pa3/
|-- data/
|   `-- gsm8k_test_50.jsonl          # Fixed 50-problem evaluation benchmark
|-- src/
|   |-- __init__.py
|   |-- generation.py                # Step prompt, greedy, self-consistency
|   |-- extraction.py                # Regex parser for steps and numerical answers
|   |-- prm_judge.py                 # Step-level verifier prompt & scoring loop
|   |-- search.py                    # PRM-guided Best-of-N and budget tracking
|   `-- utils.py                     # 4-bit model loading, logging, bookkeeping
|-- tests/
|   |-- __init__.py
|   `-- test_public_adapter_smoke.py # Public smoke test suite for grading interface
|-- outputs/                         # Generated predictions and metric dumps
|   `-- results_summary.json         # Automated metrics table across all 4 configurations
|-- submission_adapter.py            # Grading adapter contract (Required)
|-- requirements.txt
|-- pyproject.toml
|-- make_submission.sh               # Submission bundler script
|-- REPORT_TEMPLATE.md               # Scaffold for written report
`-- README.md
```

---

### Getting Started

#### 1. Setup Environment
```bash
pip install -r requirements.txt
```

#### 2. Run Public Smoke Tests
The repository includes a public test suite to verify your adapter signatures and parsing math offline:
```bash
pytest -v tests/test_public_adapter_smoke.py
```
*(Initially, tests will fail with `NotImplementedError` until you implement the required adapter methods).*

#### 3. Execution on Kaggle (GPU T4x2)
Create a new Kaggle notebook, set the **Accelerator** in the top sidebar to **GPU T4x2**, and turn **Internet** to **On**. Clone the repository:
```bash
!git clone https://github.com/ahmad-sarfraz345/cs5326-pa3-starter.git
%cd cs5326-pa3-starter
!pip install -q -r requirements.txt
```
Load the reference model in 4-bit NF4 precision within ~5.5 GB VRAM:
```python
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

model_id = "Qwen/Qwen2.5-7B-Instruct"
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
```

#### 4. Packaging Your Submission
When your implementation passes all tests and your benchmark run produces `outputs/results_summary.json`:
```bash
bash make_submission.sh <your_roll_number>
```
This generates `<your_roll_number>_pa3.zip` containing your `src/`, `submission_adapter.py`, `outputs/results_summary.json`, and `REPORT.pdf`. Upload this archive to LMS.

