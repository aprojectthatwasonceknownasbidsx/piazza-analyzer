import sys
sys.path.append('..')

from textblob import TextBlob
from models import Post, Comment, Tag
from utils import *

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine('sqlite:///../test.db', echo=False)
Session = sessionmaker(bind=engine)
session = Session()


def rakeAll(num):
        posts = session.query(Post).limit(num).all()
        for i in posts:
            get_keywords(i.text)


def tbAll(num):
        posts = session.query(Post).limit(num).all()
        for i in posts:
            tb = TextBlob(i.text)
            tb.sentiment.polarity
            tb.sentiment.subjectivity

import timeit


def main():
    for num in range(0,100,10):
        print("Rake for ", num, ": ",
              timeit.timeit('rakeAll(%d)' % num, number=10,
              setup = "from __main__ import rakeAll")/10)
        print("TextBlob for ", num, ": ",
              timeit.timeit('tbAll(%d)' % num, number=10,
              setup = "from __main__ import tbAll")/10)
 