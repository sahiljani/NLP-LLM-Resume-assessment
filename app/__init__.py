from flask import Flask
from app.controllers.resume_parser_controller import resume_parser_bp
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.config.Config')
    app.config['UPLOAD_FOLDER'] = 'uploads'
    
    # Ensure the upload folder exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Register Blueprints
    app.register_blueprint(resume_parser_bp, url_prefix='/')

    return app
