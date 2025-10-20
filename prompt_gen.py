from llm_api import call_llm
import re

OPTIMIZER_PROMPT = """
You are an expert prompt engineer. Your task is to generate the highest performing **System Instruction** for a large language model whose sole job is to solve complex grade school math word problems (GSM8K).

The instruction you generate must be a single, concise paragraph. It must focus on:
1.  **Clarity**: Clearly define the model's role as a math solver.
2.  **Reasoning**: **Mandate** step-by-step thinking (Chain-of-Thought).
3.  **Precision**: Emphasize numerical accuracy and attention to detail.

Your entire response MUST contain **ONLY** the new system instruction, enclosed exactly within the specified format tags, with **no other commentary or text outside the tags**.

Format your output exactly in this format:
[NEW INSTRUCTION START]
<Your proposed new system instruction here>
[NEW INSTRUCTION END]
"""

def generate_optimized_instruction(best_prompt: str, best_score: float) -> str:
    fallback_prompt = best_prompt
    # auto generate new prompt
    llm_output = call_llm(OPTIMIZER_PROMPT)
    
    regex = re.compile(
        r'\[NEW INSTRUCTION START\]\s*(.*?)\s*\[NEW INSTRUCTION END\]', 
        re.DOTALL | re.IGNORECASE
    )
    match = regex.search(llm_output)
    
    if match:
        new_instruction = match.group(1).strip()
        if not new_instruction:
            print(f"\n[CRASH DIAGNOSIS] LLM outputted tags but NO content.")
            raise ValueError(f"CRASH: Prompt generation returned empty content within tags.")
        return new_instruction        
    
    print("\nprompt parse error: Tags not found in the output. RAW OUTPUT FOLLOWS:")
    print("-" * 50)
    # Print the raw output for diagnosis
    print(llm_output.strip() if llm_output else "[EMPTY OUTPUT STRING/NONE]")
    print("-" * 50)
    
    # Check if the LLM outputted text but just failed the format
    if llm_output.strip() and llm_output.strip() != fallback_prompt.strip():
        # If the output is new and non-empty, use it as the new prompt for one trial 
        # to see if it works, even if the format is wrong.
        return f"Please use this instruction: {llm_output.strip()}"

    return fallback_prompt