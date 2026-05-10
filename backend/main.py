from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

from resume import extract_resume_data
from scraper import scrape_jobs
from scorer import score_jobs

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/jobs/search")
async def search_jobs(resume: UploadFile = File(...)):
    if not resume.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    pdf_content = await resume.read()
    
    try:
        user_profile = extract_resume_data(pdf_content)
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Failed to parse resume: {str(e)}")

    try:
        scraped_jobs = scrape_jobs(
            user_profile.get("preferred_role"), 
            user_profile.get("location_preference"),
            user_profile.get("experience_level")
        )
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Failed to scrape jobs: {str(e)}")

    try:
        scored_jobs = score_jobs(scraped_jobs, user_profile)
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Failed to score jobs: {str(e)}")

    return {
        "profile": user_profile,
        "jobs": scored_jobs
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
