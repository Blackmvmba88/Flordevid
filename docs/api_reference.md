# API Reference

Complete API documentation for the Flordevid dashboard and data interfaces.

## Base URL

```
http://localhost:8000
```

Change to your deployment URL in production.

## Authentication

Currently, no authentication is required. For production, implement:
- API keys
- OAuth2
- JWT tokens

## REST API Endpoints

### System Status

#### GET `/api/status`

Get current system status and statistics.

**Response:**
```json
{
  "status": "running",
  "uptime": 3600.5,
  "connected_clients": 2,
  "total_readings": 36000
}
```

**Fields:**
- `status` (string): System status ("running", "stopped", "error")
- `uptime` (float): Seconds since system started
- `connected_clients` (int): Number of active WebSocket connections
- `total_readings` (int): Total number of sensor readings processed

**Status Codes:**
- `200 OK`: Success

**Example:**
```bash
curl http://localhost:8000/api/status
```

---

### Sensor Data

#### GET `/api/sensors/data`

Get the most recent sensor reading.

**Response:**
```json
{
  "timestamp": 1698765432.123,
  "audio_peak": 0.125,
  "audio_rms": 0.089,
  "emf_avg": 0.543,
  "emf_peak": 0.789
}
```

**Fields:**
- `timestamp` (float): Unix timestamp of reading
- `audio_peak` (float): Audio peak level in volts
- `audio_rms` (float): Audio RMS level in volts
- `emf_avg` (float): EMF average level in volts
- `emf_peak` (float): EMF peak level in volts

**Status Codes:**
- `200 OK`: Success
- `503 Service Unavailable`: No sensor connected

**Example:**
```bash
curl http://localhost:8000/api/sensors/data
```

---

### Anomaly History

#### GET `/api/anomalies`

Get recent anomaly detections (last 20).

**Query Parameters:**
- `limit` (int, optional): Maximum number of results (default: 20)

**Response:**
```json
{
  "anomalies": [
    {
      "timestamp": 1698765432.123,
      "confidence": 0.873,
      "anomaly_class": "spike",
      "audio_peak": 1.523,
      "emf_avg": 2.145
    },
    {
      "timestamp": 1698765430.456,
      "confidence": 0.921,
      "anomaly_class": "sustained",
      "audio_peak": 1.234,
      "emf_avg": 2.567
    }
  ]
}
```

**Anomaly Classes:**
- `normal`: No anomaly detected
- `spike`: Sudden brief increase in signal
- `sustained`: Prolonged elevated signal level
- `oscillating`: Rhythmic fluctuation pattern

**Status Codes:**
- `200 OK`: Success

**Example:**
```bash
curl http://localhost:8000/api/anomalies?limit=10
```

---

### Trigger Analysis

#### POST `/api/analyze`

Manually trigger an analysis cycle.

**Request Body:**
```json
{
  "source": "manual",
  "options": {
    "sensitivity": "high"
  }
}
```

**Response:**
```json
{
  "status": "Analysis triggered",
  "timestamp": 1698765432.123,
  "analysis_id": "abc123"
}
```

**Status Codes:**
- `200 OK`: Analysis started
- `503 Service Unavailable`: System busy

**Example:**
```bash
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"source":"manual"}'
```

---

## WebSocket API

### Real-Time Data Stream

#### WS `/ws/stream`

WebSocket endpoint for real-time bidirectional communication.

**Connection:**
```javascript
const ws = new WebSocket('ws://localhost:8000/ws/stream');

ws.onopen = () => {
    console.log('Connected');
};

ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    console.log('Received:', data);
};

ws.onerror = (error) => {
    console.error('WebSocket error:', error);
};

ws.onclose = () => {
    console.log('Disconnected');
};
```

### Message Types

#### 1. Sensor Reading

Sent periodically (every 1 second by default) with current sensor data.

```json
{
  "type": "sensor_reading",
  "data": {
    "timestamp": 1698765432.123,
    "audio_peak": 0.125,
    "audio_rms": 0.089,
    "emf_avg": 0.543,
    "emf_peak": 0.789
  }
}
```

#### 2. Anomaly Alert

Sent when an anomaly is detected.

```json
{
  "type": "anomaly_alert",
  "data": {
    "timestamp": 1698765432.123,
    "confidence": 0.873,
    "anomaly_class": "spike",
    "audio_peak": 1.523,
    "emf_avg": 2.145
  }
}
```

#### 3. Status Update

Periodic system status updates.

```json
{
  "type": "status",
  "data": {
    "status": "running",
    "uptime": 3600.5,
    "connected_clients": 2,
    "total_readings": 36000
  }
}
```

