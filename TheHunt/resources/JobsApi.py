from TheHunt.models import Hit, Location, SearchTerm
from flask_restful import Resource


class JobsApi(Resource):
    def __init__(self):
        self.base_query = Hit.query\
        .join(SearchTerm, Hit.term == SearchTerm.id)\
        .join(Location, Hit.loc == Location.id)\
        .with_entities(
            Location.full.label("location"),
            Hit.id,
            Hit.title,
            Hit.company,
            Hit.url,
            SearchTerm.text.label("search_term")
        )
        super().__init__()

    def get_ignored(self):
        return self.base_query\
            .filter(Hit.ignore == True)\
            .all()

    def get_applied(self):
        return self.base_query\
        .filter(Hit.applied == True)\
        .filter(Hit.ignore == False)\
        .all()

    def get_interested(self):
        return self.base_query\
        .filter(Hit.interested == True)\
        .filter(Hit.ignore == False)\
        .all()

    def get_interviewing(self):
        return self.base_query\
        .filter(Hit.interview == True)\
        .filter(Hit.ignore == False)\
        .all()

    def get_offers(self):
        return self.base_query\
        .filter(Hit.interview == True)\
        .filter(Hit.ignore == False)\
        .all()
