import json, os
from groq import Groq
from dotenv import load_dotenv

load_dotenv('.env')

data = json.load(open('temp2.txt', encoding='utf-8'))
combined_markdown = ''
for i, res in enumerate(data.get('results', [])):
    md = res.get('markdown', '')
    combined_markdown += md[:6000] + '\n\n'

client = Groq(api_key=os.environ.get('GROQ_API_KEY'))
prompt = f'''
You are an expert job data extractor.
Extract a list of jobs from the following scraped website markdown.
Format your response as a raw JSON list of objects, without markdown wrapping.
Required keys for each object:
"title", "company", "location", "salary", "requirements", "apply_url"

CRITICAL INSTRUCTION FOR "apply_url":
You MUST extract the exact URL from the markdown link syntax [Job Title](URL). 
DO NOT make up URLs. DO NOT just return "https://naukri.com". Find the specific job URL!
If you cannot find specific fields like salary, use "Not disclosed".
Ensure the JSON is perfectly valid.

Markdown:
{combined_markdown[:12000]}
'''
chat_completion = client.chat.completions.create(
    messages=[
        {'role': 'system', 'content': 'Output only valid JSON.'},
        {'role': 'user', 'content': prompt}
    ],
    model='llama-3.1-8b-instant',
    temperature=0.2,
)
print(chat_completion.choices[0].message.content)
