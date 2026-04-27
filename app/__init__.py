from flask import Flask
import os

def create_app():
    # Get the parent directory (project root)
    template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates'))
    static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static'))
    
    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
    
    # Register blueprints
    from app.routes import main
    app.register_blueprint(main)
    
    return app
