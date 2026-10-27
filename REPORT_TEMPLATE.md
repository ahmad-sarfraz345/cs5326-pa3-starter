# CS 5326: Programming Assignment 3 Technical Report
**Student Name:** [Your Name]  
**Roll Number:** [Your Roll Number]  
**Date:** [Date]  

---

## 1. Benchmark Results & Compute Scaling
### 1.1 Summary Table
| Method | GSM8K Acc (%) | Total LLM Calls | Avg Output Tokens / Prob | Total Runtime (s) |
| :--- | :---: | :---: | :---: | :---: |
| Greedy ($N=1$) | | 50 | | |
| Self-Consistency ($N=5$) | | 250 | | |
| Compute-Matched SC ($N_{\text{SC}}=15$) | | 750 | | |
| PRM Best-of-5 ($\min$) | | ~1150 | | |
| PRM Best-of-5 (Product) | | ~1150 | | |
| PRM Best-of-5 (Penalty) | | ~1150 | | |

### 1.2 Accuracy vs. Compute Scaling Plot
*(Include your plot showing GSM8K Accuracy vs. Total Inference Calls / Tokens)*

### 1.3 Discussion of Results
* Does PRM-guided Best-of-5 outperform candidate-matched Self-Consistency ($N=5$)?
* Does it outperform compute-matched Self-Consistency ($N_{\text{SC}}=15$)? Explain why or why not.

---

## 2. Path Score Aggregation Ablation
* Compare the accuracy of the three aggregation rules ($\min$, product, penalty) on the same 5 candidate paths per problem.
* Analyze the theoretical and empirical differences:
  - Why is minimum-pooling aggressive toward potential false negatives?
  - What happens to the joint probability (product) as reasoning path length grows?

---

## 3. Failure Mode & Qualitative Error Taxonomy
Analyze at least three concrete failure cases from your run on `data/gsm8k_test_50.jsonl`:

### Case 1: Judge False Positive (Flawed step marked VALID)
* **Problem ID / Question:**
* **Flawed Reasoning Step:**
* **Judge Verdict & Rationale:**
* **Why did the judge miss it?**

### Case 2: Judge False Negative (Valid step marked INVALID)
* **Problem ID / Question:**
* **Valid Step Flagged as Invalid:**
* **Judge Verdict & Rationale:**
* **Why did the judge fail?**

### Case 3: Mode Collapse / Shared Flawed Premise
* **Problem ID / Question:**
* **Common Mistake Shared Across Paths:**
* **Why did search fail to recover?**

---

## 4. Test-Time Compute Efficiency Analysis
* How many extra seconds and tokens did PRM verification take per problem?
* If given a fixed budget of $10\times$ greedy compute, would you recommend pure repeated sampling (large $N$ Self-Consistency) or step-level PRM search? Justify with your empirical data.

---

## 5. Limitations & Reproducibility
* Hardware environment (e.g., Kaggle T4, local GPU), quantization settings, runtime duration, software package versions, random seeds.
* Discussion of the fundamental difference between a zero-shot prompted LLM judge and a reward model trained directly on human step-level verifications (e.g., PRM800K).

