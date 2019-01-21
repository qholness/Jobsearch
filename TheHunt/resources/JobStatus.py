from TheHunt.models import Hit, Location, SearchTerm
from flask_restful import Resource
from flask import request, jsonify
from TheHunt.db import db


def fetch_job(func):
    def _decor(self, *args, **kwargs):
        jobid = request.args.get('jobid').replace("Ampersand", "&")
        if jobid:
            job = Hit.query.filter(Hit.id == jobid).first()
            if job:
                return func(self, job, *args, **kwargs)
        return f"Couldn't find {jobid}."
    return _decor




class JobStatus(Resource):
    pass


class Interested(JobStatus):
    @fetch_job
    def post(self, job):
        if job.interested is True:
            job.interested = False
            job.applied = False
            job.interview = False
            job.offer = False
            ret = f"Uninterested: { job.id }."
        else:
            job.interested = True
            job.ignore = False
            ret = f"Interested: { job.id }."
        db.session.add(job)
        db.session.commit()
        return jsonify(ret)


class Applied(JobStatus):
    @fetch_job
    def post(self, job):
        if job.applied is True:
            job.applied = False
            job.interview = False
            job.offer = False
            ret = f"Unapplied: { job.id }."
        else:
            job.interested = True
            job.ignore = False
            job.applied = True
            ret = f"Adding to applied: { job.id }."
        db.session.add(job)
        db.session.commit()
        return ret



class Interview(JobStatus):
    @fetch_job
    def post(self, job):
        if job.interview is True:
            job.interview = False
            job.offer = False
            ret = f"Uninterviewing: { job.id }."
        else:
            job.interview = True
            ret = f"Interviewing: { job.id }."
        db.session.add(job)
        db.session.commit()
        return jsonify(ret)
        


class Offer(JobStatus):
    @fetch_job
    def post(self, job):
        if job.offer is True:
            job.offer = False
            ret = f"Unoffering: { job.id }."
        else:
            job.offer = True
            ret = f"Offered!: { job.id }."
        db.session.add(job)
        db.session.commit()
        return jsonify(ret)


class Ignore(JobStatus):
    @fetch_job
    def post(self, job):
        if job.ignore is True:
            job.ignore = False
            job.interested = False
            job.applied = False
            ret = f"Unignoring: { job.id }."
        else:
            job.ignore = True
            job.interested = False
            job.applied = False
            job.offer = False
            job.interview = False
            ret = f"Ignoring: { job.id }."
        db.session.add(job)
        db.session.commit()
        return jsonify(ret)