from flask import Flask
from flask_socketio import SocketIO

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dev-secret-key-change-in-production'
    
    socketio = SocketIO(app, cors_allowed_origins="*")
    
    from app.controllers.main_controller import main_bp
    from app.controllers.telemetry_controller import telemetry_bp
    from app.controllers.api_controller import api_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(telemetry_bp)
    app.register_blueprint(api_bp)
    
    return app, socketio