from TheHunt.models import SearchTerm, Location, Hit
from sqlalchemy import asc, func
import json

class SearchVector:
    def __init__(self, term=None, loc=None, termid=None, locid=None):
        self.term = term
        self.loc = loc
        self.termid = termid
        self.locid = locid
        self.url = f"https://www.indeed.com/jobs?q="\
            f"{self.term}&l={self.loc}"

    def jsonify(self):
        return json.dumps(
            dict(
                term=self.term,
                loc=self.loc,
                termid=self.termid,
                locid=self.locid,
                url=self.url                
            )
        )

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
