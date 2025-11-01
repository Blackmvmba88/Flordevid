"""
Panel Flordevid - Backend FastAPI
Monitoreo y visualización en tiempo real
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import asyncio
import json
import time
from datetime import datetime
from pydantic import BaseModel

# Crear aplicación FastAPI
app = FastAPI(
    title="Panel Flordevid",
    description="Monitoreo de señales ambientales en tiempo real y detección de anomalías",
    version="1.0.0"
)

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data models
class SensorReading(BaseModel):
    timestamp: float
    audio_peak: float
    audio_rms: float
    emf_avg: float
    emf_peak: float

class SystemStatus(BaseModel):
    status: str
    uptime: float
    connected_clients: int
    total_readings: int

class AnomalyAlert(BaseModel):
    timestamp: float
    confidence: float
    anomaly_class: str
    audio_peak: float
    emf_avg: float

# Global state
system_state = {
    'status': 'running',
    'start_time': time.time(),
    'total_readings': 0,
    'latest_reading': None,
    'anomaly_history': [],
    'connected_clients': 0,
}

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        system_state['connected_clients'] = len(self.active_connections)
    
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        system_state['connected_clients'] = len(self.active_connections)
    
    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except (WebSocketDisconnect, Exception) as e:
                # Connection may have closed, will be cleaned up on next iteration
                pass

manager = ConnectionManager()

# Routes
@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve dashboard HTML"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Flordevid Dashboard</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: #fff;
                padding: 20px;
            }
            .container {
                max-width: 1400px;
                margin: 0 auto;
            }
            h1 {
                text-align: center;
                margin-bottom: 30px;
                font-size: 2.5em;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            }
            .grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 20px;
                margin-bottom: 20px;
            }
            .card {
                background: rgba(255,255,255,0.1);
                backdrop-filter: blur(10px);
                border-radius: 15px;
                padding: 25px;
                box-shadow: 0 8px 32px rgba(0,0,0,0.1);
                border: 1px solid rgba(255,255,255,0.2);
            }
            .card h2 {
                margin-bottom: 15px;
                font-size: 1.5em;
                border-bottom: 2px solid rgba(255,255,255,0.3);
                padding-bottom: 10px;
            }
            .metric {
                display: flex;
                justify-content: space-between;
                margin: 10px 0;
                font-size: 1.1em;
            }
            .metric-label {
                opacity: 0.9;
            }
            .metric-value {
                font-weight: bold;
                font-size: 1.3em;
            }
            .status-online {
                color: #4ade80;
            }
            .status-warning {
                color: #fbbf24;
            }
            .status-alert {
                color: #f87171;
            }
            .alert-item {
                background: rgba(248,113,113,0.2);
                padding: 10px;
                border-radius: 8px;
                margin: 8px 0;
                border-left: 4px solid #f87171;
            }
            .alert-time {
                font-size: 0.85em;
                opacity: 0.8;
            }
            #connection-status {
                text-align: center;
                padding: 10px;
                border-radius: 8px;
                margin-bottom: 20px;
                background: rgba(74,222,128,0.2);
                border: 1px solid #4ade80;
            }
            .full-width {
                grid-column: 1 / -1;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🔬 Flordevid Environmental Monitor</h1>
            
            <div id="connection-status">
                <span id="ws-status">Connecting...</span>
            </div>
            
            <div class="grid">
                <div class="card">
                    <h2>📊 System Status</h2>
                    <div class="metric">
                        <span class="metric-label">Status:</span>
                        <span class="metric-value status-online" id="system-status">Online</span>
                    </div>
                    <div class="metric">
                        <span class="metric-label">Uptime:</span>
                        <span class="metric-value" id="uptime">0s</span>
                    </div>
                    <div class="metric">
                        <span class="metric-label">Total Readings:</span>
                        <span class="metric-value" id="total-readings">0</span>
                    </div>
                    <div class="metric">
                        <span class="metric-label">Clients:</span>
                        <span class="metric-value" id="clients">0</span>
                    </div>
                </div>
                
                <div class="card">
                    <h2>🎤 Audio Sensor</h2>
                    <div class="metric">
                        <span class="metric-label">Peak Level:</span>
                        <span class="metric-value" id="audio-peak">0.00 V</span>
                    </div>
                    <div class="metric">
                        <span class="metric-label">RMS Level:</span>
                        <span class="metric-value" id="audio-rms">0.00 V</span>
                    </div>
                </div>
                
                <div class="card">
                    <h2>⚡ EMF Sensor</h2>
                    <div class="metric">
                        <span class="metric-label">Average:</span>
                        <span class="metric-value" id="emf-avg">0.00 V</span>
                    </div>
                    <div class="metric">
                        <span class="metric-label">Peak:</span>
                        <span class="metric-value" id="emf-peak">0.00 V</span>
                    </div>
                </div>
                
                <div class="card full-width">
                    <h2>⚠️ Anomaly Alerts</h2>
                    <div id="alerts">
                        <p style="opacity: 0.7; text-align: center;">No anomalies detected</p>
                    </div>
                </div>
            </div>
        </div>
        
        <script>
            const ws = new WebSocket(`ws://${window.location.host}/ws/stream`);
            
            ws.onopen = () => {
                document.getElementById('ws-status').textContent = '✓ Connected to sensor stream';
            };
            
            ws.onclose = () => {
                document.getElementById('ws-status').textContent = '✗ Disconnected';
                document.getElementById('connection-status').style.background = 'rgba(248,113,113,0.2)';
                document.getElementById('connection-status').style.borderColor = '#f87171';
            };
            
            ws.onmessage = (event) => {
                const data = JSON.parse(event.data);
                
                if (data.type === 'sensor_reading') {
                    updateSensorData(data.data);
                } else if (data.type === 'anomaly_alert') {
                    addAnomaly(data.data);
                } else if (data.type === 'status') {
                    updateStatus(data.data);
                }
            };
            
            function updateSensorData(data) {
                document.getElementById('audio-peak').textContent = data.audio_peak.toFixed(3) + ' V';
                document.getElementById('audio-rms').textContent = data.audio_rms.toFixed(3) + ' V';
                document.getElementById('emf-avg').textContent = data.emf_avg.toFixed(3) + ' V';
                document.getElementById('emf-peak').textContent = data.emf_peak.toFixed(3) + ' V';
            }
            
            function updateStatus(data) {
                document.getElementById('system-status').textContent = data.status;
                document.getElementById('uptime').textContent = formatUptime(data.uptime);
                document.getElementById('total-readings').textContent = data.total_readings;
                document.getElementById('clients').textContent = data.connected_clients;
            }
            
            function addAnomaly(data) {
                const alertsDiv = document.getElementById('alerts');
                const time = new Date(data.timestamp * 1000).toLocaleTimeString();
                
                if (alertsDiv.firstChild && alertsDiv.firstChild.tagName === 'P') {
                    alertsDiv.innerHTML = '';
                }
                
                const alertHtml = `
                    <div class="alert-item">
                        <div><strong>${data.anomaly_class.toUpperCase()}</strong> detected (${(data.confidence * 100).toFixed(1)}% confidence)</div>
                        <div>Audio: ${data.audio_peak.toFixed(3)}V | EMF: ${data.emf_avg.toFixed(3)}V</div>
                        <div class="alert-time">${time}</div>
                    </div>
                `;
                
                alertsDiv.insertAdjacentHTML('afterbegin', alertHtml);
                
                // Keep only last 5 alerts
                while (alertsDiv.children.length > 5) {
                    alertsDiv.removeChild(alertsDiv.lastChild);
                }
            }
            
            function formatUptime(seconds) {
                const hours = Math.floor(seconds / 3600);
                const minutes = Math.floor((seconds % 3600) / 60);
                const secs = Math.floor(seconds % 60);
                return `${hours}h ${minutes}m ${secs}s`;
            }
            
            // Request status update every 5 seconds
            setInterval(() => {
                fetch('/api/status')
                    .then(r => r.json())
                    .then(data => updateStatus(data));
            }, 5000);
        </script>
    </body>
    </html>
    """

