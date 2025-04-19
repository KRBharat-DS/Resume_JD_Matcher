# Import the Article class from the newspaper3k library
# newspaper3k is designed to extract article text from web pages
from newspaper import Article
# Note: You'll need to have run 'pip install newspaper3k'
# And potentially 'pip install nltk' and run 'python -m nltk.downloader punkt'
# if newspaper3k requires the NLTK tokenizer data.

def jd_parser(url=None, manual_text=None):
    """
    Extracts Job Description text either from a URL or from manually provided text.

    It prioritizes extracting from the URL if provided. If URL extraction fails
    or no URL is given, it falls back to using the manual_text if available.

    Args:
        url (str, optional): The URL of the job description page. Defaults to None.
        manual_text (str, optional): Manually pasted job description text. Defaults to None.

    Returns:
        str | None: The extracted job description text (stripped of leading/trailing whitespace),
                    or None if neither method yields text.
    """

    # --- Attempt 1: Extract from URL ---
    if url:
        try:
            print(f"\nAttempting to extract JD from URL: {url}")
            # Create an Article object with the given URL
            article = Article(url)
            # Download the HTML content of the page
            # This might raise network-related exceptions
            article.download()
            # Parse the downloaded HTML to extract the main article content
            # This uses newspaper3k's algorithms to find the relevant text block
            article.parse()
            # Get the extracted text and remove leading/trailing whitespace
            jd_text = article.text.strip()

            # Check if any text was actually extracted
            if jd_text:
                print("✅ JD text successfully extracted from URL.")
                # If text was found, return it immediately
                return jd_text
            else:
                # If parsing succeeded but resulted in empty text, raise an error
                # This helps differentiate from download/parse failures in the except block
                raise ValueError("Extracted text from URL was empty.")

        except Exception as e:
            # Catch any exception during the download/parse process (network error, parsing error, ValueError from above)
            # newspaper3k might not work on all websites (e.g., heavy JS, anti-scraping measures)
            print(f"⚠️ Could not extract text from URL '{url}'. Reason: {e}")
            # Do not return here; proceed to check for manual_text as a fallback

    # --- Attempt 2: Use Manual Text ---
    # This part is reached if:
    #   a) No URL was provided initially.
    #   b) URL was provided, but an exception occurred during processing.
    if manual_text:
        print("ℹ️ Using manually provided text as JD.")
        # If manual_text exists, strip whitespace and return it
        return manual_text.strip()

    # --- Failure Case ---
    # This part is reached if no URL was given AND no manual_text was given,
    # OR if URL extraction failed AND no manual_text was given.
    print("❌ No JD text could be obtained either from URL or manual input.")
    return None

# Example Usage (optional, for testing this script directly)
# if __name__ == '__main__':
#     # Example 1: Valid URL (replace with a real job posting URL)
#     # test_url = "https://jobs.lever.co/openai/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx" # Example structure
#     # jd1 = extract_jd_text(url=test_url)
#     # if jd1:
#     #     print("\n--- JD from URL ---")
#     #     print(jd1[:500] + "...")
#     # else:
#     #     print("\n--- JD from URL Failed ---")

#     # Example 2: Invalid URL / URL extraction fails
#     test_url_bad = "https://this.url.does.not.exist.xyz"
#     jd2 = extract_jd_text(url=test_url_bad)
#     if jd2:
#         print("\n--- JD from Bad URL (Should not happen often) ---")
#         print(jd2[:500] + "...")
#     else:
#         print("\n--- JD from Bad URL Failed (Expected) ---")


#     # Example 3: Manual Text Input
#     manual_jd = """
#     Job Title: Software Engineer
#     Location: Remote

#     We are looking for a skilled software engineer to join our team.
#     Responsibilities include developing and maintaining web applications.
#     Requires 3+ years of experience with Python and Django.
#     """
#     jd3 = extract_jd_text(manual_text=manual_jd)
#     if jd3:
#         print("\n--- JD from Manual Text ---")
#         print(jd3)
#     else:
#         print("\n--- JD from Manual Text Failed ---")


#     # Example 4: URL fails, but manual text is provided
#     jd4 = extract_jd_text(url=test_url_bad, manual_text=manual_jd)
#     if jd4:
#         print("\n--- JD from Failed URL + Manual Text ---")
#         print(jd4)
#     else:
#         print("\n--- JD from Failed URL + Manual Text Failed ---")

#     # Example 5: No input provided
#     jd5 = extract_jd_text()
#     if jd5:
#         print("\n--- JD from No Input (Should not happen) ---")
#         print(jd5)
#     else:
#         print("\n--- JD from No Input Failed (Expected) ---")
