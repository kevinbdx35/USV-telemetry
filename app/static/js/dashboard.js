class USVDashboard {
    constructor() {
        this.socket = io();
        this.map = null;
        this.usvMarker = null;
        this.pathPolyline = null;
        this.sensorChart = null;
        this.cameraStream = null;
        this.pathCoordinates = [];
        
        this.initializeMap();
        this.initializeChart();
        this.setupSocketListeners();
        this.setupCameraSystem();
    }

    initializeMap() {
        this.map = L.map('map').setView([48.3833, -4.4833], 12);
        
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© OpenStreetMap contributors'
        }).addTo(this.map);

        const usvIcon = L.divIcon({
            className: 'usv-marker',
            html: '<i class="fas fa-ship" style="color: #0d6efd; font-size: 20px;"></i>',
            iconSize: [30, 30],
            iconAnchor: [15, 15]
        });

        this.usvMarker = L.marker([48.3833, -4.4833], { icon: usvIcon }).addTo(this.map);
        this.pathPolyline = L.polyline([], { color: '#0d6efd', weight: 3 }).addTo(this.map);
    }

    initializeChart() {
        const ctx = document.getElementById('sensorChart').getContext('2d');
        this.sensorChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: [],
                datasets: [
                    {
                        label: 'Battery (%)',
                        data: [],
                        borderColor: '#198754',
                        backgroundColor: 'rgba(25, 135, 84, 0.1)',
                        tension: 0.4
                    },
                    {
                        label: 'Temperature (°C)',
                        data: [],
                        borderColor: '#ffc107',
                        backgroundColor: 'rgba(255, 193, 7, 0.1)',
                        tension: 0.4
                    },
                    {
                        label: 'Speed (m/s)',
                        data: [],
                        borderColor: '#0dcaf0',
                        backgroundColor: 'rgba(13, 202, 240, 0.1)',
                        tension: 0.4
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: {
                        display: false
                    },
                    y: {
                        beginAtZero: true
                    }
                },
                plugins: {
                    legend: {
                        position: 'top'
                    }
                }
            }
        });
    }

    setupSocketListeners() {
        this.socket.on('connect', () => {
            console.log('Connected to telemetry server');
            this.updateConnectionStatus(true);
        });

        this.socket.on('disconnect', () => {
            console.log('Disconnected from telemetry server');
            this.updateConnectionStatus(false);
        });

        this.socket.on('telemetry_update', (data) => {
            this.updateDashboard(data);
        });

        this.socket.on('position_update', (data) => {
            this.updatePosition(data);
        });

        this.socket.on('camera_frame', (data) => {
            this.updateCameraFeed(data);
        });
    }

    setupCameraSystem() {
        window.connectCamera = () => {
            this.socket.emit('request_camera_stream');
            document.getElementById('camera-status').innerHTML = `
                <i class="fas fa-spinner fa-spin fa-3x text-light mb-3"></i>
                <p class="text-light">Connecting to camera...</p>
            `;
        };

        window.disconnectCamera = () => {
            this.socket.emit('stop_camera_stream');
            const feed = document.getElementById('camera-feed');
            feed.style.display = 'none';
            document.getElementById('camera-status').style.display = 'block';
            document.getElementById('camera-status').innerHTML = `
                <i class="fas fa-camera fa-3x text-muted mb-3"></i>
                <p class="text-muted">Camera feed disconnected</p>
                <button class="btn btn-outline-primary btn-sm" onclick="connectCamera()">
                    <i class="fas fa-play me-1"></i>Connect Camera
                </button>
            `;
        };
    }

    updateDashboard(data) {
        document.getElementById('battery-level').textContent = `${data.sensors.battery_level.toFixed(1)}%`;
        document.getElementById('speed').textContent = `${data.status.speed.toFixed(1)} m/s`;
        document.getElementById('temperature').textContent = `${data.sensors.temperature.toFixed(1)}°C`;
        document.getElementById('heading').textContent = `${data.position.heading.toFixed(0)}°`;
        
        document.getElementById('mission-mode').textContent = data.status.mode;
        document.getElementById('mission-status').textContent = data.status.mission_status;
        document.getElementById('wind-speed').textContent = `${data.sensors.wind_speed.toFixed(1)} m/s`;
        document.getElementById('water-temp').textContent = `${data.sensors.water_temperature.toFixed(1)}°C`;
        
        if (data.status.target_latitude && data.status.target_longitude) {
            document.getElementById('target-position').textContent = 
                `${data.status.target_latitude.toFixed(6)}, ${data.status.target_longitude.toFixed(6)}`;
        }

        this.updateChart(data);
    }

    updatePosition(data) {
        const { lat, lng, heading } = data;
        
        this.usvMarker.setLatLng([lat, lng]);
        this.pathCoordinates.push([lat, lng]);
        
        if (this.pathCoordinates.length > 100) {
            this.pathCoordinates.shift();
        }
        
        this.pathPolyline.setLatLngs(this.pathCoordinates);
        
        this.usvMarker.setRotationAngle(heading);
    }

    updateChart(data) {
        const currentTime = new Date().toLocaleTimeString();
        
        if (this.sensorChart.data.labels.length >= 20) {
            this.sensorChart.data.labels.shift();
            this.sensorChart.data.datasets.forEach(dataset => dataset.data.shift());
        }
        
        this.sensorChart.data.labels.push(currentTime);
        this.sensorChart.data.datasets[0].data.push(data.sensors.battery_level);
        this.sensorChart.data.datasets[1].data.push(data.sensors.temperature);
        this.sensorChart.data.datasets[2].data.push(data.status.speed);
        
        this.sensorChart.update('none');
    }

    updateCameraFeed(frameData) {
        const feed = document.getElementById('camera-feed');
        const status = document.getElementById('camera-status');
        
        if (frameData && frameData.frame) {
            feed.src = `data:image/jpeg;base64,${frameData.frame}`;
            feed.style.display = 'block';
            status.style.display = 'none';
        }
    }

    updateConnectionStatus(connected) {
        const statusElement = document.querySelector('.navbar-text');
        if (connected) {
            statusElement.innerHTML = '<i class="fas fa-circle text-success me-1"></i>Connected';
        } else {
            statusElement.innerHTML = '<i class="fas fa-circle text-danger me-1"></i>Disconnected';
        }
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new USVDashboard();
});