@app.get("/api/status")
async def get_status():
    """Get system status"""
    return SystemStatus(
        status=system_state['status'],
        uptime=time.time() - system_state['start_time'],
        connected_clients=system_state['connected_clients'],
        total_readings=system_state['total_readings']
    )

@app.get("/api/sensors/data")
async def get_sensor_data():
    """Get latest sensor readings"""
    if system_state['latest_reading']:
        return system_state['latest_reading']
    return {
        'timestamp': time.time(),
        'audio_peak': 0.0,
        'audio_rms': 0.0,
        'emf_avg': 0.0,
        'emf_peak': 0.0
    }

@app.get("/api/anomalies")
async def get_anomalies():
    """Get anomaly history"""
    return {'anomalies': system_state['anomaly_history'][-20:]}

@app.post("/api/analyze")
async def trigger_analysis():
    """Trigger manual analysis"""
    return {'status': 'Analysis triggered', 'timestamp': time.time()}

@app.websocket("/ws/stream")
async def websocket_stream(websocket: WebSocket):
    """WebSocket endpoint for real-time data streaming"""
    await manager.connect(websocket)
    
    try:
        # Send initial status
        await websocket.send_json({
            'type': 'status',
            'data': {
                'status': system_state['status'],
                'uptime': time.time() - system_state['start_time'],
                'connected_clients': system_state['connected_clients'],
                'total_readings': system_state['total_readings']
            }
        })
        
        # Keep connection alive and wait for messages
        while True:
            # Wait for any messages from client
            try:
                data = await asyncio.wait_for(websocket.receive_text(), timeout=1.0)
            except asyncio.TimeoutError:
                # Send periodic updates
                continue
                
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# Background task to simulate sensor data
async def simulate_sensor_data():
    """Simulate sensor data for testing"""
    import random
    
    while True:
        await asyncio.sleep(1)
        
        # Generate simulated data
        reading = {
            'timestamp': time.time(),
            'audio_peak': random.uniform(0.05, 0.5),
            'audio_rms': random.uniform(0.03, 0.3),
            'emf_avg': random.uniform(0.3, 1.0),
            'emf_peak': random.uniform(0.5, 1.5),
        }
        
        # Occasionally generate anomaly
        if random.random() < 0.05:  # 5% chance
            reading['audio_peak'] = random.uniform(1.0, 2.0)
            reading['emf_avg'] = random.uniform(2.0, 3.0)
            
            anomaly = {
                'timestamp': reading['timestamp'],
                'confidence': random.uniform(0.7, 0.95),
                'anomaly_class': random.choice(['spike', 'sustained', 'oscillating']),
                'audio_peak': reading['audio_peak'],
                'emf_avg': reading['emf_avg'],
            }
            
            system_state['anomaly_history'].append(anomaly)
            
            # Broadcast anomaly
            await manager.broadcast({
                'type': 'anomaly_alert',
                'data': anomaly
            })
        
        system_state['latest_reading'] = reading
        system_state['total_readings'] += 1
        
        # Broadcast sensor reading
        await manager.broadcast({
            'type': 'sensor_reading',
            'data': reading
        })

@app.on_event("startup")
async def startup_event():
    """Start background tasks"""
    asyncio.create_task(simulate_sensor_data())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