#### 4. Error Message

Sent when an error occurs.

```json
{
  "type": "error",
  "data": {
    "code": "SENSOR_DISCONNECT",
    "message": "Sensor connection lost",
    "timestamp": 1698765432.123
  }
}
```

### Client Commands

Send commands to the server via WebSocket:

#### Subscribe to Specific Events

```json
{
  "command": "subscribe",
  "events": ["sensor_reading", "anomaly_alert"]
}
```

#### Change Update Rate

```json
{
  "command": "set_rate",
  "interval": 500
}
```

**Interval in milliseconds** (min: 100ms, max: 10000ms)

---

## Serial Protocol

The ESP32 outputs JSON data via serial at 115200 baud.

### Output Format

```json
{
  "timestamp": 12345,
  "audio_peak": 0.125,
  "audio_rms": 0.089,
  "emf_avg": 0.543,
  "emf_peak": 0.789
}
```

**Reading Serial Data (Python):**

```python
import serial
import json

ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)

while True:
    line = ser.readline().decode('utf-8').strip()
    try:
        data = json.loads(line)
        print(f"Audio: {data['audio_peak']}, EMF: {data['emf_avg']}")
    except json.JSONDecodeError:
        pass  # Skip non-JSON lines
```

---

## Data Types

### SensorReading

```typescript
interface SensorReading {
  timestamp: number;      // Unix timestamp (seconds)
  audio_peak: number;     // Voltage (0-3.3V)
  audio_rms: number;      // Voltage (0-3.3V)
  emf_avg: number;        // Voltage (0-3.3V)
  emf_peak: number;       // Voltage (0-3.3V)
}
```

### AnomalyAlert

```typescript
interface AnomalyAlert {
  timestamp: number;           // Unix timestamp (seconds)
  confidence: number;          // Confidence score (0-1)
  anomaly_class: string;       // "normal" | "spike" | "sustained" | "oscillating"
  audio_peak: number;          // Voltage at detection
  emf_avg: number;             // Voltage at detection
}
```

### SystemStatus

```typescript
interface SystemStatus {
  status: string;              // "running" | "stopped" | "error"
  uptime: number;              // Seconds since start
  connected_clients: number;   // Active WebSocket connections
  total_readings: number;      // Total readings processed
}
```

---

## Rate Limits

To prevent abuse, consider implementing:

- **REST API**: 100 requests/minute per IP
- **WebSocket**: 1 connection per client
- **Data rate**: Updates every 100ms minimum

## Error Codes

| Code | Description | HTTP Status |
|------|-------------|-------------|
| `SENSOR_DISCONNECT` | Sensor connection lost | 503 |
| `INVALID_REQUEST` | Malformed request | 400 |
| `NOT_FOUND` | Endpoint not found | 404 |
| `RATE_LIMIT` | Too many requests | 429 |
| `INTERNAL_ERROR` | Server error | 500 |

## CORS Configuration

The API allows cross-origin requests from all origins by default. For production:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
```

## Integration Examples

### Python

```python
import requests
import websocket
import json

# REST API
response = requests.get('http://localhost:8000/api/status')
print(response.json())

# WebSocket
def on_message(ws, message):
    data = json.loads(message)
    print(f"Type: {data['type']}, Data: {data['data']}")

ws = websocket.WebSocketApp(
    'ws://localhost:8000/ws/stream',
    on_message=on_message
)
ws.run_forever()
```

### JavaScript/Node.js

```javascript
// REST API
fetch('http://localhost:8000/api/status')
  .then(res => res.json())
  .then(data => console.log(data));

// WebSocket
const ws = new WebSocket('ws://localhost:8000/ws/stream');

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log(`Type: ${data.type}`, data.data);
};
```

### cURL

```bash
# GET request
curl http://localhost:8000/api/status

# POST request
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"source":"manual"}'

# WebSocket (using websocat)
websocat ws://localhost:8000/ws/stream
```

## Security Recommendations

For production deployment:

1. **Use HTTPS/WSS**: Encrypt all communications
2. **Authentication**: Implement API keys or OAuth2
3. **Rate Limiting**: Prevent abuse
4. **Input Validation**: Sanitize all inputs
5. **CORS**: Restrict allowed origins
6. **Logging**: Log all API access
7. **Monitoring**: Track unusual activity

## Support

For API issues or questions:
- Check this documentation
- Review example code
- Open GitHub issue
- Contact support

## Changelog

### v1.0.0 (Current)
- Initial API release
- REST endpoints for status, data, and anomalies
- WebSocket streaming
- Serial protocol support

---

## License

MIT License - See LICENSE file in root directory
