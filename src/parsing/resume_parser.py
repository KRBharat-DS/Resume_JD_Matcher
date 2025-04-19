# Import the PyMuPDF library, commonly imported as fitz
import fitz
# Import the io library, needed for handling in-memory byte streams like uploaded files
import io

# Define the function to parse the resume, accepting various input types
def parse_resume(file_input):
    """
    Parses text from a PDF file.

    Accepts various input types for flexibility:
    - A file path (string) to the PDF file.
    - An in-memory BytesIO object (commonly from file uploads like Streamlit).
    - Raw bytes representing the PDF content.

    Args:
        file_input (str | io.BytesIO | bytes): The source of the PDF data.

    Returns:
        str: The extracted text content from all pages of the PDF.

    Raises:
        TypeError: If the input type is not supported.
        Exception: Re-raises exceptions encountered during PDF processing (e.g., corrupted file).
    """
    # Initialize an empty string to accumulate text from all pages
    resume_text = ""
    # Initialize the document object to None. This ensures we can safely check
    # if it needs closing in the 'finally' block, even if opening fails.
    doc = None

    try:
        # --- Input Type Handling ---
        if isinstance(file_input, str):
            # If input is a string, assume it's a file path
            print("Processing PDF from file path...") # Added print for clarity during execution
            doc = fitz.open(file_input)
        elif isinstance(file_input, io.BytesIO):
            # If input is a BytesIO object (typical for Streamlit uploads)
            print("Processing PDF from BytesIO stream...") # Added print for clarity
            # IMPORTANT: Ensure the stream's read pointer is at the beginning.
            # Uploaded file objects might have been read previously.
            file_input.seek(0)
            # Read the entire content of the BytesIO stream into memory as bytes
            pdf_bytes = file_input.read()
            # Open the PDF document from the byte stream
            doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        elif isinstance(file_input, bytes):
             # If input is already raw bytes
             print("Processing PDF from raw bytes...") # Added print for clarity
             # Open the PDF document directly from the byte stream
             doc = fitz.open(stream=file_input, filetype="pdf")
        else:
            # If the input type is none of the above, raise an error
            raise TypeError(f"Unsupported input type for parse_resume: {type(file_input)}")

        # --- Text Extraction ---
        # Iterate through each page in the opened PDF document
        print(f"Extracting text from {len(doc)} pages...") # Added print for progress
        for page_num, page in enumerate(doc): # Using enumerate for potential page-specific logging
            # Extract text from the current page.
            # page.get_text() extracts plain text. Other options exist like "html", "dict", etc.
            page_text = page.get_text()
            resume_text += page_text
            # Optional: Add a separator between pages if needed, e.g., resume_text += "\n--- Page Break ---\n"
            # print(f"  Extracted text from page {page_num + 1}") # Uncomment for detailed logging

    except Exception as e:
        # If any error occurs during the try block (opening, reading, processing)
        print(f"Error processing PDF: {e}")
        # Re-raise the exception. This allows the calling code (e.g., Streamlit app)
        # to know that processing failed and handle it appropriately (e.g., show user error).
        raise
    finally:
        # --- Resource Cleanup ---
        # This block executes regardless of whether an exception occurred or not.
        # It's crucial for releasing resources like file handles.
        if doc:
            print("Closing PDF document.") # Added print for clarity
            # If the document object was successfully created, close it.
            doc.close()

    # Return the accumulated text from all pages
    print("PDF parsing complete.") # Added print for clarity
    return resume_text

# Example Usage (optional, for testing this script directly)
# if __name__ == '__main__':
#     # Example 1: Using a file path
#     try:
#         text_from_path = parse_resume("path/to/your/resume.pdf") # Replace with a real path
#         print("\n--- Text from Path ---")
#         print(text_from_path[:500]) # Print first 500 chars
#     except Exception as e:
#         print(f"Failed to process from path: {e}")

#     # Example 2: Simulating a BytesIO upload
#     try:
#         with open("path/to/your/resume.pdf", "rb") as f: # Replace with a real path
#             bytes_io_obj = io.BytesIO(f.read())
#         text_from_stream = parse_resume(bytes_io_obj)
#         print("\n--- Text from BytesIO ---")
#         print(text_from_stream[:500]) # Print first 500 chars
#     except Exception as e:
#         print(f"Failed to process from BytesIO: {e}")
