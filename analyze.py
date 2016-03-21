from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Post, Comment, PostAnalysis, Keyword
from utils import *


class PiazzaAnalyzer:

    def __init__(self):
        self.engine = create_engine('sqlite:///test.db', echo=False)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def get_keyword(self, name):
        """
        Returns the topic if it exists, and otherwise creates it
        """

        keyword = self.session.query(Keyword).filter(
            Keyword.name == name).first()
        if not keyword:
            keyword = Keyword(name)
            self.session.add(keyword)
            self.session.commit()
        return keyword

    def analyze_post(self, post):
        text = get_all_text(post)
        polarity, subjectivity = get_sentiment(text)
        keywords = get_keywords(text)
        analysis = PostAnalysis(polarity, subjectivity)
        for kw in keywords:
            keyword = self.get_keyword(kw)
            analysis.keywords.append(keyword)
        post.analysis.append(analysis)
        self.session.commit()

    def analyze_posts(self):
        posts = self.session.query(Post).all()
        for post in posts:
            post.analysis = []
            self.analyze_post(post)
            print(post.index,post.title)