# USV Telemetry System

A modern, real-time telemetry dashboard for Unmanned Surface Vehicles (USV) built with Flask and WebSocket technology.

## Features

### 🚢 Real-time Telemetry
- Live position tracking with interactive map
- Real-time sensor data monitoring
- Battery, temperature, speed, and heading indicators
- Mission status and control mode display

### 📱 Modern Dashboard
- Responsive design for mobile and desktop
- Clean, intuitive user interface
- Real-time charts and data visualization
- Live camera feed from USV

### 🎥 Camera System
- Live video streaming from USV camera
- Simulated camera feed for development
- Real-time frame transmission via WebSocket

### 🗺️ Interactive Map
- OpenStreetMap integration with Leaflet.js
- Real-time USV position tracking
- Path history visualization
- Custom USV marker with heading indicator

## Technology Stack

- **Backend**: Flask, Flask-SocketIO
- **Frontend**: Bootstrap 5, Chart.js, Leaflet.js
- **Real-time Communication**: WebSocket via Socket.IO
- **Camera Processing**: OpenCV, Base64 encoding
- **Styling**: Custom CSS with modern design principles

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd usv
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the application:
```bash
python run.py
```

2. Open your browser and navigate to:
```
http://localhost:5001
```

3. The dashboard will display:
   - Real-time USV telemetry data
   - Interactive map with position tracking
   - Live camera feed (simulated if no camera available)
   - Sensor readings and mission status

## API Endpoints

### REST API
- `GET /` - Main dashboard
- `GET /health` - Health check
- `GET /api/usv/current` - Current USV data
- `GET /api/usv/history` - Historical data
- `GET /api/usv/path` - Path coordinates
- `POST /telemetry/data` - Receive telemetry data
- `GET /telemetry/status` - Telemetry service status

### WebSocket Events
- `telemetry_update` - Real-time telemetry data
- `position_update` - Position and heading updates
- `camera_frame` - Live camera frames
- `request_camera_stream` - Start camera streaming
- `stop_camera_stream` - Stop camera streaming

## Project Structure

```
usv/
├── app/
│   ├── __init__.py              # Flask application factory
│   ├── controllers/             # Route handlers
│   │   ├── main_controller.py   # Main dashboard routes
│   │   ├── telemetry_controller.py # Telemetry endpoints
│   │   └── api_controller.py    # REST API endpoints
│   ├── models/                  # Data models
│   │   └── usv_data.py         # USV data structures
│   ├── services/                # Business logic
│   │   ├── telemetry_service.py # Telemetry processing
│   │   └── camera_service.py    # Camera handling
│   ├── static/                  # Static assets
│   │   ├── css/
│   │   ├── js/
│   │   └── images/
│   ├── templates/               # HTML templates
│   │   ├── base.html
│   │   └── dashboard.html
│   └── utils/                   # Utility functions
├── config/                      # Configuration files
├── logs/                        # Application logs
├── tests/                       # Test files
├── requirements.txt             # Python dependencies
├── .gitignore                  # Git ignore rules
└── run.py                      # Application entry point
```

## Configuration

The application uses environment variables for configuration:

- `FLASK_ENV` - Environment (development/production)
- `SECRET_KEY` - Flask secret key
- `CAMERA_INDEX` - Camera device index (default: 0)

## Development

### Architecture Principles

This project follows clean architecture principles:

- **KISS**: Simple, focused components
- **DRY**: Reusable code modules
- **SOLID**: Proper separation of concerns
- **Modular**: Independent, testable components
- **Responsive**: Mobile-first design approach

### Code Structure

- **Controllers**: Handle HTTP requests and responses
- **Services**: Business logic and data processing
- **Models**: Data structures and validation
- **Templates**: Presentation layer with Jinja2
- **Static Assets**: CSS, JavaScript, and images

## Testing

Run tests with:
```bash
python -m pytest tests/
```

## Contributing

1. Follow the existing code style
2. Write tests for new features
3. Update documentation
4. Ensure responsive design compatibility

## License

This project is licensed under the MIT License.

## Support

For issues and questions, please create an issue in the project repository.