import os

class Config():
    SECRET_KEY=os.environ.get('SECRET_KEY')
    REGISTERED_USERS = {
    'dylan@gmail.com': {
        'name': 'Dylan',
        'password': 'ilovemydog'
    }
}