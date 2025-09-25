# api/job_api_utils.py
import requests
from urllib.parse import quote # 1. Import the quote function
from bs4 import BeautifulSoup # 1. Import BeautifulSoup


def fetch_job_listings(search_terms=list, page=2):
    """
    Fetches job listings from the Arbeitnow API.
    """
    query_string = " ".join(search_terms)
    encoded_query = quote(query_string)

    api_url = f"https://www.arbeitnow.com/api/job-board-api?search={encoded_query}&page={page}"
    
    try:
        response = requests.get(api_url)
        # This will raise an error if the request failed
        response.raise_for_status()
        
        data = response.json()
        raw_jobs = data.get("data", [])
        parsed_jobs = _parse_job_data(raw_jobs)

        return parsed_jobs # Return the list of jobs, or an empty list
        
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while calling the job API: {e}")
        return []

def _parse_job_data(raw_jobs: list) -> list:
    """
    A helper function to clean the raw job data.
    """
    parsed_jobs = []
    for job in raw_jobs:
        # 3. Use BeautifulSoup to parse the HTML description
        soup = BeautifulSoup(job.get("description", ""), "html.parser")

        # 4. Create a clean dictionary with only the data we need
        clean_job = {
            "title": job.get("title"),
            "company_name": job.get("company_name"),
            "location": job.get("location"),
            "url": job.get("url"),
            "clean_description": soup.get_text(separator="\n").strip(), # Extracts clean text
        }
        parsed_jobs.append(clean_job)

    return parsed_jobs
