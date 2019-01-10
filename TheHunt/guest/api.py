from TheHunt.models import SearchTerm, Location, Hit,\
    WordCorpusCount, UniqueWords, Company
from flask import session
from sqlalchemy.orm import joinedload
from sqlalchemy import func, desc


def get_search_terms():
    return SearchTerm\
        .query\
        .with_entities(SearchTerm.text)\
        .order_by(SearchTerm.text)


def get_locations():
    return Location\
        .query\
        .with_entities(
            Location.city, Location.state, Location.full)\
        .order_by(Location.city)


def get_hits():
    search_term = SearchTerm\
        .query\
        .filter(
            SearchTerm.text==session['search_args']['search_term'])\
        .first()

    search_location = Location\
        .query\
        .filter(
            Location.full==session['search_args']['search_location'])\
        .first()

    search_summary = session['search_args']['search_summary']
    search_min_salary = session['search_args']['search_min_salary']
    search_company = session['search_args']['search_company']

    search_summary = None if search_summary == '' else search_summary
    search_min_salary = None if search_min_salary == '' else search_min_salary
    search_company = None if search_company == '' else search_company

    hits = Hit.query

    if search_term is not None:
        hits = hits.filter(Hit.term==search_term.id)

    if search_location is not None:
        hits = hits.filter(Hit.loc==search_location.id)

    if search_summary is not None:
        search_summary = f'%{search_summary.lower()}%'
        hits = hits.filter(
            func.lower(Hit.summary).ilike(search_summary))

    if search_min_salary is not None:
        search_min_salary = float(search_min_salary)
        hits = hits.filter(
            Hit.min_salary >= search_min_salary)

    if search_company is not None:
        search_company = f'%{search_company.lower()}%'
        hits = hits\
            .filter(func.lower(Company.name).ilike(search_company))

    hits = hits\
        .join(Location, Hit.loc==Location.id)\
        .join(SearchTerm, Hit.term==SearchTerm.id)\
        .add_columns(
            Hit.title,
            Hit.updated_date.label('updated'),
            Hit.summary,
            Hit.company,
            Location.city,
            Location.state,
            Hit.min_salary,
            Hit.max_salary,
            Hit.url,
            SearchTerm.text.label("search_term")
        )
    return hits


def get_results_by_search_term():
    return Hit\
        .query\
        .with_entities(func.count(Hit.id).label('total'))\
        .join(SearchTerm, Hit.term == SearchTerm.id)\
        .add_columns(SearchTerm.text.label('search_term'))\
        .group_by(SearchTerm.id, 'search_term')\
        .order_by(desc('total'))\


def get_top_search_combo():
    return Hit\
        .query\
        .with_entities(func.count(Hit.term).label('total'))\
        .join(SearchTerm, Hit.term == SearchTerm.id)\
        .join(Location, Hit.loc == Location.id)\
        .add_column(Location.full.label('location'))\
        .add_column(SearchTerm.text.label('searchterm'))\
        .group_by(
            'location',
            'searchterm')\
        .order_by(desc('total'))


def get_top_salaries_by_search_term(limit=50):
    return Hit\
        .query\
        .filter(Hit.min_salary != None)\
        .with_entities(
            (func.sum(Hit.min_salary)/func.count(Hit.min_salary))
            .label('average_min_salary'))\
        .join(SearchTerm, Hit.term==SearchTerm.id)\
        .order_by(desc('average_min_salary'))\
        .add_column(SearchTerm.text)\
        .group_by(SearchTerm.text, Hit.term)\
        .limit(limit)


def get_top_words(how_many=10):
    return WordCorpusCount\
        .query\
        .with_entities(WordCorpusCount.total)\
        .join(UniqueWords, WordCorpusCount.word==UniqueWords.id)\
        .order_by(WordCorpusCount.total.desc())\
        .add_column(UniqueWords.word)\
        .limit(how_many)


def get_top_companies_hiring(how_many=100):
    return Hit\
        .query\
        .with_entities(
            Hit.company.label('name'),
            func.count(Hit.company).label('total'))\
        .group_by('name')\
        .order_by(desc('total'))


def get_top_locations(how_many=10):
    return Hit\
        .query\
        .with_entities(func.count(Hit.loc).label('total'))\
        .join(Location, Hit.loc == Location.id)\
        .order_by(desc('total'))\
        .group_by(Location.id)\
        .add_column(Location.city)\
        .add_column(Location.state)
