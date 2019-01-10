from datetime import datetime, timedelta
from tqdm import tqdm
from TheHunt import create_app
from TheHunt.db import db
from TheHunt.models import SearchTerm, Location, Hit, Company
from TheHunt.appadmin import api
from sqlalchemy import exc as sa_exc, func, asc
import bs4
from bs4 import BeautifulSoup
import utilities
import time
import click
import requests
import sys
import warnings
import time
import sys


def timeit(func):
    start = datetime.now()
    def decor(*args, **kwargs):
        res = func(*args, **kwargs)
        print(f"{func.__name__}: {(datetime.now() - start).total_seconds()}")
        return res
    return decor


def remove_new_line(s):
    return s.replace('\n', '')


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


def exists(x):
    return Hit.query.filter(Hit.id==x).first()


def run_page(session, vec, url, goto=0):
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
            jobid = f"{j['title']}.{j['company']}.{j['location']}"
            if exists(jobid) is None:
                hits.append(generate_hit(jobid, j, vec, j['company']))
            counter += 1
        db.session.add_all(hits)
        db.session.commit()

    return counter


class SearchVector:
    def __init__(self, term=None, loc=None, termid=None, locid=None):
        self.term = term
        self.loc = loc
        self.termid = termid
        self.locid = locid
        self.url = f"https://www.indeed.com/jobs?q="\
            f"{self.term,}&l={self.loc}"

    def __repr__(self):
        return f"{self.term}.{self.loc}"


def searchterm_query():
    return SearchTerm\
            .query\
            .with_entities(SearchTerm.id, SearchTerm.text)\
            .outerjoin(Hit, SearchTerm.id==Hit.term)\
            .group_by(SearchTerm.id)\
            .order_by(asc(func.count(Hit.term)))


def location_query():
    return Location\
            .query\
            .with_entities(Location.id, Location.full)\
            .outerjoin(Hit, Location.id==Hit.loc)\
            .group_by(Location.id)\
            .order_by(asc(func.count(Hit.loc)))


def get_search_vectors():
    return [SearchVector(t.text, l.full, t.id, l.id)
        for t in searchterm_query().all()
        for l in location_query().all()]


def scrape_copy(vector, num_jobs_wanted, session):
    # Run initial page
    update_count = 0
    goto = num_jobs_wanted - update_count
    update_count += run_page(session, vector, vector.url, goto)
    for _ in range(0, num_jobs_wanted, 10):
        url = vector.url + f"&start={_}"
        goto = num_jobs_wanted - update_count
        update_count += run_page(session, vector, url, goto)
        if update_count >= num_jobs_wanted:
            break
    print(f"{vector.term} - {vector.loc}: {update_count} hits.")


@timeit
def clear_hit_data():
    print("Deleting hits")
    Hit.query.delete()
    Company.query.delete()
    db.session.commit()


def run(num_jobs, vectors):
    procs_running = 0
    # MAX_PROCS = 4
    sesh = db.session
    for vec in vectors:
        scrape_copy(vec, num_jobs, sesh)


@click.command()
@click.option('--num_jobs', default=10, help="Number of jobs desired per location")
@click.option('--clear_hits', default=False, is_flag=True, help="Clear existing job search hits")
@click.option('--runs', default=100, help="Number of times to run")
@click.option('--waithours', type=float, default=1, help="Number of hours before refreshing")
def main(num_jobs, clear_hits, runs, waithours):
    print(f"Running with options: {num_jobs}, {clear_hits}, {runs}, {waithours}")
    start = datetime.now()
    if clear_hits:
        clear_hit_data()
    for r in range(0, runs):
        if r == 0:
            print(f"Started: {start}")
            vectors = get_search_vectors()
            run(num_jobs, vectors)
            api.update_word_corpus()
            continue
        while True:
            # Check to see if time has passed since last start
            waittime = start + timedelta(hours=waithours)
            print(f"Next Run at: {waittime}")
            if datetime.now() > waittime:
                start = datetime.now()  # Reset last run timestamp
                print(f"Started: {start}")
                vectors = get_search_vectors()
                run(num_jobs, vectors)
                api.update_word_corpus()
                break
            else:
                print(f"Sleeping for {waithours} hour(s)...")
                countdowntotal = (waittime - start).total_seconds()
                while countdowntotal > 0:
                    writeout = countdowntotal//60\
                        if countdowntotal > 60\
                        else int(countdowntotal)
                    sys.stdout.write(f"{writeout} ")
                    sys.stdout.flush()
                    time.sleep(1)
                    sys.stdout.write("\b" * (len(str(writeout)) + 1))
                    countdowntotal -= 1


if __name__ == '__main__':
    app = create_app()
    app.config.from_object('TheHunt.config.ETL')
    with app.app_context():
        main()
