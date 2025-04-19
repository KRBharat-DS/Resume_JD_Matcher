import sys
import os
import pprint

print("-" * 30)
print("DEBUG: INSIDE matcher.py - TOP LEVEL")
try:
    # Calculate paths relative to *this* file (matcher.py)
    matcher_file_path = os.path.abspath(__file__)
    matching_dir = os.path.dirname(matcher_file_path)
    src_dir = os.path.abspath(os.path.join(matching_dir, '..')) # Go up one level to src
    llm_dir = os.path.join(src_dir, 'LLM')
    llm_init_file = os.path.join(llm_dir, '__init__.py')
    llm_client_file = os.path.join(llm_dir, 'client.py')
    src_init_file = os.path.join(src_dir, '__init__.py')

    print(f"DEBUG (matcher.py): My path is: {matcher_file_path}")
    print(f"DEBUG (matcher.py): Calculated src dir: {src_dir}")
    print(f"DEBUG (matcher.py): Calculated LLM dir: {llm_dir}")
    print(f"DEBUG (matcher.py): Does src dir exist? {os.path.isdir(src_dir)}")
    print(f"DEBUG (matcher.py): Does src/__init__.py exist? {os.path.isfile(src_init_file)}")
    print(f"DEBUG (matcher.py): Does LLM dir exist? {os.path.isdir(llm_dir)}")
    print(f"DEBUG (matcher.py): Does LLM/__init__.py exist? {os.path.isfile(llm_init_file)}")
    print(f"DEBUG (matcher.py): Does LLM/client.py exist? {os.path.isfile(llm_client_file)}")
    print(f"DEBUG (matcher.py): Is src dir in sys.path? {src_dir in sys.path}")
    print("DEBUG (matcher.py): Current sys.path:")
    pprint.pprint(sys.path)

except Exception as debug_e:
    print(f"DEBUG (matcher.py): Error during path debugging: {debug_e}")
print("-" * 30)
# --- End Debug Block ---


# --- Original Imports ---
from sentence_transformers import SentenceTransformer, util
# ... other imports needed by matcher.py ...


# --- Import LLM model getter ---
get_model = None # Initialize to None
try:
    # Try absolute import from src directory (since src is in sys.path)
    print("DEBUG (matcher.py): Attempting absolute import: from LLM.client import get_model") # Keep this print
    from llm.client import get_model
    print("✅ Successfully imported 'get_model' from LLM.client using absolute path in matcher.py.")

except ImportError as e:
    # Make the error message more specific here
    print(f"ERROR (matcher.py): Failed absolute import 'from LLM.client import get_model'. Error: {e}. LLM features will be unavailable.")
    # get_model remains None
except Exception as e:
    # Catch any other unexpected error during import
    print(f"An unexpected error occurred during import of get_model in matcher.py: {e}")
    # get_model remains None

# --- Sentence Transformer Model Loading ---
# Load the Sentence Transformer model ONCE when the module is loaded.
# This is much more efficient than loading it inside the function every time it's called.
# 'all-MiniLM-L6-v2' is a good starting point - fast and reasonably accurate for semantic similarity.
embedding_model = None # Initialize to None
try:
    print("Loading Sentence Transformer model (all-MiniLM-L6-v2)...")
    # Wrap model loading in try-except in case download or loading fails
    embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
    print("✅ Sentence Transformer model loaded successfully.")
except Exception as e:
    print(f"Error loading Sentence Transformer model: {e}. Embedding similarity will not be available.")
    # embedding_model remains None if loading fails


