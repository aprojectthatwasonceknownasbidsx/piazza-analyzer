from rake import Rake
from textblob import TextBlob
import re

def get_keywords(text):
    """
    Gets main keywords using RAKE Algorithm

    """
    rake = Rake("SmartStoplist.txt")
    keywords = rake.run(text)
    return [k[0] for k in keywords if len(k[0].split(" ")) <= 2 and k[1] > 1]


def get_sentiment(text):
    body_tb = TextBlob(text)
    return body_tb.sentiment.polarity, body_tb.sentiment.subjectivity


def get_all_text(post):
    title = re.sub('\W+',' ', post.title)
    text = re.sub('\W+',' ', post.text)
    comments = [re.sub('\W+',' ', comment.text) for comment in post.comments]
    return title + " " + text + " " + " ".join(comments)

to_default = lambda x: max(1, x)