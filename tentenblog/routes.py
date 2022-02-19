from tentenblog import app, db
from tentenblog.models import *
from tentenblog.forms import *
from flask import render_template, redirect, url_for, request, flash, abort

# flask security
from flask_login import login_user, login_required, current_user, logout_user, login_manager
from werkzeug.security import generate_password_hash, check_password_hash

from functools import wraps

# create admin_only decorator similar to login_required
def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # if id is not 1 then abort
        if current_user.id != 1:
            return abort(403)
        return f(*args, **kwargs)
    return decorated_function

    
# ********************routes**********************


@app.route('/')
def get_all_posts():
    logged_in = login_user(current_user)
    # to display the posts in descending order, newest first
    posts = BlogPost.query.order_by(BlogPost.id.desc())
    return render_template("index.html", all_posts=posts, logged_in=logged_in)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    form.validate_on_submit()

    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash("Email already used")
            return redirect(url_for("login"))
        new_user = User(
            name=form.name.data,
            email=form.email.data,
            password=generate_password_hash(
                form.password.data,
                method='pbkdf2:sha256',
                salt_length=8)
        )

        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        return redirect(url_for("get_all_posts"))

    return render_template('register.html', form=form)


# @login_manager.user_loader
# def load_user(id):
#     return User.query.get(int(id))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.query.filter_by(email=email).first()
        if not user:
            flash("Invalid credentials")
            return redirect(url_for("login"))

        elif not check_password_hash(user.password, password):
            flash("Invalid credentials")
            return redirect(url_for("login"))

        else:
            login_user(user)
            return redirect(url_for("get_all_posts"))
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("get_all_posts"))


@app.route("/post/<int:index>")
def show_post(index):
    posts = BlogPost.query.order_by(BlogPost.id.desc()).all()
    requested_post = None
    for blog_post in posts:
        if blog_post.id == index:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)


@app.route("/new-post", methods=["GET", "POST"])
# @admin_only
@login_required
def new_post():
    new_post_form = CreatePostForm()
    new_post_form.validate_on_submit()
    today = datetime.datetime.now().strftime("%B %d, %Y")
    #blog_content = new_post_form.body.data('ckeditor')
    #random_image = 'https://source.unsplash.com/random/450x300'

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


@app.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
# @admin_only
@login_required
def edit_post(post_id):
    post = BlogPost.query.get(post_id)
    edit_post_form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        body=post.body,
        author=post.author,
        img_url=post.img_url
    )

    if edit_post_form.validate_on_submit():
        post.title = edit_post_form.title.data
        post.subtitle = edit_post_form.subtitle.data
        post.body = edit_post_form.body.data
        post.author = edit_post_form.author.data
        post.img_url = edit_post_form.img_url.data
        db.session.commit()

        return redirect(url_for('show_post', index=post.id))

    return render_template('make-post.html', form=edit_post_form, is_edit=True)


@app.route("/delete/<post_id>")
# @admin_only
def delete(post_id):

    post_to_delete = BlogPost.query.get(post_id)
    db.session.delete(post_to_delete)
    db.session.commit()

    return redirect(url_for('get_all_post'))


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")
