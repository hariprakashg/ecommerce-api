from flask import Flask
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os

mongo = PyMongo()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    
    # Force load environment variables
    load_dotenv()
    
    uri = os.getenv("MONGO_URI")
    secret = os.getenv("JWT_SECRET")

    # Debug: This will print in your terminal so we can see if it's working
    print(f"--- DEBUG: URI FOUND: {uri is not None} ---")

    app.config["MONGO_URI"] = uri
    app.config["JWT_SECRET_KEY"] = secret

    # Initialize extensions with the app context
    with app.app_context():
        mongo.init_app(app)
        jwt.init_app(app)

    from .auth import auth_bp
    from .routes import api_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(api_bp, url_prefix='/api')

    return app