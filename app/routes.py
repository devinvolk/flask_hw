from flask import render_template, request, redirect, url_for, flash
import requests
from app.forms import PokeSearch, LoginForm, SignUp
from app import app
from app.models import User
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, current_user, login_required

@app.route('/', methods=['GET'])
@login_required
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data.lower()
        password = form.password.data
        
        # Query user from db
        queried_user = User.query.filter_by(email=email).first()
        if queried_user and check_password_hash(queried_user.password, password):
            login_user(queried_user)
            flash(f'Successfully Logged In! Welcome back, {queried_user.first_name}!', 'success')            
            return redirect(url_for('home'))
        else:
            error = 'Incorrect Email/Password!'
            flash(f'{error}', 'danger')
            return render_template('login.html', error=error, form=form)
    return render_template('login.html', form=form)

@app.route('/signup', methods=['Get', 'POST'])
def signup():
    form = SignUp()
    if request.method == 'POST' and form.validate_on_submit():
        new_user_data = {
            'first_name': form.first_name.data.title(),
            'last_name': form.last_name.data.title(),
            'email': form.email.data.lower(),
            'password': form.password.data
        }
        new_user = User()

        # Implementing values from our form data for our instance
        new_user.from_dict(new_user_data)

        # Save user to database
        new_user.save_to_db()

        flash('You have successfully registered!', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)

@app.route('/logout', methods=['GET'])
@login_required
def logout():
    if current_user:
        logout_user()
        flash('You have logged out!', 'warning')
        return redirect(url_for('login'))

@app.route('/pokemon', methods=['GET', 'POST'])
def pokemon():
    print(request.method)
    form = PokeSearch()
    if request.method == 'POST':
        name = request.form.get('name')
        url = f'https://pokeapi.co/api/v2/pokemon/{name}'
        response = requests.get(url)
        if response.ok:
            pokedex = []
            pokemon_dict= {
                'Name': name,
                'Ability': response.json()['abilities'][0]['ability']['name'],
                'Base Experience': response.json()['base_experience'],
                'Front Shiny': response.json()['sprites']['front_shiny'],
                'Attack Base Stat': response.json()['stats'][1]['base_stat'],
                'HP Base Stat': response.json()['stats'][0]['base_stat'],
                'Defense Base Stat': response.json()['stats'][2]['base_stat']
        }   
            pokedex.append(pokemon_dict)
            return render_template('pokemon.html', form=form, pokedex=pokedex)
        else:
            error = 'That Pokemon is not in our database.'    
            return render_template('pokemon.html', error=error, form=form)
    return render_template('pokemon.html', form=form)