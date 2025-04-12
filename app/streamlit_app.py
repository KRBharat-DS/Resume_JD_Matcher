import pandas as pd
import numpy as np
import streamlit as st
import io
import os
import sys
import inspect

# --- Path Setup (Good as is) ---
try:
    current_file_path = os.path.abspath(inspect.getfile(inspect.currentframe()))
    project_root = os.path.abspath(os.path.join(os.path.dirname(current_file_path), '..'))
except TypeError:
    print("Warning: Could not determine script path automatically. Assuming current working directory is project root or similar context.")
    project_root = os.getcwd()

src_path = os.path.join(project_root, 'src')
if src_path not in sys.path:
    sys.path.insert(0, src_path)

try:
    # Assuming these functions exist in your src/utils.py
    from utils import parse_resume, compute_bert_similarity, extract_jd_text
except ImportError as e:
    st.error(f"Failed to import utility functions: {e}")
    st.stop() # Stop execution if core functions can't be imported

# --- Placeholder for missing function ---
def get_common_keywords(text1, text2, n=10):
    """Placeholder function for common keywords."""
    # In a real scenario, implement TF-IDF, CountVectorizer, or simple word overlap
    words1 = set(text1.lower().split())
    words2 = set(text2.lower().split())
    common = list(words1.intersection(words2))
    # Return top N or implement more sophisticated logic
    return ", ".join(common[:n]) if common else "N/A"

# --- Streamlit App UI ---

st.title("Resume & Job Description Matcher")

# Step 1: Upload Resume
st.subheader("1. Upload Resume (PDF)")
resume_file = st.file_uploader("Choose a resume file", type="pdf", key="resume_uploader")

# Initialize resume_text state
if 'resume_text' not in st.session_state:
    st.session_state.resume_text = None

# Parse resume immediately upon upload (or display error)
if resume_file is not None:
    try:
        # Use BytesIO to handle the uploaded file object directly
        resume_bytes = io.BytesIO(resume_file.getvalue())
        st.session_state.resume_text = parse_resume(resume_bytes) # Pass the BytesIO object
        # st.success("Resume parsed successfully!") # Optional feedback
    except Exception as e:
        st.error(f"Error parsing resume: {e}")
        st.session_state.resume_text = None # Reset on error
else:
    # Clear parsed text if file is removed
     st.session_state.resume_text = None


# Step 2: Input JD (Job Description)
st.subheader("2. Provide Job Description")
st.write("Enter a URL OR paste the text below:")
jd_url_input = st.text_input("Enter URL for JD (optional)", "", key="jd_url")
jd_text_area_input = st.text_area("Paste JD Text Here (if no URL provided)", "", height=200, key="jd_text_area")

# Step 3: Match Button and Results
st.subheader("3. Calculate Match")

if st.button("Match Resume to Job Description", key="match_button"):
    # --- Logic inside the button click ---
    final_jd_text = None
    resume_text = st.session_state.get('resume_text', None) # Get parsed resume text

    # Validate Resume Input
    if not resume_text:
        st.error("❌ Please upload and successfully parse a resume first.")
        st.stop() # Stop execution for this button click

    # --- Determine and Extract JD Text ---
    if jd_text_area_input:
        st.info("Using text pasted in the text area for JD.")
        final_jd_text = jd_text_area_input
    elif jd_url_input:
        st.info(f"Attempting to fetch JD from URL: {jd_url_input}")
        try:
            # Call your extraction function ONLY here
            final_jd_text = extract_jd_text(url=jd_url_input) # Assuming extract_jd_text handles URL fetching
            if not final_jd_text:
                 # Handle cases where extract_jd_text returns None/empty without error
                 st.error(f"❌ Could not extract text from URL. Please check the URL or paste the text manually.")
                 st.stop()
            # st.success("Successfully fetched and parsed JD from URL.") # Optional feedback
        except Exception as e:
            # Catch errors during URL fetching/parsing
            st.error(f"❌ Error fetching or parsing JD from URL: {e}")
            st.error("Please check the URL or paste the JD text into the text area.")
            st.stop() # Stop execution for this button click
    else:
        st.error("❌ Please provide a Job Description either via URL or by pasting the text.")
        st.stop() # Stop execution for this button click

    # --- Compute Similarity if both texts are available ---
    if resume_text and final_jd_text:
        try:
            with st.spinner('Calculating similarity...'):
                 # Compute similarity
                cosine_similarity_score = compute_bert_similarity(resume_text, final_jd_text)

                # Display Results
                st.subheader("📊 Matching Results")
                # Display score as percentage
                st.metric(label="Similarity Score", value=f"{cosine_similarity_score:.2%}") # Format as percentage

                # Common keywords (using the placeholder)
                st.subheader("🔑 Common Keywords/N-Grams (Simple Overlap)")
                common_keywords = get_common_keywords(resume_text, final_jd_text)
                st.write(common_keywords)

        except Exception as e:
            st.error(f"An error occurred during similarity calculation: {e}")

    # This else should theoretically not be reached due to earlier checks, but kept for safety
    # else:
    #     st.error("Could not proceed. Ensure both resume and JD are provided and processed.")