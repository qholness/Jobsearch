from TheHunt.models import Hit, SearchTerm, Location, WordCopus, WordCorpusCount, UniqueWords
from sqlalchemy import func, or_, desc
from flask_restful import Resource
from flask import session, jsonify


def marshal_with(data, cellify_func):
    if data.count() > 0:
        return "".join(list(map(cellify_func, data.all())))
    return"<p>No data.</p>"


class JobCount(Resource):
    def get(self):
        return jsonify(dict(jobs=Hit.query.with_entities(Hit.id).count()))


class HitSearch(Resource):
    def __init__(self):
        self.args = session.get('search_args')

    def __filter_by_search_term__(self):
        return SearchTerm\
        .query\
        .filter(
            SearchTerm.text==self.args['search_term'])\
        .first()

    def __filter_by_location__(self):
        return Location\
        .query\
        .filter(Location.full==self.args['search_location'])\
        .first()

    def get_hits(self):
        flipit = lambda x: None if x == '' else x
        search_term = self.__filter_by_search_term__()
        search_location = self.__filter_by_location__()
        ancillary = (self.args['search_summary'], self.args['search_min_salary'], self.args['search_company'])
        search_summary, search_min_salary, search_company = list(map(flipit, ancillary))
        hits = Hit.query

        if search_term is not None:
            hits = hits.filter(Hit.term==search_term.id)

        if search_location is not None:
            hits = hits.filter(Hit.loc==search_location.id)

        if search_summary is not None:
            search_summary = f'%{search_summary.lower()}%'
            hits = hits.filter(
                func.lower(Hit.summary)
                    .ilike(search_summary))

        if search_min_salary is not None:
            search_min_salary = float(search_min_salary)
            hits = hits.filter(
                Hit.min_salary >= search_min_salary)

        if search_company is not None:
            search_company = f'%{search_company.lower()}%'
            hits = hits\
                .filter(func.lower(Hit.company).ilike(search_company))

        hits = hits\
            .join(Location, Hit.loc==Location.id)\
            .join(SearchTerm, Hit.term==SearchTerm.id)\
            .filter(or_(
                Hit.ignore == False,
                Hit.ignore == None))\
            .add_columns(
                Hit.id,
                Hit.title,
                Hit.updated_date.label('updated'),
                func.substr(Hit.summary, 0, 200).label('summary'),
                Hit.company,
                Location.city,
                Location.state,
                Hit.min_salary,
                Hit.max_salary,
                Hit.url,
                SearchTerm.text.label("search_term")
            )
        return hits

    def get_top_locations(self, how_many=10):
        return Hit\
            .query\
            .filter(or_(
                Hit.ignore == False,
                Hit.ignore == None))\
            .with_entities(func.count(Hit.loc).label('total'))\
            .join(Location, Hit.loc == Location.id)\
            .order_by(desc('total'))\
            .group_by(Location.id)\
            .add_column(Location.city)\
            .add_column(Location.state)\
            .all()

    def get_search_terms(self):
        return SearchTerm\
        .query\
        .with_entities(SearchTerm.text)\
        .order_by(SearchTerm.text)\
        .all()

    def get_locations(self):
        return Location\
            .query\
            .with_entities(
                Location.city, Location.state, Location.full)\
            .all()


class TopWords(HitSearch):
    def cellify(self, x):
        return f"<tr><td>{ x.word }</td>"\
            f"<td>{ x.total }</td></tr>"

    def get(self, how_many=10):
        data = WordCorpusCount\
            .query\
            .with_entities(WordCorpusCount.total)\
            .join(UniqueWords, WordCorpusCount.word==UniqueWords.id)\
            .order_by(WordCorpusCount.total.desc())\
            .add_column(UniqueWords.word)\
            .limit(how_many)
        return marshal_with(data, self.cellify)


