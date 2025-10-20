# GenAI assignment 1 for IEMS 490
(Sachin Venkatesh Thakku Saravana)

This repository contains the code and instructions to run Assignment 1 of IEMS 490, focusing on both manual and automated prompt engineering. I have implemented various strategies to improve the performance of both Gemini-2.5-flash and Gemini-2.0-flash-lite on a math problem-solving task using the Gemini API and the GSM8K dataset (subsampled to 300). All the files and datasets are self contained and can be run locally or inside a Docker container.

Related docker files and requirements included

## Brief outline

- baseline prompting with a simple prompt, not refined
- manual prompt engineering with two strategies: role assertion and chain of thought
  - role assertion: instructing the model to assume the role of an expert math tutor
  - chain of thought: guiding the model to reason step-by-step before providing the final answer
- automated prompt optimization using a basic optimization loop to iteratively refine the prompt based on validation performance

Drawbacks and difficulties faced: role assertion and chain of thought worked as expected with the latter showing a better score. However, the automated prompt optimization showed only a marginal improvement over the best manual prompt provided by chain of thought, indicating that the optimization strategy could be further refined for better results. I used both OPRO strategy, which did not yield significant improvements and would often get stuck or return no response due to API limitations, and a simpler iterative refinement approach that provided slight improvements but was still limited by the complexity of prompt design and the model's inherent capabilities. 

Neverthless, the experiments demonstrate the potential of prompt engineering in enhancing model performance on specific tasks and was a good learning experience as a first hands on project with GenAI models. I took the help of gemini-2.5 pro and copilot agent for code generation, albeit very limited.
	