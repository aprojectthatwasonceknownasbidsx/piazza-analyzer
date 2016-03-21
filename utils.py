from rake import Rake
import time
from datetime import datetime
from textblob import TextBlob


def post_to_dictionary(post):
    """
    Converts a post into a JSON-transferrable dictionary of relevant info
    and analyses. Currently, contains the following items:
        title - The title of the submission
        body   - The text of the ubmission
        tags    - The tags on the post 
        date    - DateTime Object when the comment was submitted
        time    - The time when the comment was submitted (epoch time)
        polarity- TextBlob's guess of the polarity of the comment
        subjectivity- Textblob's guess of subjectivity of comment.
    """
    p = dict()
    p['title'] = post.subject
    p['body'] = post.body
    p['tags'] = [topic.name for topic in post.topics]
    p['date'] = post.time
    p['time'] = time.mktime(post.time.timetuple())
    body_tb = TextBlob(post.body)
    p['polarity'] = body_tb.sentiment.polarity
    p['subjectivity'] = body_tb.sentiment.subjectivity
    return p


def post_to_table(post):
    """
    Converts a post into a list of relevant info
    and analyses (to be placed in table format):
    """
    p = list()
    p.append(post.index)  # Index
    p.append(post.subject)  # Title
    p.append("--".join([topic.name for topic in post.topics]))  # Categories
    p.append(datetime.strftime(post.time,'%m/%d/%Y'))  # Time
    return p


def comment_to_dictionary(comment):
    """
    Converts a comment into a JSON-transferrable dictonary of relevant
    info and analysis: Currently, contains the following items:
        comment - The text of the comment
        time    - The time when the comment was submitted
        polarity- TextBlob's guess of the polarity of the comment
        subjectivity- Textblob's guess of subjectivity of comment.
    """
    p = dict()
    p['comment'] = comment.text
    p['date'] = comment.time
    p['time'] = time.mktime(comment.time.timetuple())
    body_tb = TextBlob(comment.text)
    p['polarity'] = body_tb.sentiment.polarity
    p['subjectivity'] = body_tb.sentiment.subjectivity
    return p

def get_keywords(text):
    """
    Gets main keywords using RAKE Algorithm

    """
    rake = Rake("SmartStoplist.txt")
    keywords = rake.run(text)
    return [k[0] for k in keywords if len(k[0].split(" ")) <= 2 and k[1] > 1]

to_default = lambda x: max(1, x)