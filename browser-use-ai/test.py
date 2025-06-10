from langchain_google_genai import ChatGoogleGenerativeAI
import asyncio
import json
import os
from datetime import datetime
from browser_use import Agent
from dotenv import load_dotenv

# Read GOOGLE_API_KEY into env
load_dotenv()

# Initialize the model
llm = ChatGoogleGenerativeAI(model='gemini-2.5-flash-preview-04-17')

def extract_content_from_agent_result(result):
    """
    Extract meaningful content from the AgentHistoryList result.
    
    Args:
        result: The result from agent.run()
    
    Returns:
        str: Extracted content or string representation of the result
    """
    try:
        # Method 1: Check if result has a history attribute
        if hasattr(result, 'history') and len(result.history) > 0:
            # Look through the history from the end to find meaningful content
            for entry in reversed(result.history):
                # Try different attributes that might contain the final result
                for attr in ['result', 'message', 'content', 'output', 'response']:
                    if hasattr(entry, attr):
                        value = getattr(entry, attr)
                        if value and str(value).strip():
                            return str(value)
                
                # If no specific attribute found, convert the entry to string
                entry_str = str(entry)
                if entry_str and len(entry_str.strip()) > 10:  # Avoid empty or very short strings
                    return entry_str
        
        # Method 2: Check if result has direct content attributes
        for attr in ['result', 'content', 'output', 'response', 'final_result']:
            if hasattr(result, attr):
                value = getattr(result, attr)
                if value and str(value).strip():
                    return str(value)
        
        # Method 3: Check if result is iterable and extract from last item
        try:
            if hasattr(result, '__iter__') and not isinstance(result, str):
                items = list(result)
                if items:
                    return str(items[-1])
        except:
            pass
        
        # Method 4: Fallback to string representation
        return str(result)
        
    except Exception as e:
        print(f"Error extracting content: {e}")
        return str(result)

def write_to_json_file(data, filename=None):
    """
    Write data to a JSON file locally.
    
    Args:
        data: The data to write (should be JSON serializable)
        filename: Optional filename. If not provided, generates one with timestamp
    
    Returns:
        str: The filename that was written to
    """
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"job_postings_{timestamp}.json"
    
    # Ensure the filename has .json extension
    if not filename.endswith('.json'):
        filename += '.json'
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Data successfully written to {filename}")
        return filename
    except Exception as e:
        print(f"Error writing to JSON file: {e}")
        return None

career_pages = [
    "https://www.hashicorp.com/en/careers/open-positions",
    # "https://www.flipkartcareers.com/#!/",
    # "https://careers.swiggy.com/#/",
    # "https://www.amazon.jobs/en",
]

async def main():
    for i, page in enumerate(career_pages):
        company_name = page.split('//')[1].split('.')[0] if '//' in page else f"company_{i}"
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        # Create agent without additional_tools parameter
        agent = Agent(
            task=f"""Open {page} and find job postings for 'devops engineer', 'SRE', or 'site reliability engineer'.
                Make a list of all the job postings with details like job title, location, required experience, and job URL.
                Return the results as a structured list or JSON format that I can parse.
                The job postings should be in the format of 'job title', 'location', 'required experience', 'job URL'
                Write the results to a JSON file with the name 'jobs_{timestamp}.json'""",
            llm=llm
        )
        
        # Run the agent and get results
        result = await agent.run()
        
        # Extract the actual content from the AgentHistoryList
        try:
            # Use the improved content extraction function
            content = extract_content_from_agent_result(result)
            
            # Try to parse JSON from the content
            import re
            json_match = re.search(r'\[.*\]|\{.*\}', content, re.DOTALL)
            if json_match:
                try:
                    job_data = json.loads(json_match.group())
                    # Ensure it's wrapped in a proper structure
                    if not isinstance(job_data, dict):
                        job_data = {
                            "company": company_name,
                            "source_url": page,
                            "job_listings": job_data,
                            "timestamp": datetime.now().isoformat()
                        }
                    else:
                        # Add metadata if not present
                        job_data.setdefault("company", company_name)
                        job_data.setdefault("source_url", page)
                        job_data.setdefault("timestamp", datetime.now().isoformat())
                except json.JSONDecodeError:
                    job_data = {
                        "company": company_name,
                        "source_url": page,
                        "extracted_content": content,
                        "timestamp": datetime.now().isoformat(),
                        "note": "Content could not be parsed as JSON"
                    }
            else:
                job_data = {
                    "company": company_name,
                    "source_url": page,
                    "extracted_content": content,
                    "timestamp": datetime.now().isoformat(),
                    "note": "No JSON structure found in content"
                }
            
            # Save to JSON file with timestamp
            filename = f"jobs_{timestamp}.json"
            write_to_json_file(job_data, filename)
            
        except Exception as e:
            print(f"Error processing results for {company_name}: {e}")
            # Save raw result as fallback
            fallback_data = {
                "company": company_name,
                "source_url": page,
                "raw_result": str(result),
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            write_to_json_file(fallback_data, f"jobs_{timestamp}_raw.json")

asyncio.run(main())