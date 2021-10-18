from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField

from config import *
import datetime



## Delete this code:
# import requests
# posts = requests.get("https://api.npoint.io/43644ec4f0013682fc0d").json()

app = Flask(__name__)
app.config['SECRET_KEY'] = token
ckeditor = CKEditor(app)
Bootstrap(app)

##CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

##CONFIGURE TABLE
class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)


posts = db.session.query(BlogPost).all()

##WTForm
class CreatePostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()], render_kw={'autofocus': True})
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    author = StringField("Author", validators=[DataRequired()])
    img_url = StringField("Blog Image URL", validators=[DataRequired(), URL()])
    body = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField("Submit Post")


@app.route('/')
def get_all_posts():
    posts = BlogPost.query.order_by(BlogPost.id.desc())
    return render_template("index.html", all_posts=posts)


@app.route("/post/<int:index>")
def show_post(index):
    requested_post = None
    for blog_post in posts:
        if blog_post.id == index:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)


@app.route("/new-post", methods=["GET", "POST"])
def new_post():
    new_post_form = CreatePostForm()
    new_post_form.validate_on_submit()
    today = datetime.datetime.now().strftime("%B %d, %Y")
    # blog_content = new_post_form.body.data('ckeditor')
    # random_image = 'https://source.unsplash.com/random/450x300'

    if new_post_form.validate_on_submit():
        new_blog = BlogPost(
            title=new_post_form.title.data,
            subtitle=new_post_form.subtitle.data,
            date=today,
            body=new_post_form.body.data,
            author=new_post_form.author.data,
            img_url=new_post_form.img_url.data
            
            )
        
        db.session.add(new_blog)
        db.session.commit()

        return redirect(url_for('get_all_posts'))
    
    return render_template('make-post.html', form=new_post_form)

@app.route("/edit_post")
def edit_post():
    pass

@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")

if __name__ == "__main__":
    #app.run(host='0.0.0.0', port=5000)
    app.run(debug=True)