class CompaniesHiring(HitSearch):
    def cellify(self, x):
        return f"<tr><td>{x.name}</td>"\
            f"<td>{'{:,.0f}'.format(x.total)}</td></tr>"
    def get(self, how_many=100):
        data = Hit\
            .query\
            .filter(or_(
                Hit.ignore == False,
                Hit.ignore == None))\
            .with_entities(
                Hit.company.label('name'),
                func.count(Hit.company).label('total'))\
            .group_by('name')\
            .order_by(desc('total'))
        return marshal_with(data, self.cellify)


class SalariesBySearchTerm(HitSearch):
    def cellify(self, x):
        return f"<tr><td>{x.text}</td>"\
            f"<td>${'{:,.0f}'.format(x.average_min_salary)}</td></tr>"

    def get(self, limit=50):
        data = Hit\
        .query\
        .filter(Hit.min_salary != None)\
        .filter(or_(
            Hit.ignore == False,
            Hit.ignore == None))\
        .with_entities(
            (func.sum(Hit.min_salary)/func.count(Hit.min_salary))
            .label('average_min_salary'))\
        .join(SearchTerm, Hit.term==SearchTerm.id)\
        .order_by(desc('average_min_salary'))\
        .add_column(SearchTerm.text)\
        .group_by(SearchTerm.text, Hit.term)\
        .limit(limit)
        return marshal_with(data, self.cellify)


class LocationBySearchTerm(HitSearch):
    def cellify(self, x):
        return f"<tr><td>{x.city}</td>"\
            f"<td>{x.state}</td>"\
            f"<td>{'{:,.0f}'.format(x.total)}</td></tr>"

    def get(self, limit=10):
        data =  Hit\
            .query\
            .filter(or_(
                Hit.ignore == False,
                Hit.ignore == None))\
            .with_entities(func.count(Hit.loc).label('total'))\
            .join(Location, Hit.loc == Location.id)\
            .order_by(desc('total'))\
            .group_by(Location.id)\
            .add_column(Location.city)\
            .add_column(Location.state)
        return marshal_with(data, self.cellify)


class MostJobsByLocation(HitSearch):
    def cellify(self, x):
        return f"<tr><td>{x.searchterm}.{x.location}</td>"\
            f"<td>{'{:,.0f}'.format(x.total)}</td></tr>"

    def get(self, limit):
        data = Hit\
        .query\
        .filter(or_(
            Hit.ignore == False,
            Hit.ignore == None))\
        .with_entities(func.count(Hit.loc).label('total'))\
        .join(Location, Hit.loc == Location.id)\
        .order_by(desc('total'))\
        .group_by(Location.id)\
        .add_column(Location.city)\
        .add_column(Location.state)
        return marshal_with(data, self.cellify)


class TopTerms(HitSearch):
    def cellify(self, x):
        return f"<tr><td>{x.search_term}</td>"\
            f"<td>{'{:,.0f}'.format(x.total)}</td></tr>"

    def get(self, limit=10):
        data = Hit\
        .query\
        .filter(or_(
            Hit.ignore == False,
            Hit.ignore == None))\
        .with_entities(func.count(Hit.id).label('total'))\
        .join(SearchTerm, Hit.term == SearchTerm.id)\
        .add_columns(SearchTerm.text.label('search_term'))\
        .group_by(SearchTerm.id, 'search_term')\
        .order_by(desc('total'))
        return marshal_with(data, self.cellify)


class TopTermLocCombos(HitSearch):
    def cellify(self, x):
        return f"<tr><td>{x.searchterm}.{x.location}</td>"\
            f"<td>{'{:,.0f}'.format(x.total)}</td></tr>"

    def get(self, limit=10):
        data = Hit\
            .query\
            .filter(or_(
                Hit.ignore == False,
                Hit.ignore == None))\
            .with_entities(func.count(Hit.term).label('total'))\
            .join(SearchTerm, Hit.term == SearchTerm.id)\
            .join(Location, Hit.loc == Location.id)\
            .add_column(Location.full.label('location'))\
            .add_column(SearchTerm.text.label('searchterm'))\
            .group_by(
                'location',
                'searchterm')\
            .order_by(desc('total'))
        return marshal_with(data, self.cellify)
