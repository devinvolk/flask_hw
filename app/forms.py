from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField

class PokeSearch(FlaskForm):
    name = StringField('Name:')
    submit_btn = SubmitField('Search')