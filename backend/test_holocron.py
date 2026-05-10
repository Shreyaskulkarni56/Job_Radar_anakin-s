import requests, os, time, json
from dotenv import load_dotenv
load_dotenv('.env')
key = os.environ.get('ANAKIN_API_KEY')
headers = {'X-API-Key': key, 'Content-Type': 'application/json'}
payload = {'action_id': 'ro_jobs', 'params': {'tag': 'developer', 'limit': 15}}
res = requests.post('https://api.anakin.io/v1/holocron/task', headers=headers, json=payload)
job_id = res.json().get('job_id')
print('Job ID:', job_id)
for _ in range(10):
    time.sleep(3)
    poll = requests.get(f'https://api.anakin.io/v1/holocron/jobs/{job_id}', headers=headers)
    status = poll.json().get('status')
    if status == 'completed':
        data = poll.json().get('data', {})
        print('Total:', data.get('count'))
        for j in data.get('data', [])[:2]:
            print(f"- {j.get('position')} at {j.get('company')} -> {j.get('apply_url')}")
        break
    elif status == 'failed':
        print('Failed', poll.json())
        break
