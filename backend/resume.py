import io
import os
import json
from PyPDF2 import PdfReader
from groq import Groq

def extract_resume_data(pdf_bytes: bytes) -> dict:
    reader = PdfReader(io.BytesIO(pdf_bytes))
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"

    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY environment variable is not set")

    client = Groq(api_key=api_key)

    prompt = f"""
    Extract the following details from the resume text provided below.
    Return ONLY a JSON object with the following exact keys:
    - name (string)
    - skills (list of strings)
    - experience_level (string, e.g., 'fresher', '1-2 yrs')
    - preferred_role (string, inferred from skills and projects, e.g., 'React Developer')
    - location_preference (string, default to 'Remote' or 'Bangalore' if not found, or extract if mentioned)
    
    Resume Text:
    {text}
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
    return json.loads(response_text)
