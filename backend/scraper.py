import json
import os
import requests
from groq import Groq

def scrape_jobs(role: str, location: str, experience_level: str = None) -> list:
    """
    Uses Anakin Batch Universal Scraper + Groq for strict JSON extraction 
    across multiple local job boards!
    """
    role_slug = role.lower().replace(" ", "-") if role else "developer"
    loc_slug = location.lower().replace(" ", "-") if location else "bangalore"

    is_fresher = experience_level and any(word in experience_level.lower() for word in ['fresh', '0', 'entry', 'intern', 'beginner', 'none', '1', 'one'])

    naukri_url = f"https://www.naukri.com/{role_slug}-jobs-in-{loc_slug}"
    if is_fresher: naukri_url += "?experience=0"

    internshala_url = f"https://internshala.com/jobs/fresher-{role_slug}-jobs-in-{loc_slug}" if is_fresher else f"https://internshala.com/jobs/{role_slug}-jobs-in-{loc_slug}"

    linkedin_url = f"https://www.linkedin.com/jobs/search?keywords={role.replace(' ', '%20')}&location={location.replace(' ', '%20')}"
    if is_fresher: linkedin_url += "&f_E=2" # 2 represents Entry level

    urls = [
        naukri_url,
        internshala_url,
        f"https://wellfound.com/jobs?q={role_slug.replace('-', '+')}&l={loc_slug}",
        linkedin_url
    ]

    anakin_api_key = os.environ.get("ANAKIN_API_KEY")

    if anakin_api_key:
        try:
            headers = {
                "X-API-Key": anakin_api_key,
                "Content-Type": "application/json"
            }
            payload = {
                "urls": urls,
                "useBrowser": False,
                "generateJson": False
            }
            
            # Submit batch job
            submit_url = "https://api.anakin.io/v1/url-scraper/batch"
            response = requests.post(submit_url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            job_id = response.json().get("jobId")
            
            if job_id:
                import time
                poll_url = f"https://api.anakin.io/v1/url-scraper/{job_id}"
                
                # Poll until completed
                batch_results = []
                for attempt in range(25): # Wait up to 125 seconds
                    time.sleep(5)
                    res = requests.get(poll_url, headers=headers, timeout=30)
                    res.raise_for_status()
                    data = res.json()
                    
                    if data.get("status") == "completed":
                        batch_results = data.get("results", [])
                        if "markdown" in data:
                            batch_results = [data]
                        break
                    elif data.get("status") in ["failed", "error"]:
                        print("Anakin batch job failed:", data.get("error"))
                        break
                
                # Combine markdown from all pages
                combined_markdown = ""
                for i, res in enumerate(batch_results):
                    # some pages return markdown, some cleanedHtml
                    md = res.get("markdown", "")
                    if not md: md = res.get("cleanedHtml", "")
                    
                    print(f"--- Anakin Extracted Text (Page {i+1}) ---")
                    print(md[:500] + "\n...[truncated]...\n")
                    
                    # Take only a smaller chunk per page to avoid token limits
                    combined_markdown += md[:6000] + "\n\n"
                    
                if combined_markdown.strip():
                    groq_api_key = os.environ.get("GROQ_API_KEY")
                    if groq_api_key:
                        client = Groq(api_key=groq_api_key)
                        
                        prompt = f"""
                        You are an expert job data extractor.
                        Extract a list of jobs from the following scraped website markdown.
                        Format your response as a raw JSON list of objects, without markdown wrapping.
                        Required keys for each object:
                        "title", "company", "location", "salary", "requirements", "apply_url"
                        
                        CRITICAL INSTRUCTION FOR EXPERIENCE FILTERING:
                        The user has the following experience level: "{experience_level or 'Fresher/0 years'}".
                        You MUST completely IGNORE and SKIP any jobs in the markdown that require more experience (e.g., 4-5 years, Senior, Lead).
                        ONLY extract jobs that match the user's experience level or do not explicitly state a high experience requirement.
                        
                        CRITICAL INSTRUCTION FOR "apply_url":
                        You MUST extract the exact URL from the markdown link syntax `[Job Title](URL)`. 
                        DO NOT make up URLs. DO NOT just return "https://naukri.com". Find the specific job URL!
                        If you cannot find specific fields like salary, use "Not disclosed".
                        Ensure the JSON is perfectly valid.
                        
                        Markdown:
                        {combined_markdown[:12000]}
                        """
                        
                        chat_completion = client.chat.completions.create(
                            messages=[
                                {"role": "system", "content": "Output only valid JSON."},
                                {"role": "user", "content": prompt}
                            ],
                            model="llama-3.1-8b-instant",
                            temperature=0.2,
                        )
                        
                        response_text = chat_completion.choices[0].message.content.strip()
                        
                        if "```json" in response_text:
                            response_text = response_text.split("```json")[1].split("```")[0].strip()
                        elif "```" in response_text:
                            response_text = response_text.split("```")[1].strip()
                            
                        scraped_jobs = json.loads(response_text)
                        
                        if scraped_jobs and isinstance(scraped_jobs, list):
                            normalized = []
                            for i, j in enumerate(scraped_jobs):
                                normalized.append({
                                    "id": str(i+1),
                                    "title": j.get("title", f"{role or 'Developer'}"),
                                    "company": j.get("company", "Company Name"),
                                    "location": j.get("location", location or "Remote"),
                                    "salary": j.get("salary", "Not disclosed"),
                                    "requirements": j.get("requirements", "Various skills required"),
                                    "apply_url": j.get("apply_url", "https://google.com")
                                })
                            return normalized

        except Exception as e:
            print(f"Anakin IO API or Groq extraction failed: {str(e)}.")
            import traceback
            traceback.print_exc()
            print("Falling back to mock data.")

    return [
        {
            "id": "1",
            "title": f"Senior {role or 'Developer'}",
            "company": "Tech Innovators Inc.",
            "location": location or "Remote",
            "salary": "$120,000 - $150,000",
            "requirements": "React, Node.js, AWS, 5+ years experience",
            "apply_url": "https://google.com"
        }
    ]
