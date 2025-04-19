# streamlit_app.py - MINIMAL TEST WITH IMPORTS

import streamlit as st # <--- MOVE THIS TO THE TOP
import os
import io
import sys
import inspect

# --- Keep Path Setup ---
try:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = script_dir
    src_path = os.path.join(project_root, 'src')
    if os.path.isdir(src_path):
        if src_path not in sys.path:
            sys.path.insert(0, src_path)
        # print(f"INFO: Successfully added '{src_path}' to sys.path.") # Optional print
    else:
        print(f"ERROR: Calculated src directory does not exist: {src_path}")
except NameError:
    print("Warning: __file__ not defined. Path setup might be incomplete.")
# --- End Path Setup ---


# --- Imports ---
try:
    from parsing.resume_parser import parse_resume
    from parsing.jd_parser import jd_parser
    from matching.matcher import compute_embedding_similarity
    from matching.matcher import match_resume_with_jd_llm
    from matching.matcher import improve_resume_text
    print("✅ Successfully imported backend functions (in minimal test).")
except ImportError as e:
    # This st.error() can now run because 'st' is defined above
    st.error(f"Import Error: {e}")
    st.stop() # Stop if imports fail
except Exception as e:
    st.error(f"Other Error during import: {e}")
    st.stop() # Stop if imports fail




# --- Streamlit App UI ---


st.title("📄➡️🎯 Resume & Job Description Matcher")

# --- Section 1: Resume Input ---
st.subheader("1. Upload Resume (PDF)")
# File uploader widget
resume_file = st.file_uploader("Choose a resume PDF file", type="pdf", key="resume_uploader")

# Initialize resume_text in session state if it doesn't exist
if 'resume_text' not in st.session_state:
    st.session_state.resume_text = None
    st.session_state.resume_filename = None # Also store filename

# Process the uploaded file
if resume_file is not None:
    # Check if it's a new file or the same one
    if st.session_state.resume_filename != resume_file.name:
        st.info(f"Processing uploaded resume: {resume_file.name}")
        try:
            # Use BytesIO to handle the uploaded file object in memory
            resume_bytes = io.BytesIO(resume_file.getvalue())
            # Call the parsing function from your backend
            st.session_state.resume_text = parse_resume(resume_bytes)
            st.session_state.resume_filename = resume_file.name # Store filename to prevent reprocessing
            st.success("✅ Resume parsed successfully!")
            # Optionally display a snippet of the parsed text for verification
            # with st.expander("Parsed Resume Text (Snippet)"):
            #    st.text(st.session_state.resume_text[:500] + "...")
        except Exception as e:
            st.error(f"❌ Error parsing resume PDF: {e}")
            # Reset state on error
            st.session_state.resume_text = None
            st.session_state.resume_filename = None
# Handle file removal by user
elif st.session_state.resume_filename is not None:
     st.info("Resume file removed.")
     st.session_state.resume_text = None
     st.session_state.resume_filename = None


# --- Section 2: Job Description Input ---
st.subheader("2. Provide Job Description")
st.write("Enter a URL **OR** paste the text below:")

# Use columns for better layout
col1, col2 = st.columns([1, 2]) # Give more space to text area

with col1:
    jd_url_input = st.text_input("Enter URL for JD (Optional)", "", key="jd_url", placeholder="e.g., https://jobs.example.com/...")

with col2:
    jd_text_area_input = st.text_area("Paste JD Text Here (If no URL or URL fails)", "", height=200, key="jd_text_area", placeholder="Paste the full job description text here...")

# --- Section 3: Matching ---
st.subheader("3. Analyze Match")
st.write("Click the button below to compare the parsed resume against the provided job description.")

