import time
import threading
from typing import Optional
from flask_socketio import SocketIO
from app.models.usv_data import USVDataManager
from app.services.camera_service import CameraService

class TelemetryService:
    def __init__(self, socketio: SocketIO):
        self.socketio = socketio
        self.data_manager = USVDataManager()
        self.camera_service = CameraService()
        self.running = False
        self.update_interval = 1.0
        
        self._setup_socket_handlers()
        
    def start(self):
        if not self.running:
            self.running = True
            self._run_telemetry_loop()
    
    def stop(self):
        self.running = False
    
    def _run_telemetry_loop(self):
        while self.running:
            try:
                current_data = self.data_manager.get_current_data()
                
                self.socketio.emit('telemetry_update', current_data)
                self.socketio.emit('position_update', {
                    'lat': current_data['position']['latitude'],
                    'lng': current_data['position']['longitude'],
                    'heading': current_data['position']['heading'],
                    'timestamp': current_data['timestamp']
                })
                
                time.sleep(self.update_interval)
                
            except Exception as e:
                print(f"Telemetry service error: {e}")
                time.sleep(5)
    
    def process_incoming_data(self, data: dict):
        try:
            self.data_manager.update_data(data)
            return True
        except Exception as e:
            print(f"Error processing incoming data: {e}")
            return False
    
    def _setup_socket_handlers(self):
        @self.socketio.on('request_camera_stream')
        def handle_camera_request():
            if not self.camera_service.is_active():
                success = self.camera_service.start_stream(self._camera_frame_callback)
                if success:
                    self.socketio.emit('camera_status', {'status': 'connected'})
                else:
                    self.socketio.emit('camera_status', {'status': 'error', 'message': 'Failed to start camera'})
        
        @self.socketio.on('stop_camera_stream')
        def handle_camera_stop():
            self.camera_service.stop_stream()
            self.socketio.emit('camera_status', {'status': 'disconnected'})
    
    def _camera_frame_callback(self, encoded_frame: str):
        try:
            self.socketio.emit('camera_frame', {'frame': encoded_frame})
        except Exception as e:
            print(f"Error sending camera frame: {e}")