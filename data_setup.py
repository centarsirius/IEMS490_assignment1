from datasets import load_dataset
import random
import os

def load_and_sample_gsm8k(sample_size=300, seed=42):
    """Loads the GSM8K dataset and returns a sub-sample."""
    # Load train split
    dataset = load_dataset("openai/gsm8k", "main", split="train")

    random.seed(seed)
    sampled_indices = random.sample(range(len(dataset)), sample_size)
    sampled_data = dataset.select(sampled_indices).to_list()

    print(f"Sampling {len(sampled_data)} questions.")
    return sampled_data

# Test the data loading and sampling function
# if __name__ == '__main__':
#     sample = load_and_sample_gsm8k(sample_size=5)
#     print("\nExample data point structure:")
#     print(f"Question: {sample[1]['question']}")
#     print(f"Ground Truth Answer (Raw): {sample[1]['answer']}")