from datetime import datetime
from TheHunt import create_app
from TheHunt.db import db
from TheHunt.models import SearchTerm, Location, Hit, Company
from TheHunt.appadmin import api
from sqlalchemy import exc as sa_exc
from time import sleep
import utilities
import bs4
from bs4 import BeautifulSoup
import requests
import warnings


def remove_new_line(s):
    return s.replace('\n', '')


def awaitdb(func):
    """Await database connection"""
    def decor(*args, **kwargs):
        while True:
            try:
                return func(*args, **kwargs)
                break
            except sa_exc.OperationalError:
                print(f"Database is locked... Awaiting: {func.__name__}.")
                db.session.rollback()
                sleep(5)
            except sa_exc.IntegrityError:
                print("IntegrityError encountered")
                break
            except sa_exc.InvalidRequestError:
                print("Rolling back session")
                return awaitdb(func)(*args, **kwargs)
    return decor


@awaitdb
def load_company(session, datadict):

    company = Company.query.filter(Company.name==datadict['company']).first

    company = awaitdb(company)()

    if company is None:
        company = Company(name=datadict['company'])
        db.session.add(company)
    return company, session


def generate_hit(jobid, datadict, search_vector, company):
    hit = Hit(
            id=jobid,
            term=search_vector.termid,
            loc=search_vector.locid,
            title=datadict['title'],
            company=datadict['company'],
            salary=datadict['salary'],
            min_salary=datadict['min_salary'],
            max_salary=datadict['max_salary'],
            summary=datadict['summary'],
            url=datadict['url']
        )
    return hit


@awaitdb
def exists(x):
    return Hit.query.filter(Hit.id==x).first()


def run_page(vec, url, goto=0):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")

    # Get job descriptions
    jobs, num_jobs_found = utilities.get_job_desc(
        vec, soup, goto=goto)

    # Return if no jobs found
    if num_jobs_found == 0:
        return 0

    # Load jobs to database
    counter = 0
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=sa_exc.SAWarning)
        hits = []
        for j in jobs:
            # company, session = load_company(session, j)
            jobid = f"{j['title']}.{j['company']}"
            # jobid = f"{j['title']}.{j['company']}.{j['location']}"
            if exists(jobid) is None:
                hits.append(generate_hit(jobid, j, vec, j['company']))
            counter += 1
        db.session.add_all(hits)
        db.session.commit()

    return counter


def scrape_copy(vector, num_jobs_wanted):
    update_count = 0
    goto = num_jobs_wanted - update_count
    update_count += run_page(vector, vector.url, goto)
    for _ in range(0, num_jobs_wanted, 10):
        url = vector.url + f"&start={_}"
        goto = num_jobs_wanted - update_count
        update_count += run_page(vector, url, goto)
        if update_count >= num_jobs_wanted:
            break
    print(f"{vector.term} - {vector.loc}: {update_count} hits.")
