import os
from flask import Flask
from .config import Config, BASE_DIR

template_dir = os.path.join(BASE_DIR, '..', 'templates')
static_dir = os.path.join(BASE_DIR, '..', 'static')


def create_app():
    app = Flask(__name__, 
                template_folder=template_dir, 
                static_folder=static_dir)
    
    app.config.from_object(Config)
    
    with app.app_context():
        from . import routes 
        
    return app