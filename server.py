from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from models import Post, Comment, Topic 
from datetime import datetime
from textblob import TextBlob
import time
from rake import Rake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class PostConfig:
    """
    Class used by get_posts, and get_table_posts 
    to get the specific posts (as filtered)
    """
    def reset():
        PostConfig.startdate = datetime.strptime('01012000','%m%d%Y')
        PostConfig.enddate = datetime.now()
        PostConfig.limit = 500
        PostConfig.topics = None

    def get():
        return db.session.query(Post).filter(
            Post.time.between(PostConfig.startdate,PostConfig.enddate)
            ).limit(PostConfig.limit).all()


class CommentConfig:
    """
    Class used by get_comments,
    to get the specific comments (as filtered)
    """
    def reset():
        CommentConfig.startdate = datetime.strptime('01012000','%m%d%Y')
        CommentConfig.enddate = datetime.now()
        CommentConfig.limit = 500

    def get():
        return db.session.query(Comment).filter(
            Post.time.between(CommentConfig.startdate,CommentConfig.enddate)
            ).limit(CommentConfig.limit).all()

PostConfig.reset()
CommentConfig.reset()


@app.route('/')
def home():
    """
        Serves the main page
    """
    f = open("static/analytics.html")
    return f.read()


def post_to_dictionary(post):
    """
    Converts a post into a dictionary of relevant info
    and analyses
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
    Converts a post into a dictionary of relevant info
    and analyses
    """
    p = list()
    p.append(post.index)  # Index
    p.append(post.subject)  # Title
    p.append("--".join([topic.name for topic in post.topics]))  # Categories
    p.append(datetime.strftime(post.time,'%m/%d/%Y'))  # Time
    return p


def comment_to_dictionary(comment):
    """
    Converts a comment into a dicitonary of relevant
    info and analysis
    """
    p = dict()
    p['comment'] = comment.text
    p['date'] = comment.time
    p['time'] = time.mktime(comment.time.timetuple())
    body_tb = TextBlob(comment.text)
    p['polarity'] = body_tb.sentiment.polarity
    p['subjectivity'] = body_tb.sentiment.subjectivity
    return p

to_default = lambda x: max(1, x)


@app.route('/get/post')
def get_posts():
    posts = PostConfig.get()
    postdata = [post_to_dictionary(post) for post in posts]
    return jsonify(data=postdata)


@app.route('/get/post_table')
def get_post_table():
    posts = PostConfig.get()
    postdata = [post_to_table(post) for post in posts]
    return jsonify(data=postdata)


@app.route('/get/comments')
def get_comments():
    comments = CommentConfig.get()
    commentdata = [comment_to_dictionary(comment) for comment in comments]
    return jsonify(data=commentdata)


@app.route('/get/topics')
def get_topics():
    topics = db.session.query(Topic).all()
    return jsonify(data=[topic.name for topic in topics])


@app.route('/get/post/<int:post_id>')
def get_post(post_id):
    post_id = to_default(post_id)
    post = db.session.query(Post).get(post_id)
    dictionary = post_to_dictionary(post)
    dictionary['comments'] = [comment_to_dictionary(comm) for comm in post.children]
    text = post.subject + " " + post.body + " ".join([c.text for c in post.children])
    dictionary['topics'] = get_keywords(text)
    return jsonify(data=dictionary)

def get_keywords(text):
    rake = Rake("SmartStoplist.txt")
    keywords = rake.run(text)
    return [k[0] for k in keywords if len(k[0].split(" ")) <= 2 and k[1] > 1]

@app.route('/select/post')
def select_post():
    startdate = request.args.get('start',None)
    if startdate:
        PostConfig.startdate = datetime.strptime(startdate, '%m%d%Y')
        print("Updating start date to ", startdate)

    enddate = request.args.get('end',None)
    if enddate:
        PostConfig.enddate = datetime.strptime(enddate,'%m%d%Y')
        print("Updating end date to ", enddate)

    return ''


@app.route('/select/topic')
def select_topic():
    topic = request.args.get('topic',None)
    if topic:
        PostConfig.topics = topic
        CommentConfig.topics = topic


@app.route('/select/comment')
def select_comment():
    startdate = request.args.get('start',None)
    if startdate:
        CommentConfig.startdate = datetime.strptime(startdate, '%m%d%Y')
        print("Updating start date to ", startdate)
    enddate = request.args.get('end',None)
    if enddate:
        CommentConfig.enddate = datetime.strptime(enddate,'%m%d%Y')
        print("Updating end date to ", enddate)

    return ''

@app.route('/select/reset')
def reset():
    PostConfig.reset()
    CommentConfig.reset()
    return ''

if __name__ == '__main__':
    app.debug = True
    app.run()
