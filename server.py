from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from models import Post, Comment, Topic 
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


@app.route('/')
def hello_world():
    return jsonify(a=str(db.session.query(Post).first()))


def post_to_dictionary(post):
    p = dict()
    p['title'] = post.subject
    p['body'] = post.body
    p['topics'] = [topic.name for topic in post.topics]
    p['date'] = post.time
    return p

to_default = lambda x: max(1,x)

@app.route('/get/post')
def get_posts():
    posts = db.session.query(Post).limit(100).all()
    postdata = list()
    for post in posts:
        postdata.append(post_to_dictionary(post))
    return jsonify(results=postdata)

@app.route('/get/post/<int:post_id>')
def get_post(post_id):
    post_id = to_default(post_id)
    post = db.session.query(Post).get(post_id)
    return jsonify(results=post_to_dictionary(post))

@app.route('/select/post')
def select():
    startdate = request.args.get('start','01012000')
    enddate =  request.args.get('end',datetime.strftime(datetime.now(),'%m%d%Y'))
    startdate = datetime.strptime(startdate,'%m%d%Y')
    enddate = datetime.strptime(enddate,'%m%d%Y')
    print(db.session.query(Post).filter(Post.time.between(startdate,enddate)).first())
    return "HI"

if __name__ == '__main__':
    app.debug = True
    app.run()
