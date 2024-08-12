import os
from bs4 import BeautifulSoup
import requests
import time

url = 'https://www.timesjobs.com/candidate/job-search.html?searchType=Home_Search&from=submit&asKey=OFF&txtKeywords=&cboPresFuncArea=35'

def fetch_jobs():
    try:
        html_text = requests.get(url).text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the webpage: {e}")
        return None
    return BeautifulSoup(html_text, 'lxml')

def find_jobs(unfamiliar_skill):
    soup = fetch_jobs()
    if not soup:
        return

    jobs = soup.find_all('li', class_='clearfix job-bx wht-shd-bx')
    
    if not os.path.exists('posts'):
        os.makedirs('posts')

    for index, job in enumerate(jobs):
        published_date = job.find('span', class_='sim-posted').text.replace('\n', '')

        if 'today' in published_date or '1 day ago' in published_date:
            company_name = job.find('h3', class_='joblist-comp-name').text.replace(' ', '').replace('\n', '')

            skills = job.find('span', class_='srp-skills').text.replace(' ', '').replace('\n', '')

            more_info = job.find("h2").a['href']

            if unfamiliar_skill not in skills:
                with open(f'posts/{index}.txt', 'w') as f:
                    f.write(f"Company name: {company_name.strip()}\n")
                    f.write(f"Skills: {skills.strip()}\n")
                    f.write(f"Published Date: {published_date}\n")
                    f.write(f"More Info: {more_info}\n")
                print(f'File saved: {index}')

if __name__ == '__main__':
    print("Put some skill that you are not familiar with")
    unfamiliar_skill = input(">")
    print(f'Filtering out {unfamiliar_skill}')

    while True:
        find_jobs(unfamiliar_skill)
        time_wait = 10
        print(f'Waiting {time_wait} minutes...')
        time.sleep(time_wait * 60)