# Match button
if st.button("🔍 Analyze Resume-JD Match", key="match_button"):

    # --- Input Validation ---
    # Retrieve parsed resume text from session state
    resume_text = st.session_state.get('resume_text', None)

    # Check if resume has been successfully parsed
    if not resume_text:
        st.error("❌ Please upload and successfully parse a resume PDF first.")
        st.stop() # Stop execution for this button click if no resume

    # --- Determine and Extract JD Text ---
    final_jd_text = None # Initialize JD text variable
    # Prioritize manually pasted text
    if jd_text_area_input:
        st.info("ℹ️ Using manually pasted text for Job Description.")
        final_jd_text = jd_text_area_input.strip() # Use stripped text
    # Fallback to URL if text area is empty but URL is provided
    elif jd_url_input:
        st.info(f"ℹ️ Attempting to fetch Job Description from URL: {jd_url_input}")
        try:
            # Call your extraction function (ensure it handles potential errors)
            with st.spinner("Fetching and parsing JD from URL..."):
                final_jd_text = jd_parser(url=jd_url_input) # Assumes extract_jd_text handles URL fetching

            # Check if extraction was successful
            if not final_jd_text or not final_jd_text.strip():
                 st.warning(f"⚠️ Could not extract meaningful text from URL. Please check the URL or paste the text manually.")
                 # Don't stop here, allow user to paste manually if desired.
                 # Consider clearing the URL input or giving specific feedback.
            else:
                st.success("✅ Successfully fetched and parsed JD from URL.")
                # Optionally display snippet
                # with st.expander("Parsed JD Text (Snippet from URL)"):
                #    st.text(final_jd_text[:500] + "...")

        except Exception as e:
            # Catch errors during URL fetching/parsing
            st.error(f"❌ Error fetching or parsing JD from URL: {e}")
            st.warning("Please check the URL or paste the JD text into the text area.")
            # Don't stop, user might still want to use pasted text if they add it now.
    else:
        # If neither URL nor text area has input
        st.error("❌ Please provide a Job Description either via URL or by pasting the text.")
        st.stop() # Stop execution if no JD source is provided

    # --- Perform Analysis if both texts are available ---
    if resume_text and final_jd_text and final_jd_text.strip():
        st.markdown("---") # Separator
        st.subheader("📊 Matching Analysis Results")

        # --- Analysis 1: Embedding Similarity ---
        try:
            with st.spinner('Calculating semantic similarity score...'):
                similarity_score = compute_embedding_similarity(resume_text, final_jd_text)

            if similarity_score is not None:
                # Display score as percentage using st.metric
                st.metric(label="Semantic Similarity Score (Embeddings)", value=f"{similarity_score*100:.2f}%",
                          help="Measures how similar the overall meaning of the resume and JD are, based on sentence embeddings (0-100%). Higher is generally better.")
            else:
                st.warning("⚠️ Could not calculate embedding similarity score.")

        except Exception as e:
            st.error(f"An error occurred during similarity calculation: {e}")

        # --- Analysis 2: Common Keywords (Placeholder) ---
        # st.subheader("🔑 Common Keywords (Simple Overlap)") # Optional section
        # try:
        #     common_keywords = get_common_keywords(resume_text, final_jd_text)
        #     st.write(common_keywords)
        # except Exception as e:
        #     st.error(f"Error calculating common keywords: {e}")

        # --- Analysis 3: LLM (Gemini) Detailed Match ---
        try:
            with st.spinner('Asking AI Assistant (Gemini) for detailed analysis...'):
                 # *** Use the correct function name from your backend ***
                 # Using 'match_resume_with_jd' as per your import list,
                 # but 'match_resume_with_jd_llm' might be more accurate.
                llm_result = match_resume_with_jd_llm(resume_text, final_jd_text)

            st.subheader("🤖 AI Assistant Analysis (Gemini)")
            if llm_result:
                # Use markdown to render potential formatting from the LLM
                st.markdown(llm_result, unsafe_allow_html=True) # Allow basic HTML if needed for formatting like lists
            else:
                st.warning("⚠️ AI analysis returned no result. The LLM might be unavailable or encountered an issue.")

        except Exception as e:
            st.error(f"❌ Error during AI analysis: {e}")

    elif resume_text and (not final_jd_text or not final_jd_text.strip()):
        # If resume is ready but JD failed or is empty after trying
        st.warning("⚠️ Cannot perform analysis because the Job Description text is missing or could not be obtained.")


# --- Section 4: Resume Improvement ---
st.markdown("---") # Separator
st.subheader("✨ Improve Your Resume (AI Assistant)")

# Retrieve resume text again, in case it was parsed in a previous run
current_resume_text = st.session_state.get('resume_text', None)

if current_resume_text:
    st.write("Get suggestions from the AI Assistant on how to tailor your resume based *only* on its content (does not use the JD here).")
    # Improve button
    if st.button("💡 Suggest Resume Improvements", key="improve_button"):
        try:
            with st.spinner("AI Assistant is thinking about improvements..."):
                # Call the backend function for resume improvement
                # *** Ensure 'improve_resume_text' exists and works ***
                improved_text = improve_resume_text(current_resume_text)

            st.subheader("📝 AI-Suggested Improvements")
            if improved_text:
                # Display suggestions in a text area or markdown
                st.markdown(improved_text, unsafe_allow_html=True)
            else:
                st.warning("⚠️ AI Assistant returned no improvement suggestions.")
        except NameError:
             st.error("❌ The 'improve_resume_text' function is not defined or imported correctly.")
        except Exception as e:
            st.error(f"❌ Error during resume improvement: {e}")
else:
    # Show info if no resume is loaded
    st.info("ℹ️ Please upload a resume first to enable the improvement feature.")

# --- Footer or Additional Info ---
st.markdown("---")
st.caption("Powered by Streamlit, Gemini, and Sentence Transformers.")
