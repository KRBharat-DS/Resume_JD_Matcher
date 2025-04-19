# src/LLM/client.py

import google.generativeai as genai
import os
from dotenv import load_dotenv

print("DEBUG: Starting src.LLM.client execution...") # Add print at very top

load_dotenv()
api_key = os.getenv("GEMAI_API_KEY")
model = None

if not api_key:
    print("ERROR in client.py: GEMAI_API_KEY environment variable not found.")
    # --- RAISE AN ERROR ---
    # This will stop execution and show up clearly
    raise ValueError("CRITICAL: GEMAI_API_KEY environment variable not found. Please check your .env file.")
else:
    try:
        print("DEBUG in client.py: API Key found. Configuring Google GenAI...")
        genai.configure(api_key=api_key)

        print("DEBUG in client.py: Instantiating Gemini model...")
        # Ensure the model name is correct and available to your key
        model = genai.GenerativeModel("gemini-1.5-pro-latest")
        print("✅ SUCCESS in client.py: Gemini client configured and model instantiated.")

    except Exception as e:
        print(f"ERROR in client.py: Failed to configure/instantiate Gemini model. Exception: {e}")
        # --- RAISE AN ERROR ---
        # Wrap the original exception for more context
        raise RuntimeError(f"CRITICAL: Failed to configure/instantiate Gemini model: {e}") from e

def get_model():
    """Returns the instantiated GenerativeModel object, or None if setup failed."""
    # This function now primarily relies on whether 'model' was successfully assigned above.
    # The explicit checks for None happen where get_model() is called (e.g., in matcher.py)
    print(f"DEBUG: get_model() called. Returning model object (type: {type(model)}).") # See what type it is
    return model

print("DEBUG: Finished src.LLM.client execution.") # Add print at very end
