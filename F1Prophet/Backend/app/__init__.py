from flask import Flask
from flask_cors import CORS
from .config import Config
from .database import init_db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    

    CORS(app, resources={
        r"/api/*": {
            "origins": ["http://localhost:5173", "http://localhost:3000"]
        }
    })
    

    init_db(app)
    from app.routes import auth_bp, drivers, teams
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(drivers.bp)
    app.register_blueprint(teams.bp)
    
    @app.route('/')
    def index():
        return {'message': 'F1 Prophet API is running'}
    
    return app