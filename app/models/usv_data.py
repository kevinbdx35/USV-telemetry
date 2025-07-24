import time
import json
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict

@dataclass
class USVPosition:
    latitude: float
    longitude: float
    altitude: float
    heading: float
    timestamp: float

@dataclass
class USVSensors:
    battery_level: float
    temperature: float
    humidity: float
    wind_speed: float
    wind_direction: float
    water_temperature: float

@dataclass
class USVStatus:
    mode: str
    speed: float
    target_latitude: Optional[float] = None
    target_longitude: Optional[float] = None
    mission_status: str = "idle"

@dataclass
class USVData:
    position: USVPosition
    sensors: USVSensors
    status: USVStatus
    timestamp: float

class USVDataManager:
    def __init__(self):
        self._current_data: Optional[USVData] = None
        self._history: List[USVData] = []
        self._max_history = 1000
    
    def update_data(self, data: Dict) -> None:
        try:
            position = USVPosition(**data.get('position', {}))
            sensors = USVSensors(**data.get('sensors', {}))
            status = USVStatus(**data.get('status', {}))
            
            usv_data = USVData(
                position=position,
                sensors=sensors,
                status=status,
                timestamp=time.time()
            )
            
            self._current_data = usv_data
            self._history.append(usv_data)
            
            if len(self._history) > self._max_history:
                self._history.pop(0)
                
        except Exception as e:
            print(f"Error updating USV data: {e}")
    
    def get_current_data(self) -> Dict:
        if self._current_data:
            return asdict(self._current_data)
        return self._generate_sample_data()
    
    def get_history(self, limit: int = 100) -> List[Dict]:
        return [asdict(data) for data in self._history[-limit:]]
    
    def get_path_data(self) -> List[Dict]:
        return [
            {
                'lat': data.position.latitude,
                'lng': data.position.longitude,
                'timestamp': data.timestamp
            }
            for data in self._history
        ]
    
    def _generate_sample_data(self) -> Dict:
        import random
        
        base_lat = 48.3833
        base_lng = -4.4833
        
        return {
            'position': {
                'latitude': base_lat + random.uniform(-0.01, 0.01),
                'longitude': base_lng + random.uniform(-0.01, 0.01),
                'altitude': random.uniform(0, 2),
                'heading': random.uniform(0, 360),
                'timestamp': time.time()
            },
            'sensors': {
                'battery_level': random.uniform(20, 100),
                'temperature': random.uniform(15, 35),
                'humidity': random.uniform(40, 80),
                'wind_speed': random.uniform(0, 15),
                'wind_direction': random.uniform(0, 360),
                'water_temperature': random.uniform(18, 25)
            },
            'status': {
                'mode': random.choice(['manual', 'auto', 'mission']),
                'speed': random.uniform(0, 10),
                'target_latitude': base_lat + random.uniform(-0.002, 0.002),
                'target_longitude': base_lng + random.uniform(-0.002, 0.002),
                'mission_status': random.choice(['idle', 'active', 'returning'])
            },
            'timestamp': time.time()
        }