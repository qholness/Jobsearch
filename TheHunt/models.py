from TheHunt.db import db
from datetime import datetime


def string_col(*args, **kwargs):
    return db.Column(db.Text(*args, **kwargs))


class SearchTerm(db.Model):
    __tablename__ = 'search_term'
    id = db.Column(db.Integer, primary_key=True)
    created_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    updated_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    text = string_col()
    hit = db.relationship("Hit", cascade="all, delete-orphan")


class Location(db.Model):
    __tablename__ = 'locations'
    id = db.Column(db.Integer, primary_key=True)
    created_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    updated_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    city = string_col()
    state = string_col()
    full = string_col()
    hit = db.relationship("Hit", cascade="all, delete-orphan")


class Hit(db.Model):
    __tablename__ = 'hits'
    jid = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.Text, index=True)
    created_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    updated_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    term = db.Column(db.ForeignKey('search_term.id'))
    loc = db.Column(db.ForeignKey('locations.id'))
    title = string_col()
    # company = db.Column(db.ForeignKey('company.id'))
    company = string_col()
    salary = string_col()
    min_salary = db.Column(db.Numeric)
    max_salary = db.Column(db.Numeric)
    summary = db.Column(db.String(500))
    url = string_col()


class WordCopus(db.Model):
    __tablename__ = 'word_copus'
    id = db.Column(db.Integer, primary_key=True)
    word = string_col()


class UniqueWords(db.Model):
    __tablename__ = 'unique_words'
    id = db.Column(db.Integer, primary_key=True)
    word = string_col()


class WordCorpusCount(db.Model):
    __tablename__ = 'word_copus_count'
    word = db.Column(db.ForeignKey('unique_words.id'), primary_key=True)
    total = db.Column(db.Integer)


class Company(db.Model):
    __tablename__ = 'company'
    created_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    updated_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    id = db.Column(db.Integer, primary_key=True)
    name = string_col()


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = string_col()
    password = string_col()
