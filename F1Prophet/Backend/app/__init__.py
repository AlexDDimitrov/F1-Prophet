from flask import Flask
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from .config import Config
from .database import init_db

limiter = Limiter(
    key_func=get_remote_address,
    #default_limits=["200 per day", "50 per hour"]
)

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.json.ensure_ascii = False
    
    CORS(app, resources={
        CORS(app, resources={
        r"/*": {
            "origins": [
                "http://localhost:5173", 
                f"http://localhost:{app.config.get('PORT', 5000)}", 
                "http://localhost:3000", 
                "https://f1-prophet.3labz.com"
            ],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    })
    
    limiter.init_app(app)

    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        "pool_recycle": 60,
        "pool_pre_ping": True,
        "pool_size": 5,
        "max_overflow": 10
    }

    init_db(app)

    from . import models

    from app.routes import drivers, teams, predictions, admin, leaderboards, profile, races
    from app.routes.auth import auth_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(drivers.bp)
    app.register_blueprint(teams.bp)
    app.register_blueprint(predictions.bp)
    app.register_blueprint(admin.bp)
    app.register_blueprint(leaderboards.bp)
    app.register_blueprint(profile.bp)
    app.register_blueprint(races.bp)
    
    @app.route('/')
    def index():
        return {'message': 'F1 Prophet API is running'}
    
    return app