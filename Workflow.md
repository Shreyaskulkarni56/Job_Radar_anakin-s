JobRadar — Full Workflow
STEP 1: USER UPLOADS RESUME (PDF)
        ↓
        Frontend sends PDF to FastAPI backend

STEP 2: EXTRACT RESUME DATA
        ↓
        Backend reads PDF text
        ↓
        Groq LLM extracts:
        - Name
        - Skills (React, Python, etc.)
        - Experience level (fresher / 1-2 yrs)
        - Preferred role (based on projects + skills)
        - Location preference

STEP 3: BUILD SEARCH URLS
        ↓
        Using extracted role + location, build 3 URLs:
        - naukri.com/react-developer-jobs-in-bangalore
        - internshala.com/jobs/react-developer-jobs-in-bangalore
        - wellfound.com/jobs?q=react+developer&l=bangalore

STEP 4: SCRAPE WITH ANAKIN
        ↓
        Send all 3 URLs to Anakin Batch API
        ↓
        Anakin returns clean markdown from all 3 boards
        ↓
        (runs in parallel, not one by one)

STEP 5: SCORE JOBS AGAINST YOUR RESUME
        ↓
        Send scraped jobs + your resume data to Groq
        ↓
        Groq compares each job's requirements
        against YOUR actual skills
        ↓
        Gives each job:
        - Fit Score (1-10)
        - Fit Reason ("You have 4/5 required skills")
        - Missing Skills ("Only missing: GraphQL")

STEP 6: SHOW RESULTS
        ↓
        Jobs sorted by fit score (highest first)
        ↓
        Each card shows:
        - Job title + company
        - Salary + location
        - Your fit score
        - What skills you match
        - What's missing
        - Direct apply button

Data Flow Diagram
[PDF Resume]
     ↓
[FastAPI Backend]
     ↓
[Groq] → extracts profile
     ↓
[Anakin Batch API] → scrapes 3 job boards
     ↓
[Groq] → scores each job vs your resume
     ↓
[React Frontend] → shows ranked job cards

Files We Need to Build
jobradar/
├── backend/
│   ├── main.py          → FastAPI routes
│   ├── resume.py        → PDF reading + Groq extraction
│   ├── scraper.py       → Anakin batch scraping
│   ├── scorer.py        → Job scoring vs resume
│   └── requirements.txt
└── frontend/
    └── src/
        ├── App.jsx       → Main UI
        ├── Upload.jsx    → Resume upload component
        ├── JobCard.jsx   → Individual job card
        └── App.css       → Styles