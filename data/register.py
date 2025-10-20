from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField
from wtforms.fields import EmailField
from wtforms.validators import DataRequired, Length


class RegisterForm(FlaskForm):
    email = EmailField('E-mail:', validators=[DataRequired()])
    password = PasswordField('Password:', validators=[DataRequired(message="This field must be filled in."),
                                                   Length(min=6, message="The minimum password length is 6 characters.")],
                             default='123456')
    password_again = PasswordField('Repeat password:',
                                   validators=[DataRequired(message="This field must be filled in."),
                                               Length(min=6, message="The minimum password length is 6 characters.")])
    name = StringField('Name:', validators=[DataRequired(message="This field must be filled in.")])
    submit = SubmitField('Submit')