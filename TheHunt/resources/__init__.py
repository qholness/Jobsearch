from flask_restful import Resource, Api
from flask import request, session
from .HitByStatusCount import HitByStatusCount
from .JobsApi import JobsApi
from .HitSearch import (
    JobCount,
    HitSearch,
    CompaniesHiring,
    SalariesBySearchTerm,
    LocationBySearchTerm,
    MostJobsByLocation,
    TopTerms,
    TopTermLocCombos,
    TopWords
)
from .JobStatus import JobStatus, Interested, Applied, Interview, Offer, Ignore


api = Api()

class Sample(Resource):
    def get(self):
        return {"sample": "sample retrieved"}

job_status_api_url = '/api/job-status'

api.add_resource(Sample, '/sample')
api.add_resource(JobsApi, '/ignored-jobs')
api.add_resource(HitSearch, '/hits-search')
api.add_resource(HitByStatusCount, '/api/hit-by-status-count')
api.add_resource(JobCount, '/api/job-count')
api.add_resource(CompaniesHiring, '/api/hits/companies-hiring')
api.add_resource(SalariesBySearchTerm, '/api/hits/salaries-by-search-term')
api.add_resource(LocationBySearchTerm, '/api/hits/locations-by-search-term')
api.add_resource(TopTerms, '/api/hits/top-terms')
api.add_resource(TopTermLocCombos, '/api/hits/top-terms-and-locations')
api.add_resource(TopWords, '/api/hits/top-words')
api.add_resource(JobStatus, f'{ job_status_api_url }')
api.add_resource(Interested, f'{ job_status_api_url }/interested')
api.add_resource(Applied, f'{ job_status_api_url }/applied')
api.add_resource(Interview, f'{ job_status_api_url }/interview')
api.add_resource(Offer, f'{ job_status_api_url }/offer')
api.add_resource(Ignore, f'{ job_status_api_url }/ignore')