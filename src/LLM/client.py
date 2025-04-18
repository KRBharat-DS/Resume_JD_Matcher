# Import the Google Generative AI library
import google.generativeai as genai
# Import the os library to access environment variables
import os
# Import the function to load environment variables from a .env file
from dotenv import load_dotenv

# --- Load Environment Variables ---
# Load variables from the .env file into the environment.
# This should be called early, ideally once at the start of the application or module.
# Make sure you have a .env file in your project root with GEMAI_API_KEY=your_actual_key
load_dotenv()

# --- Get API Key ---
# Retrieve the API key from the environment variables.
# Using os.getenv is the secure way to handle secrets, avoiding hardcoding.
# Ensure the variable name "GEMAI_API_KEY" matches exactly what's in your .env file.
api_key = os.getenv("GEMAI_API_KEY")

# --- API Key Validation and Configuration ---
# Initialize the model variable to None. It will be set only if the API key is valid.
model = None

if not api_key:
    # If the API key was not found in the environment variables
    # Print an error message. Using st.error() in the main Streamlit app would be better for user feedback.
    # *** Correction: The error message mentions OPENAI_API_KEY, but you are loading GEMAI_API_KEY. Update the message. ***
    print("Error: GEMAI_API_KEY environment variable not found.")
    # Depending on the application structure, you might raise an Exception here
    # raise ValueError("GEMAI_API_KEY not found. Please set the environment variable.")
    # Or handle it in the calling code (e.g., disable LLM features in Streamlit)

else:
    # If the API key was found successfully
    try:
        # Configure the Google Generative AI library with the retrieved API key.
        # This step authenticates your requests to the Gemini API.
        print("GEMAI_API_KEY loaded. Configuring Google Generative AI...") # Added print statement
        genai.configure(api_key=api_key)

        # --- Instantiate the Model ---
        # Create an instance of the desired Gemini model.
        # "gemini-1.5-pro-latest" is a powerful model, ensure it fits your usage needs and budget.
        # Other models like "gemini-pro" might also be suitable depending on the task.
        print("Instantiating Gemini model (gemini-1.5-pro-latest)...") # Added print statement
        model = genai.GenerativeModel("gemini-1.5-pro-latest")
        print("✅ Google Generative AI client configured and model instantiated successfully.")

    except Exception as e:
        # Catch potential errors during configuration or model instantiation
        # (e.g., invalid API key format, network issues connecting to Google)
        print(f"Error configuring Google Generative AI or instantiating model: {e}")
        # Ensure the model remains None if configuration fails
        model = None

# --- Optional: Function to get the model ---
# This can be helpful if other modules need to access the configured model.
def get_model():
    """Returns the instantiated GenerativeModel object, or None if setup failed."""
    if not model:
        print("Warning: get_model() called, but the model is not configured/instantiated.")
    return model

# Example Usage (optional, for testing this script directly)
# if __name__ == '__main__':
#     test_model = get_model()
#     if test_model:
#         print("\n--- Model Object ---")
#         print(test_model)
#         # You could potentially try a simple generation here for a full test,
#         # but be mindful of API costs.
#         # try:
#         #     response = test_model.generate_content("Explain what an LLM is in one sentence.")
#         #     print("\n--- Test Generation ---")
#         #     print(response.text)
#         # except Exception as e:
#         #     print(f"Test generation failed: {e}")
#     else:
#         print("\n--- Model Not Available ---")

