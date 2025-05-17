import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json
import re
import time
import sys
import os
from dotenv import load_dotenv
import pandas as pd
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

OLLAMA_URL = "http://desktop-home:11434/api/generate"  # Your cloud Ollama instance
OLLAMA_MODEL = "mistral"  # Using Mistral for good performance

EXCEL_FILENAME = "job_applications.xlsx"

def fetch_website_html(url):
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)  # wait for loading
    html = driver.page_source
    driver.quit()
    return html

def extract_text_from_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    return soup.get_text()

def query_ollama(prompt):
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False
    }
    
    try:
        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        return response.json().get("response", "")
    except requests.exceptions.RequestException as e:
        print(f"Error querying Ollama: {e}")
        if hasattr(e.response, 'text'):
            print(f"Response content: {e.response.text}")
        raise

def load_existing_jobs():
    try:
        return pd.read_excel(EXCEL_FILENAME)
    except FileNotFoundError:
        return pd.DataFrame(columns=[
            'title', 'location', 'skills', 'description', 
            'experience', 'match', 'extraction_date', 'applied'
        ])

def save_jobs_to_excel(jobs_df):
    jobs_df.to_excel(EXCEL_FILENAME, index=False)

def process_job_batch(jobs, existing_df):
    # Convert new jobs to DataFrame
    new_df = pd.DataFrame(jobs)
    new_df['extraction_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    new_df['applied'] = False  # Default applied status
    
    # Combine with existing data
    combined_df = pd.concat([existing_df, new_df], ignore_index=True)
    
    # Remove duplicates based on title and location, keeping the most recent entry
    combined_df = combined_df.drop_duplicates(subset=['title', 'location'], keep='last')
    
    # Save immediately
    save_jobs_to_excel(combined_df)
    return combined_df

def extract_jobs_from_text(text):
    # Split text into chunks of approximately 8000 characters (leaving room for prompt)
    chunk_size = 12000
    chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
    
    # Load existing jobs at the start
    existing_df = load_existing_jobs()
    
    for i, chunk in enumerate(chunks):
        print(f"Processing chunk {i+1}/{len(chunks)}")
        prompt = f"""
You are a job listing extraction bot. From the text below, extract all job postings.

Return only a JSON array like:
[
  {{
    "title": "...",
    "location": "...",
    "skills": ["...", "..."],
    "description": "...",
    "experience": "...",
    "match": true
  }}
]

Only return the JSON array. No explanation.

Text:
{chunk}
"""
        print(f"Processing chunk of size: {len(prompt)}")
        response = query_ollama(prompt)

        # Try to extract JSON array using regex
        match = re.search(r'\[\s*{.*?}\s*\]', response, re.DOTALL)
        if match:
            try:
                jobs = json.loads(match.group())
                # Process and save this batch immediately
                existing_df = process_job_batch(jobs, existing_df)
                print(f"Saved batch {i+1} to Excel")
            except json.JSONDecodeError:
                print(f"JSON decode error in chunk {i+1}")
        else:
            print(f"No JSON array found in chunk {i+1}")

    return existing_df

def main():
    # url = "https://remotive.com/remote-jobs/feed/devops"
    url = "https://jobs.apple.com/en-in/search?location=bengaluru-BGS"
    html = fetch_website_html(url)
    
    # Write HTML to file for debugging
    with open("debug_output.html", "w", encoding="utf-8") as f:
        f.write(html)

    text = extract_text_from_html(html)
    final_df = extract_jobs_from_text(text)
    
    # Print summary
    print(f"\nTotal jobs in database: {len(final_df)}")
    print(f"Jobs not yet applied to: {len(final_df[final_df['applied'] == False])}")

if __name__ == "__main__":
    main()
