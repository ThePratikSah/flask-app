# importing all the flask packages for the project
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import json


with open('config.json', 'r') as c:
    params = json.load(c)["params"]

local_server = params['local_server']
# constructor
app = Flask(__name__)
if (local_server):
    # uri for local server
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
    # uri for prod server
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
db = SQLAlchemy(app)

# class for database 
class Contacts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    phone = db.Column(db.String(12), nullable=False)
    msg = db.Column(db.String(120), nullable=False)

class Posts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    slug = db.Column(db.String(21), nullable=False)
    content = db.Column(db.String(120), nullable=False)
    post_by = db.Column(db.String(21), nullable=False)
    file_name = db.Column(db.String(21), nullable=False)
    date = db.Column(db.String(12), nullable=False)

# different routes
# endpoint for home page
@app.route('/')
def home():
    posts = Posts.query.filter_by().all()[0: params['no_of_posts']]
    return render_template('index.html', params=params, posts=posts)

# endpoint for about
@app.route('/about')
def about():
    return render_template('about.html', params=params)

# endpoint for login
@app.route('/login')
def login():
    return render_template('login.html', params=params)

# endpoint for post
@app.route('/post/<string:post_slug>', methods=['GET'])
def post(post_slug):
    post = Posts.query.filter_by(slug=post_slug).first()
    return render_template('post.html', params=params, post=post)

# endpoint for contact
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        msg = request.form.get('msg')
        entry = Contacts(name=name, email=email, phone=phone, msg=msg)
        db.session.add(entry)
        db.session.commit()
    return render_template('/contact.html', params=params)


app.run(debug=True)