# --- Function 1: Numerical Embedding Similarity ---
def compute_embedding_similarity(resume_text, jd_text):
    """
    Computes the semantic similarity between resume and job description text
    using sentence embeddings (SentenceTransformer model).

    Args:
        resume_text (str): The text content of the resume.
        jd_text (str): The text content of the job description.

    Returns:
        float | None: The cosine similarity score (typically between 0.0 and 1.0 for text),
                      or None if the embedding model failed to load or an error occurs during computation.
    """
    # Check if the embedding model was loaded successfully during module import
    if embedding_model is None:
        print("Error: Sentence Transformer model not available for similarity computation.")
        return None # Return None if model isn't loaded

    # Ensure inputs are strings
    if not isinstance(resume_text, str) or not isinstance(jd_text, str):
        print("Error: Both resume_text and jd_text must be strings.")
        return None

    try:
        print("Encoding resume and JD text for similarity calculation...")
        # Encode both texts into vector embeddings. convert_to_tensor=True is efficient for util.cos_sim.
        embeddings = embedding_model.encode([resume_text, jd_text], convert_to_tensor=True)

        # Calculate the cosine similarity between the two embeddings
        # embeddings[0] is the resume embedding, embeddings[1] is the JD embedding
        # .item() extracts the scalar value from the resulting tensor (e.g., tensor([[0.75]]))
        similarity_score = util.cos_sim(embeddings[0], embeddings[1]).item()
        print(f"Computed embedding similarity score: {similarity_score:.4f}")

        # Ensure score is within expected range (cosine sim is -1 to 1, but for text often 0-1)
        # Clamping might be useful if you want to strictly enforce a 0-1 range for display
        # similarity_score = max(0.0, min(1.0, similarity_score))

        return similarity_score # Return the calculated float score

    except Exception as e:
        print(f"Error computing embedding similarity: {e}")
        return None # Return None if an error occurs during encoding/similarity calculation


# --- Function 2: LLM-based Matching Analysis ---
def match_resume_with_jd_llm(resume_text, jd_text):
    """
    Uses a Generative Language Model (Gemini) to analyze the match between
    a resume and a job description, providing a score, explanation, and missing factors.

    Args:
        resume_text (str): The text content of the resume.
        jd_text (str): The text content of the job description.

    Returns:
        str | None: The analysis text generated by the LLM, or None if the LLM
                    model is not available or an error occurs during generation.
    """
    # Check if the LLM model was successfully retrieved or instantiated earlier.
    # Re-check here in case client.py runs after this module is imported.
    current_llm_model = get_model() # Call get_model again to get the latest state

    if not current_llm_model:
        print("Error: LLM model not available. Cannot perform LLM-based matching.")
        return None

    # Ensure inputs are strings
    if not isinstance(resume_text, str) or not isinstance(jd_text, str):
        print("Error: Both resume_text and jd_text must be strings for LLM analysis.")
        return None

    # Define the prompt for the LLM
    # This prompt guides the LLM to act as a recruiter and provide specific outputs.
    # Using clear formatting and instructions improves the reliability of the output.
    prompt = f"""
    Analyze the following resume and job description. Act as an expert talent acquisition specialist providing a concise evaluation for a hiring manager.

    **Resume Text:**
    ---
    {resume_text}
    ---

    **Job Description Text:**
    ---
    {jd_text}
    ---

    **Your Task:**
    1.  Provide an overall **Match Score** (out of 100) representing the candidate's suitability based *only* on the provided texts. Base the score on how well the resume demonstrates the qualifications and experience listed in the job description.
    2.  Write a brief **Explanation** (2-4 sentences) justifying the score, highlighting key alignments or significant gaps.
    3.  List the most critical **Missing Factors** (specific keywords, skills, qualifications, or years of experience mentioned in the JD but seemingly absent or insufficient in the candidate's resume). If there are no significant missing factors, state "None apparent." Use bullet points for the list.
    4.  Refer to the person who submitted the resume only as "the candidate" or "the applicant". Do not invent or use a name found in the resume text.

    **Output Format:**
    Strictly follow this format, including the labels:

    Match Score: [Score]/100
    Explanation: [Your explanation here]
    Missing Factors:
    * [Missing factor 1]
    * [Missing factor 2]
    * [Or "None apparent."]
    """

    try:
        print("Sending request to LLM for resume-JD analysis...")
        # Send the prompt to the Gemini model instance retrieved earlier
        response = current_llm_model.generate_content(prompt)

        # Basic check if response has text (some APIs might return empty responses on errors/filters)
        if hasattr(response, 'text') and response.text:
             analysis_text = response.text
             print("✅ LLM analysis received.")
             return analysis_text
        else:
             # Handle cases where the response might be blocked or empty
             print("⚠️ LLM response received but contains no text. It might have been blocked or empty.")
             # Check for safety ratings or prompt feedback if available
             if hasattr(response, 'prompt_feedback'):
                 print(f"Prompt Feedback: {response.prompt_feedback}")
             return "Error: LLM response was empty or blocked. Please check content safety settings or modify input."


    except Exception as e:
        # Handle potential errors during the API call (e.g., network issues, API errors, quota limits)
        print(f"Error generating LLM response for matching: {e}")
        return f"Error during LLM analysis: {e}" # Return error message for debugging


