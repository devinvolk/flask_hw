from app import db, login
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

teamtable = db.Table('teamtable',
    db.Column('pokemon_id', db.Integer, db.ForeignKey('poke_table.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
)

class PokeTable(db.Model):
    __name__ = 'poketable'
    id = db.Column(db.Integer, primary_key=True)
    pokemon_name = db.Column(db.String, nullable=False)
    ability = db.Column(db.String, nullable=False)
    base_experience = db.Column(db.Integer, nullable=False)
    attack_base_stat = db.Column(db.Integer, nullable=False)
    hp_base_stat = db.Column(db.Integer, nullable=False)
    defense_base_stat = db.Column(db.Integer, nullable=False)
    front_shiny = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def from_dict(self, data):
        self.pokemon_name = data['Name']
        self.ability = data['Ability']
        self.base_experience = data['Base Experience']
        self.attack_base_stat = data['Attack Base Stat']
        self.hp_base_stat = data['HP Base Stat']
        self.defense_base_stat = data['Defense Base Stat']
        self.front_shiny = data['Front Shiny']
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

class User(UserMixin, db.Model):
    __name__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String)
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    team = db.relationship('PokeTable', 
        secondary = teamtable,
        backref='users', 
        lazy='dynamic')

    # hashes our password
    def hash_password(self, original_password):
        return generate_password_hash(original_password)

    # checks the hashed password
    def check_hash_password(self, login_password):
        return check_password_hash(self.password, login_password)
    
    #add a pokemon to a users team
    def add_pokemon(self, pokemon):
        self.team.append(pokemon)
        db.session.commit()

    #remove a pokemon from a users team
    def remove_pokemon(self, pokemon):
        self.team.remove(pokemon)
        db.session.commit()
    
    def check_team(self, pokemon):
        if pokemon in self.team.all():
            return False
        else:
            return True

    def max_attack(self, pokemon):
        max_attack = 0
        for pokemon in self.team:
            max_attack += int(pokemon.attack)
            return max_attack
            
    # Use this method to register our user attributes
    def from_dict(self, data):
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = self.hash_password(data['password'])
    
    #for modifying user data in the db
    def update_from_dict(self, data):
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']

    # Save the user to database
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)