from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.simple import PasswordField
from wtforms.validators import DataRequired, URL, Email
from flask_ckeditor import CKEditorField

##WTForm
class CreatePostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()], render_kw={'autofocus': True})
    
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    
    author = StringField("Author", validators=[DataRequired()])
    
    img_url = StringField("Blog Image URL", validators=[DataRequired(), URL()])
    
    body = CKEditorField("Blog Content", validators=[DataRequired()])
    
    submit = SubmitField("Submit Post")


class RegisterForm(FlaskForm):
    name = StringField("Full Name", validators=[DataRequired()], render_kw={'autofocus': True})
    email = StringField("Your email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("SIGN ME UP")


class LoginForm(FlaskForm):
    email = StringField("Your email", validators=[DataRequired(), Email()], render_kw={'autofocus': True})
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("LOG ME IN")
