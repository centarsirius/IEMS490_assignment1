from google import genai
import os 

MODEL_NAME = "gemini-2.0-flash-lite" 

try:
    CLIENT = genai.Client()
except Exception as e:
    raise RuntimeError(f"Failed to initialize Gemini Client. Is the GEMINI_API_KEY environment variable set? Error: {e}")

def call_llm(full_prompt: str) -> str:
    try:
        response = CLIENT.models.generate_content(
            model=MODEL_NAME,
            contents=full_prompt,
            config=genai.types.GenerateContentConfig(
                temperature=0.7, # high temeperature for creative generation
                max_output_tokens=4096 # sufficient length for detailed reasoning
            )
        )
        # check: return empty string if response.text is None
        return response.text if response.text is not None else ""
    except Exception as e:
        # API error message (rate limits primarily)
        print(f"\n--- API ERROR on question: {e} ---")
        return ""
    