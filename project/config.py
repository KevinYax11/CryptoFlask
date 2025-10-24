import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'una-llave-secreta-muy-dificil-de-adivinar'

    KEYS_DIR = os.path.join(BASE_DIR, '..', 'keys')

    if not os.path.exists(KEYS_DIR):
        os.makedirs(KEYS_DIR)