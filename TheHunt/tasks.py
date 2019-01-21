from . import celery
from celery.schedules import crontab
from celery.signals import worker_ready
from datetime import timedelta
from TheHunt.config import CeleryConfig
from TheHunt.models import SearchTerm, Location
from TheHunt.appadmin import api
from TheHunt.scraper.scraper import scrape_copy
from TheHunt import create_app
from TheHunt.scraper.get_search_vectors import get_search_vectors, SearchVector
import json


with create_app().app_context():
    search_vectors = get_search_vectors()


@worker_ready.connect
def at_start(sender, **k):
    with sender.app.connection() as conn:
        sender.app.send_task(
            'TheHunt.tasks.scrape',
            connection=conn)


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Call prune_hits every seven days
    sender.add_periodic_task(
        timedelta(days=CeleryConfig.PRUNE_WAIT_DAYS),
        api_prune_hits.s(),
        name='prune-hits-every-seven-days')

    # Update wordcorpus daily
    sender.add_periodic_task(
        timedelta(hours=CeleryConfig.UPDATE_WORD_CORP_WAIT_HOURS),
        api_word_corp.s(),
        name='update-word-corpus')

    # Call tacos every 10 seconds
    # sender.add_periodic_task(10, test.s(), name='ten-second-tacos')

    # Run scraper
    # sender.add_periodic_task(timedelta(hours=6), scrape.s(), name='scrape-indeed')
    for vec in search_vectors:
        sender.add_periodic_task(
            timedelta(hours=CeleryConfig.HIT_GET_WAIT_HOURS),
            scrape.s(),
            name=f'get-hits-for-{vec.term}-{vec.loc}')

@celery.task
def test():
    print("Test")
    return "Running"


@celery.task
def api_prune_hits(days=7):
    with create_app().app_context():
        api.prune_hits(days)


@celery.task
def api_word_corp():
    with create_app().app_context():
        api.update_word_corpus()


@celery.task
def scrape():
    # print("Scraping")
    for vec in search_vectors:
        print(vec)
        x = SearchTerm.query\
            .filter(SearchTerm.id == vec.termid)\
            .first()
        y = Location\
            .query\
            .filter(Location.id == vec.locid)\
            .first()
        num_jobs =  x.num_jobs * y.num_jobs
        scrape_copy(vec, num_jobs)
