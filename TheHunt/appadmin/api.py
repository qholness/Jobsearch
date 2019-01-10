from TheHunt.db import db
from TheHunt.models import Hit, SearchTerm,\
    Location, Company,\
    WordCopus, WordCorpusCount, UniqueWords
from sqlalchemy import func
from tqdm import tqdm
from datetime import datetime, timedelta


def process_word(word):
    rplc = "`1234567890~!@#$%%^&*()-=+_}{][|\\ \"';:><.,/?”“ ’"
    for rpl in rplc:
        word = word.replace(rpl, ' ').strip()

    rplc = ['\n', '\b', '\r', '\t']

    for rpl in rplc:
        word = word.replace(rpl, '').strip()
    return word.lower()


def word_check(word):
    words = ['with', 'that', 'will']
    for w in words:
        if w in word:
            return False
    return True


def update_unique_words():
    UniqueWords.query.delete()
    db.session.commit()

    unique_words = set(word.word
        for word in WordCopus.query.with_entities(WordCopus.word).all())

    for word in unique_words:
        w = UniqueWords(word=word)
        db.session.add(w)

    db.session.commit()


def update_word_corp_count():
    WordCorpusCount.query.delete()
    db.session.commit()

    update = WordCopus\
        .query\
        .with_entities(func.count(WordCopus.word).label('total'))\
        .join(UniqueWords, WordCopus.word==UniqueWords.word)\
        .group_by(UniqueWords.id)\
        .add_column(UniqueWords.id)

    for u in update:
        db.session.add(WordCorpusCount(word=u.id, total=u.total))
    db.session.commit()


def update_word_corpus():
    WordCopus.query.delete()
    db.session.commit()

    summaries = Hit.query.add_column(Hit.summary)
    summaries = tqdm(summaries.all(), leave=True)
    for summary in summaries:
        if summary.summary is None:
            continue
        words = summary.summary.split()
        for word in words:
            if word is None:
                continue
            word = process_word(word)
            if word_check(word) is False:
                continue
            if len(word) < 4 or len(word) > 20:
                continue
            db.session.add(WordCopus(word=word))
        db.session.commit()


def prune_hits(num_days=7):
    days_ago = datetime.now() - timedelta(days=num_days)
    Hit\
        .query\
        .filter(Hit.created_date <= days_ago)\
        .delete()
    db.session.commit()
