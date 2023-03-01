from flask import Flask, render_template, request
import requests
import json
import os

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return render_template('Home.html')

@app.route('/pokemon', methods=['GET', 'POST'])
def pokemon():
    print(request.method)
    if request.method == 'POST':
        name = request.form.get('name')
        print(name)
        url = f'https://pokeapi.co/api/v2/pokemon/{name}'
        response = requests.get(url)
        pokedex = []
        if response.ok:
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
            print(pokedex)
            return render_template('pokemon.html', pokedex=pokedex)
        else:
            error = 'That Pokemon is not in our database.'    
            return render_template('pokemon.html', error=error)
    return render_template('pokemon.html')