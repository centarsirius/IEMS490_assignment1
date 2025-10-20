import re

FORMATTING_INSTRUCTION = "\nOutput the final answer at the end with the prefix ####. For example: #### 123"

def parse_answer(text: str) -> str:
    # check: return empty string if input is invalid
    if not isinstance(text, str) or not text:
        return ""
        
    # regex to find the prefix #### and optional spaces or symbols
    match = re.search(r'####\s*([0-9\.\/,\$]+)', text)
    if match:
        # Clean the extracted text by removing common separators
        answer = match.group(1).replace(',', '').replace('$', '').strip()
        return answer
    return "" # check: return empty string if no match found

def extract_ground_truth(gsm8k_answer_field: str) -> str:
    match = re.search(r'####\s*([0-9\.\/]+)', gsm8k_answer_field)
    if match:
        return match.group(1).replace(',', '').strip()
    return ""

def score_math_answer(llm_output: str, ground_truth_answer_field: str) -> bool:
    """
    Compares the parsed LLM answer against the ground truth.
    """
    llm_ans_str = parse_answer(llm_output)
    gt_ans_str = extract_ground_truth(ground_truth_answer_field)

    if not llm_ans_str or not gt_ans_str:
        return False

    # check: convert to float for numerical comparison (5.0 == 5)
    try:
        return float(llm_ans_str) == float(gt_ans_str)
    except ValueError:
        # if conversion fails, fall back to string comparison
        return llm_ans_str == gt_ans_str