from flask import Flask
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from .config import Config
from .database import init_db
from .routes import predictions

limiter = Limiter(
    key_func=get_remote_address,
)

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    

    CORS(app, resources={
        r"/api/*": {
            "origins": ["http://localhost:5173", "http://localhost:3000"]
        }
    })
    
    limiter.init_app(app)
    init_db(app)
    from app.routes import drivers, teams
    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(drivers.bp)
    app.register_blueprint(teams.bp)
    app.register_blueprint(predictions.bp)
    
    @app.route('/')
    def index():
        return {'message': 'F1 Prophet API is running'}
    
    return app