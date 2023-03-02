from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField, EmailField
from wtforms.validators import DataRequired

class PokeSearch(FlaskForm):
    name = StringField('Name:')
    submit_btn = SubmitField('Search')

class LoginForm(FlaskForm):
    email = EmailField('Email:', validators=[DataRequired()])
    password = PasswordField('Password:', validators=[DataRequired()])
    submit_btn = SubmitField('Login')

class SignUp(FlaskForm):
    first_name = StringField('First Name:')
    last_name = StringField('Last Name:')
    email = EmailField('Email:', validators=[DataRequired()])
    password = PasswordField('Passwrord:', validators=[DataRequired()])
    submit_btn = SubmitField('Sign Up')