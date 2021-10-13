import pip._vendor.requests 
from bs4 import BeautifulSoup
import pandas as pd 
import os
from dotenv import load_dotenv
from pathlib import Path

dotenv_path = Path('path/to/.env')
load_dotenv(dotenv_path=dotenv_path)

def extract(page):
    headers = os.getenv('USER_AGENT')
    url = (f'https://www.indeed.com/jobs?q=software%20engineer&l=New%20York%2C%20NY&start={page}')
    r = pip._vendor.requests.get(url, headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup
    # return r.status_code

def transform(soup):
    divs = soup.find_all('div', class_ = 'job_seen_beacon')
    # loop through each div and get out respective information:
    for item in divs:
        title = item.find('span').text.strip()
        company = item.find('span', class_ = 'companyName').text.strip()
        try:
            salary = item.find('span', class_ ='salary-snippet').text.strip()
        except:
            salary = ''
        summary = item.find('div', class_ = 'job-snippet').text.strip().replace('\n', '')
    
        # store information into dictionary
        job = {
            'title': title,
            'company': company,
            'salary': salary,
            'summary': summary
        }

        # append dictionary information 
        joblist.append(job)

    return

joblist = []
# for loop to iterate through the pages: (0-40 meaning 3 pages since its going by incremements of 10)
for i in range(0,40,10):
    print(f'Getting page: {i}')
    c = extract(i)
    transform(c)

# creates a panda dataframe
df = pd.DataFrame(joblist)
print(df.head())
# creating csv file
df.to_csv('jobs.csv')
