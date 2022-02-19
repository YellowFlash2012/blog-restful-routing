from flask_admin.contrib.sqla.view import ModelView
from flask_login import UserMixin
import datetime

from tentenblog import db, login_manager, admin


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    email = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), unique=True, nullable=False)

    # "author" refers to author property in BlogPost Class
    # posts = db.relationship("BlogPost", backref="author", lazy="dynamic")

# new_user = User(name="Sakura", email="sakura@konoha.org", password="willoffire")
# db.create_all()
# db.session.add(new_user)
# db.session.commit()

#posts = db.session.query(BlogPost).all()

##CONFIGURE TABLE


class BlogPost(db.Model):
    __tablename__ = "blog_posts"
    id = db.Column(db.Integer, primary_key=True)

    # create reference to the User object
    #author = db.relationship("User", backref="posts")

    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)

    # create Foreign keys
    # author_id = db.Column(db.Integer, db.ForeignKey("user.id"))

# db.create_all()
admin.add_view(ModelView(User, db.session))