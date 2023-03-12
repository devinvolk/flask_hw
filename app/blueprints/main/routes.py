from flask import render_template, request, flash, redirect, url_for
import requests
from app.blueprints.auth.forms import PokeSearch
from . import main
from flask_login import login_required, current_user
from app.models import PokeTable, User

@main.route('/', methods=['GET'])
@login_required
def home():
    return render_template('home.html')

@main.route('/pokemon', methods=['GET', 'POST'])
@login_required
def pokemon():
    form = PokeSearch()
    if request.method == 'POST':
        if request.form['submit-btn'] == 'Search':
            name = request.form.get('name').lower()
            url = f'https://pokeapi.co/api/v2/pokemon/{name}'
            response = requests.get(url)
            if response.ok:
                pokedex = []
                pokemon_dict= {
                    'Name': name.title(),
                    'Ability': response.json()['abilities'][0]['ability']['name'].title(),
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

@main.route('/catch/<string:name>', methods=['GET', 'POST'])
@login_required
def catch(name):
    queried_pokemon = PokeTable.query.filter_by(pokemon_name=name).first()
    print(queried_pokemon)
        # check if the pokemon is already on the user's team
    if queried_pokemon:
        #checks to see if the user already has the pokemon on their team
        if current_user.check_team(queried_pokemon):
            #count of user_id is 5, do not add pokemon
            if len(current_user.team.all()) < 5:
                #link existing pokemon data from PokeTable to the User_id
                current_user.add_pokemon(queried_pokemon)
                flash(f'The {name.title()} was added to your team!', 'success')
                return redirect(url_for('main.pokemon'))
            else:    
                flash(f'Could not add {name.title()} to your team. You already have 5 Pokemon', 'danger')
                return redirect(url_for('main.pokemon'))
        else:
            flash(f'{name.title()} is already on your team', 'danger')
            return redirect(url_for('main.pokemon'))
    else:
        url = f'https://pokeapi.co/api/v2/pokemon/{name.lower()}'
        response = requests.get(url)
        pokemon_dict= {
            'Name': name.title(),
            'Ability': response.json()['abilities'][0]['ability']['name'].title(),
            'Base Experience': response.json()['base_experience'],
            'Front Shiny': response.json()['sprites']['front_shiny'],
            'Attack Base Stat': response.json()['stats'][1]['base_stat'],
            'HP Base Stat': response.json()['stats'][0]['base_stat'],
            'Defense Base Stat': response.json()['stats'][2]['base_stat']
        }
        if len(current_user.team.all()) < 5:
            new_pokemon = PokeTable()
            new_pokemon.from_dict(pokemon_dict)
            new_pokemon.save_to_db()
            current_user.add_pokemon(new_pokemon)
            flash('The Pokemon was added to your team!', 'success')
            return redirect(url_for('main.pokemon'))
        else:    
            flash(f'Could not add {pokemon_dict["Name"].title()} to your team. You already have 5 Pokemon', 'danger')
            return redirect(url_for('main.pokemon'))

@main.route('/team', methods=['GET', 'POST'])
@login_required
def team():
    return render_template('team.html')

@main.route('/release/<string:name>', methods=['GET', 'POST'])
@login_required
def release(name):
    squad = current_user.team
    for pokemon in squad:
        if pokemon.pokemon_name == name:
            current_user.remove_pokemon(pokemon)
    flash(f'{name} was removed from your team', 'success')
    return redirect(url_for('main.team'))