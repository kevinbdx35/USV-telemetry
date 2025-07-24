from flask import Blueprint, request, jsonify
from app.services.telemetry_service import TelemetryService

telemetry_bp = Blueprint('telemetry', __name__, url_prefix='/telemetry')

@telemetry_bp.route('/data', methods=['POST'])
def receive_telemetry():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        return jsonify({'status': 'success', 'message': 'Data received'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@telemetry_bp.route('/status')
def get_status():
    return jsonify({
        'service': 'telemetry',
        'status': 'active',
        'connected_devices': 1
    })