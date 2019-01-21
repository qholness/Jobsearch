from flask_restful import Resource, marshal_with, fields
from TheHunt.models import Hit


resource_fields = dict(
    ignore=fields.Integer,
    interested=fields.Integer,
    applied=fields.Integer,
    interview=fields.Integer,
    offer=fields.Integer
)


class HitCounter(object):
    def __init__(self, ignore, interested, applied, interview, offer):
        self.ignore = ignore
        self.interested = interested
        self.applied = applied
        self.interview = interview
        self.offer = offer

class HitByStatusCount(Resource):
    @marshal_with(resource_fields)
    def get(self):
        return HitCounter(
            Hit.query.filter(Hit.ignore == True).count(),
            Hit.query.filter(Hit.interested == True).count(),
            Hit.query.filter(Hit.applied == True).count(),
            Hit.query.filter(Hit.interview == True).count(),
            Hit.query.filter(Hit.offer == True).count()
        )
