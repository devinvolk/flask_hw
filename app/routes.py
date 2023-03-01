from flask import render_template, request
import requests
from app.forms import PokeSearch
from app import app

@app.route('/', methods=['GET'])
def home():
    return render_template('Home.html')

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
            return render_template('pokemon.html', error=error)
    return render_template('pokemon.html', form=form)