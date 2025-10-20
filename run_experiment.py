from data_setup import load_and_sample_gsm8k
from llm_api import call_llm
from scoring import score_math_answer, FORMATTING_INSTRUCTION
from prompt_gen import generate_optimized_instruction 
import time
from typing import List, Dict, Tuple

# data config
TOTAL_SAMPLES = 300 
VAL_SAMPLES = 50       # optimization search
EVAL_SAMPLES = 250     # final comparison
OPTIMIZATION_ITERATIONS = 4 # auto prompt improvement

# base prompt
BASELINE_PROMPT = "Answer the following question. You must show your work."

# role assertion
P_BP_PROMPT = """
You are an expert math tutor. 
Solve the following high school grade math problem step-by-step and provide the final answer clearly.
"""

# chain-of-thought
P_COT_PROMPT = """
You are a highly intelligent and expert mathematician. 
Your task is to accurately solve the provided high school grade math problem. 
Before giving your final answer, first reason through the problem step-by-step. 
Show all your calculations clearly.
"""

def run_experiment(data: List[Dict], prompt_template: str) -> float:
    correct_count = 0
    total_count = len(data)
    
    print(f"\n--- Testing on {total_count} samples ---")
    
    for i, example in enumerate(data):
        question = example['question']
        ground_truth_answer_field = example['answer'] 
        
        # creating the full prompt (template + question + format instruction)
        full_prompt = f"{prompt_template}\n{question}{FORMATTING_INSTRUCTION}"
        # LLM call
        llm_output = call_llm(full_prompt)
        # answer scoring
        is_correct = score_math_answer(llm_output, ground_truth_answer_field)
        
        if is_correct:
            correct_count += 1
            
        if (i + 1) % 40 == 0 or i == total_count - 1:
             print(f"  Progress: {i + 1}/{total_count} | Current Accuracy: {correct_count / (i+1):.2f}")
        
        time.sleep(5)  # gemini 2.5 has a 10 rpm or 250 rpd limit

    accuracy = correct_count / total_count
    return accuracy

def find_best_manual_prompt(data_val: List[Dict]) -> Tuple[str, float, str]:
    # Manual prompting on the validation set to establish the best baseline
    experiments = {
        "P-CoT": P_COT_PROMPT,
        "P-BP": P_BP_PROMPT,
        "Baseline": BASELINE_PROMPT      
    }
    
    manual_results = {}
    
    for name, prompt in experiments.items():
        print(f"\n[MANUAL] Running {name}... with prompt:\n{prompt}\n")
        accuracy = run_experiment(data_val, prompt)
        manual_results[name] = accuracy
        print(f"  -> {name} Accuracy: {accuracy:.2%}")

    best_prompt_name = max(manual_results, key=manual_results.get)
    best_accuracy = manual_results[best_prompt_name]
    best_prompt_template = experiments[best_prompt_name]
    
    print(f"\n[RESULT] Best manual prompt is '{best_prompt_name}' with {best_accuracy:.2%}")
    return best_prompt_name, best_accuracy, best_prompt_template


def run_automated_optimization(data_val: List[Dict], initial_prompt: str, initial_score: float) -> str:
    # OPRO-style prompt generation and evaluation 
    current_best_prompt = initial_prompt
    current_best_score = initial_score
    
    for i in range(OPTIMIZATION_ITERATIONS):
        print(f"\nOPTIMIZATION ITERATION {i+1}/{OPTIMIZATION_ITERATIONS}")
        
        # generate new prompt
        new_prompt_candidate = generate_optimized_instruction(current_best_prompt, current_best_score)

        # evaluate new prompt on the validation set 
        print(f"Testing candidate prompt...")
        if new_prompt_candidate == current_best_prompt:
            print("Generation failed or prompt did not change. Skipping re-test.")
            continue
        candidate_score = run_experiment(data_val, new_prompt_candidate)
        
        if candidate_score > current_best_score:
            print(f"Candidate prompt beat current best ({current_best_score:.2%} -> {candidate_score:.2%})")
            current_best_prompt = new_prompt_candidate
            current_best_score = candidate_score
        else:
            print(f"Candidate score {candidate_score:.2%} did not beat current best.")

    return current_best_prompt, current_best_score


if __name__ == '__main__':

    all_data = load_and_sample_gsm8k(sample_size=TOTAL_SAMPLES, seed=42)
    data_val = all_data[:VAL_SAMPLES]
    data_eval = all_data[VAL_SAMPLES:]
    
    best_manual_name, best_manual_score, best_manual_prompt = find_best_manual_prompt(data_val)
    
    # automated prompt optimization
    final_auto_prompt, final_auto_score_val = run_automated_optimization(
        data_val, 
        best_manual_prompt, 
        best_manual_score
    )

    # final evaluation on unseen data
    print("FINAL EVALUATION ON UNSEEN DATA")
    
    final_manual_accuracy = run_experiment(data_eval, best_manual_prompt)
    
    final_auto_accuracy = run_experiment(data_eval, final_auto_prompt)
    
    # prompting results summary
    print("PROMPTING RESULTS SUMMARY")
    print(f"Best manual prompt:\n{best_manual_prompt}\n")
    print(f"Best manual prompt result: ({best_manual_name}): {final_manual_accuracy:.2%}")
    print(f"Best Automated Prompt:\n{final_auto_prompt}\n")
    print(f"Best Automated prompt result: {final_auto_accuracy:.2%}")

    if final_auto_accuracy >= final_manual_accuracy:
        print("\n Automated prompt beat the manual prompt")
    else:
        print("\n Manual prompt beat the automated prompt")