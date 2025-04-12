import numpy as np
import pandas as pd
import fitz
from newspaper import Article
from sentence_transformers import SentenceTransformer, util
import io   # <<<---- ADD THIS LINE

# Step 1: Read Resume Text
def parse_resume(file_input):
    """
    Parses text from a PDF given a file path (string),
    an in-memory BytesIO object, or raw bytes.
    """
    resume_text = ""
    doc = None  # Initialize doc to None to ensure it can be closed in finally

    try:
        if isinstance(file_input, str):
            # Input is a file path string
            doc = fitz.open(file_input)
        elif isinstance(file_input, io.BytesIO):
            # Input is a BytesIO object (like from Streamlit upload)
            # Ensure the stream position is at the beginning
            file_input.seek(0)
            # Read the bytes from the BytesIO object and pass to stream
            doc = fitz.open(stream=file_input.read(), filetype="pdf")
        elif isinstance(file_input, bytes):
             # Input is raw bytes
             doc = fitz.open(stream=file_input, filetype="pdf")
        else:
            raise TypeError(f"Unsupported input type for parse_resume: {type(file_input)}")

        # Extract text from each page
        for page in doc:
            # page.get_text() is equivalent to page.get_text("text")
            resume_text += page.get_text()

    except Exception as e:
        # Log the error or handle it as needed
        print(f"Error processing PDF: {e}")
        # Re-raise the exception so the calling code (Streamlit app) knows there was an error
        raise
    finally:
        # IMPORTANT: Always close the document to free resources
        if doc:
            doc.close()

    return resume_text
# Step 2: Extract JD from URL or manual fallback
def extract_jd_text(url=None, manual_text=None):
    if url:
        try:
            print(f"\nTrying to extract JD from URL:\n{url}")
            article = Article(url)
            article.download()
            article.parse()
            jd_text = article.text.strip()
            if jd_text:
                print("✅ JD text successfully extracted from URL.\n")
                return jd_text
            else:
                raise ValueError("Empty text")
        except Exception as e:
            print(f"⚠️ Could not extract from URL: {e}")
    
    # Use manual input passed from Streamlit
    if manual_text:
        return manual_text.strip()

    return None



#Step 3: BERT Based Semantic Score

def compute_bert_similarity(resume_text, jd_text):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode([resume_text, jd_text], convert_to_tensor=True)
    similarity_score = util.cos_sim(embeddings[0], embeddings[1]).item()
    return similarity_score