# Results:

### 1st version
#### Baseline prompt (no modifications)
Sampling 100 questions.

--- Running Experiment with: 'Answer the following question with reasonable accuracy.' ---

Q 1/100: Correct=True | Acc: 1.00

Q 2/100: Correct=True | Acc: 1.00

...

Q 93/100: Correct=False | Acc: 0.68

Q 94/100: Correct=True | Acc: 0.69

Q 95/100: Correct=False | Acc: 0.65

BASELINE ACCURACY (100 samples): 70.00%

### Manual prompt engineering (role assertion)
Sampling 100 questions.

--- Running Experiment with: 'You are an expert math tutor. Solve the following high school grade math problem step-by-step and provide the final answer clearly.' ---

Q 1/10: Correct=False | Acc: 0.00

Q 2/10: Correct=True | Acc: 0.50

...

Q 93/10: Correct=True | Acc: 0.67

Q 94/10: Correct=True | Acc: 0.75

Q 95/10: Correct=True | Acc: 0.80

BASELINE ACCURACY (100 samples): 75.00%

### Manual prompt engineering (chain of thought)
Sampling 100 questions.

--- Running Experiment with: 'You are a highly intelligent and expert mathematician. Your task is to accurately solve the provided high school grade math problem. Before giving your final answer, first reason through the problem step-by-step. Show all your calculations clearly.' ---

Q 1/10: Correct=True | Acc: 1

Q 2/10: Correct=False | Acc: 0.50

...

Q 93/10: Correct=True | Acc: 0.78

Q 94/10: Correct=False | Acc: 0.75

Q 95/10: Correct=True | Acc: 0.77

BASELINE ACCURACY (100 samples): 78.00%

## 2nd version (with automated prompt optimization)
Sampling 300 questions.

[MANUAL] Running Baseline... with prompt:
Answer the following question. You must show your work.

--- Testing on 50 samples ---
  Progress: 50/50 | Current Accuracy: 0.68
  -> Baseline Accuracy: 68.00%

[MANUAL] Running P-BP... with prompt:

You are an expert math tutor. 
Solve the following high school grade math problem step-by-step and provide the final answer clearly.

--- Testing on 50 samples ---
  Progress: 50/50 | Current Accuracy: 0.72
  -> P-BP Accuracy: 72.00%

[MANUAL] Running P-CoT... with prompt:

You are a highly intelligent and expert mathematician. 
Your task is to accurately solve the provided high school grade math problem. 
Before giving your final answer, first reason through the problem step-by-step. 
Show all your calculations clearly.

--- Testing on 50 samples ---
  Progress: 50/50 | Current Accuracy: 0.78
  -> P-CoT Accuracy: 78.00%

[RESULT] Best manual prompt is 'P-CoT' with 78.00%

OPTIMIZATION ITERATION 1/4
Testing candidate prompt...

--- Testing on 50 samples ---
  Progress: 50/50 | Current Accuracy: 0.56
Candidate score 56.00% did not beat current best.

OPTIMIZATION ITERATION 2/4
Testing candidate prompt...

--- Testing on 50 samples ---
  Progress: 50/50 | Current Accuracy: 0.63
Candidate score 63.00% did not beat current best.

OPTIMIZATION ITERATION 3/4
Testing candidate prompt...

--- Testing on 50 samples ---
  Progress: 50/50 | Current Accuracy: 0.77
Candidate score 77.00% did not beat current best.

OPTIMIZATION ITERATION 4/4

Testing candidate prompt...

--- Testing on 50 samples ---
  Progress: 50/50 | Current Accuracy: 0.80
Candidate prompt beat current best (78.00% -> 80.00%).

FINAL EVALUATION ON UNSEEN DATA

--- Testing on 250 samples ---
  Progress: 250/250 | Current Accuracy: 0.72

--- Testing on 250 samples ---
  Progress: 250/250 | Current Accuracy: 0.75

PROMPTING RESULTS SUMMARY:

Best manual prompt result: (P-CoT): 72.00%

Best automated prompt result: 75.00%

Automated prompt beat the manual prompt
