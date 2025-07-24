from flask import Blueprint, jsonify
from app.models.usv_data import USVDataManager

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/usv/current')
def get_current_data():
    try:
        data_manager = USVDataManager()
        current_data = data_manager.get_current_data()
        return jsonify(current_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/usv/history')
def get_history():
    try:
        data_manager = USVDataManager()
        history = data_manager.get_history(limit=100)
        return jsonify(history)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/usv/path')
def get_path():
    try:
        data_manager = USVDataManager()
        path = data_manager.get_path_data()
        return jsonify(path)
    except Exception as e:
        return jsonify({'error': str(e)}), 500