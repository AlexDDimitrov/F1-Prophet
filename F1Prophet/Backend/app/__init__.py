from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    

    CORS(app, resources={
        r"/api/*": {
            "origins": ["http://localhost:5173", "http://localhost:3000"]
        }
    })
    
    from app.routes import drivers, teams
    app.register_blueprint(drivers.bp)
    app.register_blueprint(teams.bp)
    
    @app.route('/')
    def index():
        return {'message': 'F1 Prophet API is running'}
    
    return app