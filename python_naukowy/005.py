import requests
from bs4 import BeautifulSoup
import json

res = requests.get('https://nofluffjobs.com/pl/warszawa/Python?page=1&criteria=seniority%3Djunior')
soup = BeautifulSoup(res.text, 'html.parser')

posting_list = soup.find('nfj-postings-list')
posts = posting_list.find_all('nfj-posting-item-title')
titles = [post.find('h3') for post in posts]
companies = [post.find('span') for post in posts]
#salaries = [post.select('h3 + div') for post in posts]

jobs = []
for title, company in zip(titles, companies):
    jobs.append({'title': title.text, 'company': company.text})

with open('python_naukowy/jobs.json', 'w') as f:
    json.dump(jobs, f, indent=4)