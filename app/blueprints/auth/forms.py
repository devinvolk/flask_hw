from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField, EmailField
from wtforms.validators import DataRequired, EqualTo
from app.models import User 

class PokeSearch(FlaskForm):
    name = StringField('Name:')

class LoginForm(FlaskForm):
    email = EmailField('Email:', validators=[DataRequired()])
    password = PasswordField('Password:', validators=[DataRequired()])
    submit_btn = SubmitField('Login')

class SignUp(FlaskForm):
    first_name = StringField('First Name:')
    last_name = StringField('Last Name:')
    email = EmailField('Email:', validators=[DataRequired()])
    password = PasswordField('Password:', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password:', validators=[DataRequired(), EqualTo('password')])
    submit_btn = SubmitField('Sign Up')

class EditProfile(FlaskForm):
    first_name = StringField('First Name:')
    last_name = StringField('Last Name:')
    email = EmailField('Email:', validators=[DataRequired()])
    submit_btn = SubmitField('Update')