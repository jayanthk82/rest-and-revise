# api/gemini_utils.py
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure the Gemini API key
try:
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
except TypeError:
    print("ERROR: GEMINI_API_KEY not found. Please add it to your .env file.")
    # You can choose to handle this more gracefully
    # For now, we'll allow it to proceed but API calls will fail.

def generate_resume_html(user_data, job_description):
    """
    Uses the Gemini API to generate a professional resume in HTML format.

    Args:
        user_data (dict): A dictionary containing the user's skills, experience, etc.
        job_description (str): The text of the job description to tailor the resume to.

    Returns:
        str: A string containing the full HTML of the generated resume.
    """
    model = genai.GenerativeModel('gemini-1.5-flash')

    # This is a detailed prompt that tells the model exactly what to do.
    # We can refine this over time to improve the resume quality.
    prompt = f"""
    You are an expert, ATS-friendly resume writer. Your task is to generate a complete, professional resume in a single, clean HTML document.

    Use the following user data and job description to tailor the content. The resume should highlight the user's skills and experiences that are most relevant to the job.

    **User Data:**
    ---
    {user_data}
    ---
    **Job Description:**
    ---
    {job_description}
    ---

    **Instructions:**
    - The output must be a single block of HTML code. Do not include any text outside of the HTML.
    - Use standard, semantic HTML tags (e.g., `<h1>`, `<h2>`, `<h3>`, `<p>`, `<ul>`, `<li>`).
    - Do not include `<head>` or `<body>` tags, only the content.
    - Create sections for "Summary", "Skills", "Experience", and "Projects".
    - For each project, create a compelling bullet point that demonstrates impact, using the STAR method if possible.
    """

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"An error occurred with the Gemini API: {e}")
        # Return a simple HTML error message
        return "<h1>Error: Could not generate resume.</h1>"