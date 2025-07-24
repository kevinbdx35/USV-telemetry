import cv2
import base64
import threading
import time
from typing import Optional, Callable
import numpy as np

class CameraService:
    def __init__(self, camera_index: int = 0):
        self.camera_index = camera_index
        self.cap: Optional[cv2.VideoCapture] = None
        self.is_streaming = False
        self.frame_callback: Optional[Callable] = None
        self.thread: Optional[threading.Thread] = None
        self.fps = 15
        self.frame_delay = 1.0 / self.fps
        
    def start_stream(self, callback: Callable):
        if self.is_streaming:
            return False
            
        self.frame_callback = callback
        self.cap = cv2.VideoCapture(self.camera_index)
        
        if not self.cap.isOpened():
            self._simulate_camera_feed()
            return True
            
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.cap.set(cv2.CAP_PROP_FPS, self.fps)
        
        self.is_streaming = True
        self.thread = threading.Thread(target=self._capture_loop, daemon=True)
        self.thread.start()
        
        return True
    
    def stop_stream(self):
        self.is_streaming = False
        
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=2)
            
        if self.cap:
            self.cap.release()
            self.cap = None
            
        self.frame_callback = None
    
    def _capture_loop(self):
        while self.is_streaming and self.cap:
            ret, frame = self.cap.read()
            
            if not ret:
                break
                
            try:
                encoded_frame = self._encode_frame(frame)
                if self.frame_callback and encoded_frame:
                    self.frame_callback(encoded_frame)
                    
            except Exception as e:
                print(f"Camera capture error: {e}")
                break
                
            time.sleep(self.frame_delay)
    
    def _simulate_camera_feed(self):
        self.is_streaming = True
        self.thread = threading.Thread(target=self._simulate_loop, daemon=True)
        self.thread.start()
    
    def _simulate_loop(self):
        frame_count = 0
        
        while self.is_streaming:
            try:
                frame = self._generate_sample_frame(frame_count)
                encoded_frame = self._encode_frame(frame)
                
                if self.frame_callback and encoded_frame:
                    self.frame_callback(encoded_frame)
                    
                frame_count += 1
                time.sleep(self.frame_delay)
                
            except Exception as e:
                print(f"Simulated camera error: {e}")
                break
    
    def _generate_sample_frame(self, frame_count: int) -> np.ndarray:
        height, width = 480, 640
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        
        frame[:, :] = (30, 50, 70)
        
        center_x, center_y = width // 2, height // 2
        wave_offset = int(20 * np.sin(frame_count * 0.1))
        
        cv2.rectangle(frame, 
                     (center_x - 100 + wave_offset, center_y - 50), 
                     (center_x + 100 + wave_offset, center_y + 50), 
                     (0, 150, 255), -1)
        
        cv2.putText(frame, f"USV Camera Simulation", 
                   (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        
        cv2.putText(frame, f"Frame: {frame_count}", 
                   (20, height - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)
        
        timestamp = time.strftime("%H:%M:%S")
        cv2.putText(frame, timestamp, 
                   (width - 100, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)
        
        return frame
    
    def _encode_frame(self, frame: np.ndarray) -> Optional[str]:
        try:
            _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
            encoded = base64.b64encode(buffer).decode('utf-8')
            return encoded
        except Exception as e:
            print(f"Frame encoding error: {e}")
            return None
    
    def is_active(self) -> bool:
        return self.is_streaming