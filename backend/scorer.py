import json
import os
from groq import Groq

def score_jobs(jobs: list, user_profile: dict) -> list:
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY environment variable is not set")
        
    client = Groq(api_key=api_key)
    
    prompt = f"""
    You are an expert technical recruiter. Score the fit of the following jobs based on the candidate's profile.
    
    Candidate Profile:
    {json.dumps(user_profile, indent=2)}
    
    Jobs to score:
    {json.dumps(jobs, indent=2)}
    
    For each job, compare the job's requirements against the candidate's actual skills and experience level.
    Return ONLY a JSON object with a single key "scores" which contains an array of objects.
    Each object in the array MUST have this exact structure:
    {{
      "job_id": "the job id",
      "fit_score": 8, // integer from 1-10
      "fit_reason": "Brief explanation of why this is a good/bad fit",
      "missing_skills": "Comma separated list of missing skills, or 'None'"
    }}
    """

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="llama-3.1-8b-instant",
        temperature=0.2,
        response_format={"type": "json_object"}
    )
    
    response_text = chat_completion.choices[0].message.content
    scores_data = json.loads(response_text)
    scores_dict = {str(item["job_id"]): item for item in scores_data.get("scores", [])}
    
    # Merge scores with original jobs
    scored_jobs = []
    for job in jobs:
        score_info = scores_dict.get(str(job["id"]), {})
        merged_job = {**job, **score_info}
        scored_jobs.append(merged_job)
        
    # Sort by fit_score descending
    scored_jobs.sort(key=lambda x: x.get("fit_score", 0), reverse=True)
        
    return scored_jobs
