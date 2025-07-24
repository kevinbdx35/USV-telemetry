from app import create_app
from app.services.telemetry_service import TelemetryService
import threading

app, socketio = create_app()

def start_telemetry_service():
    telemetry_service = TelemetryService(socketio)
    telemetry_service.start()

if __name__ == '__main__':
    telemetry_thread = threading.Thread(target=start_telemetry_service, daemon=True)
    telemetry_thread.start()
    
    socketio.run(app, debug=True, host='0.0.0.0', port=5001)