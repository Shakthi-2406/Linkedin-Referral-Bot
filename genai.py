import requests
from urllib.parse import urlencode
import json

def get_response(resume_content :str, job_id :str, company :str, role :str):
  url = 'https://3c4e-34-125-254-40.ngrok-free.app/?'

  params = {'resume_content' : resume_content,
            'job_id' : str(job_id),
            'company' : company,
            'role' : role}

  params = urlencode(params)
  url += params
  print(url)
  response = requests.get(url)
  response = json.loads(response.text)
  print(response['message'])
  return response['message']

get_response(resume_content = 'resume_content', job_id = '158780', company = 'Oracle', role = 'Machine learning Engineer')
