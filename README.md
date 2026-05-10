# JobRadar

JobRadar is an AI-powered job matching platform that reads your resume (PDF) and scores job listings against your profile using Groq LLM.

## Architecture

- **Backend**: FastAPI
- **Frontend**: React (Vite)
- **AI**: Groq API (llama3-8b-8192)
- **PDF Extraction**: PyPDF2

## Setup Instructions

### 1. Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Create a `.env` file in `backend/` and add your Groq API key:
   ```
   GROQ_API_KEY=your_api_key_here
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the backend server:
   ```bash
   python main.py
   ```

### 2. Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   npm install axios lucide-react
   ```
3. Run the frontend development server:
   ```bash
   npm run dev
   ```

## Workflow
1. Upload a PDF Resume via the Frontend UI.
2. The FastAPI backend extracts the text using PyPDF2.
3. Groq LLM parses the resume to extract Name, Skills, Experience, Preferred Role, and Location.
4. The system mocks Anakin Batch API to fetch jobs from Naukri, Internshala, and Wellfound.
5. Groq LLM scores each job's requirements against the candidate's extracted profile.
6. The UI displays the user profile and ranked job cards showing Fit Score, Fit Reason, and Missing Skills.
