from flask_wtf import FlaskForm
from wtforms import PasswordField, BooleanField, SubmitField
from wtforms.fields import EmailField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    email = EmailField('Email:', validators=[DataRequired(message="This field must be filled in.")])
    password = PasswordField('Password:', validators=[DataRequired(message="This field must be filled in."),
                                                   Length(min=6, message="The minimum password length is 6 characters.")])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign in')