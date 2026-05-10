# 🚀 JobRadar: AI-Powered Job Matching Pipeline

JobRadar is an advanced, context-aware AI job search platform. Instead of endlessly scrolling through irrelevant jobs, JobRadar reads your resume (PDF), understands your exact experience level, automatically scrapes multiple job boards, filters out sponsored/irrelevant jobs, and scores the best matches against your profile.

## 🏗️ Architecture & Technology Stack

- **Frontend**: React (Vite) with a premium Dark Glassmorphic UI.
- **Backend**: FastAPI (Python)
- **Scraping Engine**: **Anakin AI** (Batch URL Scraper & Holocron Catalog)
- **LLM Intelligence**: **Groq API** (`llama-3.1-8b-instant`) for blazing-fast data extraction and scoring.
- **PDF Parsing**: `PyPDF2`

---

## 🧠 How It Works (The API Pipeline)

JobRadar uses a hybrid architecture combining the scraping power of Anakin AI with the speed and intelligence of Groq.

### 1. The Resume Extraction (Groq)
When you upload your PDF, the backend extracts the raw text and passes it to **Groq**. Groq parses the text into a strict JSON schema, extracting your name, skills, preferred role, and most importantly, your **experience level** (e.g., "Fresher").

### 2. Context-Aware URL Generation
Based on your extracted experience, JobRadar dynamically generates search URLs. If you are a fresher, it automatically appends filters like `?experience=0` to Naukri or `&f_E=2` to LinkedIn to target entry-level positions.

### 3. The Scraping Engine (Anakin AI APIs)
This is the core of the data pipeline. We use Anakin AI for two main purposes:
- **Anakin Batch URL Scraper API**: We pass the generated URLs (Naukri, Internshala, Wellfound, LinkedIn) into Anakin's Batch Scraper. Anakin automatically bypasses bot protections, scrapes the websites, and returns the raw Markdown text of the pages.
- **Anakin Holocron Catalog (RemoteOK)**: We also query Anakin's pre-built Holocron API for RemoteOK to fetch structured remote jobs instantly without needing to scrape.

### 4. Smart Filtering & Schema Extraction (Groq)
Anakin's scraper fetches everything on the screen, including promoted/sponsored jobs that might require 5-8 years of experience. We take the raw Markdown from Anakin and pass it into **Groq** with a strict prompt: *"The user is a Fresher. Filter out any jobs requiring more experience."* Groq instantly deletes irrelevant jobs and returns a clean, strict JSON array containing the Job Title, Company, Salary, Requirements, and the exact `apply_url`.

### 5. AI Scoring (Groq)
Finally, Groq compares your resume profile against the extracted job requirements, generating a "Fit Score", explaining why you are a good match, and listing any missing skills you might need to learn.

---

## 🛠️ Environment Setup

### Prerequisites
- Node.js (v16+)
- Python (3.10+)
- [Anakin AI API Key](https://anakin.ai/)
- [Groq API Key](https://console.groq.com/)

### 1. Clone the Repository
```bash
git clone https://github.com/Shreyaskulkarni56/Job_Radar_anakin-s.git
cd Job_Radar_anakin-s
```

### 2. Backend Setup
1. Open a terminal and navigate to the `backend` directory:
   ```bash
   cd backend
   ```
2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   # On Windows
   .\venv\Scripts\activate
   # On Mac/Linux
   source venv/bin/activate
   ```
3. Install the Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file in the `backend/` directory:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   ANAKIN_API_KEY=your_anakin_api_key_here
   ```
5. Start the FastAPI server:
   ```bash
   python main.py
   # Or run: uvicorn main:app --reload --port 8000
   ```

### 3. Frontend Setup
1. Open a new terminal and navigate to the `frontend` directory:
   ```bash
   cd frontend
   ```
2. Install the Node dependencies:
   ```bash
   npm install
   ```
3. Start the Vite development server:
   ```bash
   npm run dev
   ```
4. Open your browser and navigate to the URL provided (usually `http://localhost:5173`).

---

## 🎨 UI/UX Features
- **Dynamic Breathing Background**: Pitch black theme with subtle animated radial gradients.
- **Glassmorphism**: Frosted glass cards with glowing borders for Job Insights.
- **Staggered Animations**: Job cards cascade into view smoothly after the AI finishes scoring.
- **Interactive Shines**: Buttons feature dynamic metallic shine effects on hover.
