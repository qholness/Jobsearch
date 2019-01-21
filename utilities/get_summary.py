import requests
import bs4
from bs4 import BeautifulSoup


def get_summary(link):
    soup = requests.get(link)
    soup = BeautifulSoup(soup.text, "html.parser")
    summary = soup.find_all(name="div", attrs={'class': 'jobsearch-JobComponent-description'})
    if len(summary):
        return summary[0]\
            .text\
            .strip()\
            .replace('`', '')\
            .replace('\\', '')
    return None
