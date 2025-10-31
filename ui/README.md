# Flordevid Dashboard

FastAPI-based web dashboard for real-time monitoring and visualization of environmental sensor data.

## Features

- **Real-time Monitoring**: Live sensor data updates via WebSocket
- **Anomaly Alerts**: Visual alerts when anomalies are detected
- **System Status**: Monitor uptime, connection count, and readings
- **REST API**: Programmatic access to sensor data and system status
- **Responsive Design**: Modern, gradient-themed UI

## Installation

1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Dashboard

### Development Mode

```bash
uvicorn main:app --reload
```

### Production Mode

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

Access the dashboard at: `http://localhost:8000`

## API Endpoints

### REST API

#### GET `/api/status`
Get system status information

**Response:**
```json
{
  "status": "running",
  "uptime": 123.45,
  "connected_clients": 2,
  "total_readings": 1234
}
```

#### GET `/api/sensors/data`
Get latest sensor readings

**Response:**
```json
{
  "timestamp": 1234567890.123,
  "audio_peak": 0.125,
  "audio_rms": 0.089,
  "emf_avg": 0.543,
  "emf_peak": 0.789
}
```

#### GET `/api/anomalies`
Get recent anomaly history

**Response:**
```json
{
  "anomalies": [
    {
      "timestamp": 1234567890.123,
      "confidence": 0.87,
      "anomaly_class": "spike",
      "audio_peak": 1.523,
      "emf_avg": 2.145
    }
  ]
}
```

#### POST `/api/analyze`
Trigger manual analysis

**Response:**
```json
{
  "status": "Analysis triggered",
  "timestamp": 1234567890.123
}
```

### WebSocket API

#### WS `/ws/stream`
Real-time data streaming endpoint

**Message Types:**

1. **Sensor Reading**
```json
{
  "type": "sensor_reading",
  "data": {
    "timestamp": 1234567890.123,
    "audio_peak": 0.125,
    "audio_rms": 0.089,
    "emf_avg": 0.543,
    "emf_peak": 0.789
  }
}
```

2. **Anomaly Alert**
```json
{
  "type": "anomaly_alert",
  "data": {
    "timestamp": 1234567890.123,
    "confidence": 0.87,
    "anomaly_class": "spike",
    "audio_peak": 1.523,
    "emf_avg": 2.145
  }
}
```

3. **Status Update**
```json
{
  "type": "status",
  "data": {
    "status": "running",
    "uptime": 123.45,
    "connected_clients": 2,
    "total_readings": 1234
  }
}
```

## Integration with AI Core

To integrate with the AI Core module:

```python
import sys
sys.path.append('../ai_core')

from main import FlordovidAICore

# Initialize AI Core
ai_core = FlordovidAICore(serial_port='/dev/ttyUSB0')

# Process data and send to dashboard
async def process_and_broadcast():
    sensor_data = ai_core.read_sensor_data()
    result = ai_core.process_data(sensor_data)
    
    # Update system state
    system_state['latest_reading'] = sensor_data
    system_state['total_readings'] += 1
    
    # Broadcast to connected clients
    await manager.broadcast({
        'type': 'sensor_reading',
        'data': sensor_data
    })
    
    if result['anomaly']['is_anomaly']:
        await manager.broadcast({
            'type': 'anomaly_alert',
            'data': result['anomaly']
        })
```

## Dashboard Features

### Real-time Display

- **System Status**: Online status, uptime, total readings, connected clients
- **Audio Sensor**: Peak and RMS levels in volts
- **EMF Sensor**: Average and peak levels in volts
- **Anomaly Alerts**: Recent anomalies with confidence scores and timestamps

### Visual Design

- Gradient purple background
- Glass-morphism cards with backdrop blur
- Color-coded status indicators:
  - Green: Normal/Online
  - Yellow: Warning
  - Red: Alert/Anomaly

## Testing

### Using curl

```bash
# Get status
curl http://localhost:8000/api/status

# Get sensor data
curl http://localhost:8000/api/sensors/data

# Trigger analysis
curl -X POST http://localhost:8000/api/analyze
```

### Using WebSocket client

```javascript
const ws = new WebSocket('ws://localhost:8000/ws/stream');

ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    console.log('Received:', data);
};
```

## Deployment

### Using Docker

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Using systemd

Create `/etc/systemd/system/flordevid-dashboard.service`:

```ini
[Unit]
Description=Flordevid Dashboard
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/flordevid/ui
Environment="PATH=/opt/flordevid/ui/venv/bin"
ExecStart=/opt/flordevid/ui/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000

[Install]
WantedBy=multi-user.target
```

## Customization

### Changing Update Intervals

Edit `main.py`:

```python
# Sensor data update interval
await asyncio.sleep(1)  # Change to desired interval

# Status update interval (in JavaScript)
setInterval(() => {
    fetch('/api/status')...
}, 5000);  // Change to desired interval in ms
```

### Styling

Modify the `<style>` section in the HTML template within `main.py` to customize colors, fonts, and layout.

## License

MIT License - See LICENSE file in root directory
