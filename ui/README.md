# Panel Flordevid

Panel web basado en FastAPI para monitoreo y visualización en tiempo real de datos de sensores ambientales.

## Características

- **Monitoreo en Tiempo Real**: Actualizaciones de datos de sensores en vivo vía WebSocket
- **Alertas de Anomalías**: Alertas visuales cuando se detectan anomalías
- **Estado del Sistema**: Monitorear tiempo de actividad, conteo de conexiones y lecturas
- **API REST**: Acceso programático a datos de sensores y estado del sistema
- **Diseño Responsivo**: Interfaz moderna con tema de gradiente

## Instalación

1. Crear entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

## Ejecutar el Panel

### Modo Desarrollo

```bash
uvicorn main:app --reload
```

### Modo Producción

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

Acceder al panel en: `http://localhost:8000`

## Endpoints API

### API REST

#### GET `/api/status`
Obtener información del estado del sistema

**Respuesta:**
```json
{
  "status": "running",
  "uptime": 123.45,
  "connected_clients": 2,
  "total_readings": 1234
}
```

#### GET `/api/sensors/data`
Obtener últimas lecturas de sensores

**Respuesta:**
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
Obtener historial reciente de anomalías

**Respuesta:**
```json
{
  "anomalies": [
    {
      "timestamp": 1234567890.123,
      "confidence": 0.87,
      "anomaly_class": "pico",
      "audio_peak": 1.523,
      "emf_avg": 2.145
    }
  ]
}
```

#### POST `/api/analyze`
Activar análisis manual

**Respuesta:**
```json
{
  "status": "Análisis activado",
  "timestamp": 1234567890.123
}
```

### API WebSocket

#### WS `/ws/stream`
Endpoint de transmisión de datos en tiempo real

**Tipos de Mensajes:**

1. **Lectura de Sensor**
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

2. **Alerta de Anomalía**
```json
{
  "type": "anomaly_alert",
  "data": {
    "timestamp": 1234567890.123,
    "confidence": 0.87,
    "anomaly_class": "pico",
    "audio_peak": 1.523,
    "emf_avg": 2.145
  }
}
```

3. **Actualización de Estado**
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

## Integración con Núcleo IA

Para integrar con el módulo Núcleo IA:

```python
import sys
sys.path.append('../ai_core')

from main import FlordovidAICore

# Inicializar Núcleo IA
ai_core = FlordovidAICore(serial_port='/dev/ttyUSB0')

# Procesar datos y enviar al panel
async def process_and_broadcast():
    sensor_data = ai_core.read_sensor_data()
    result = ai_core.process_data(sensor_data)
    
    # Actualizar estado del sistema
    system_state['latest_reading'] = sensor_data
    system_state['total_readings'] += 1
    
    # Transmitir a clientes conectados
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

## Características del Panel

### Visualización en Tiempo Real

- **Estado del Sistema**: Estado en línea, tiempo de actividad, lecturas totales, clientes conectados
- **Sensor de Audio**: Niveles pico y RMS en voltios
- **Sensor EMF**: Niveles promedio y pico en voltios
- **Alertas de Anomalías**: Anomalías recientes con puntajes de confianza y marcas de tiempo

### Diseño Visual

- Fondo de gradiente púrpura
- Tarjetas glass-morphism con desenfoque de fondo
- Indicadores de estado codificados por color:
  - Verde: Normal/En línea
  - Amarillo: Advertencia
  - Rojo: Alerta/Anomalía

## Pruebas

### Usando curl

```bash
# Obtener estado
curl http://localhost:8000/api/status

# Obtener datos de sensores
curl http://localhost:8000/api/sensors/data

# Activar análisis
curl -X POST http://localhost:8000/api/analyze
```

### Usando cliente WebSocket

```javascript
const ws = new WebSocket('ws://localhost:8000/ws/stream');

ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    console.log('Recibido:', data);
};
```

## Despliegue

### Usando Docker

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Usando systemd

Crear `/etc/systemd/system/flordevid-dashboard.service`:

```ini
[Unit]
Description=Panel Flordevid
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

## Personalización

### Cambiar Intervalos de Actualización

Editar `main.py`:

```python
# Intervalo de actualización de datos de sensores
await asyncio.sleep(1)  # Cambiar al intervalo deseado

# Intervalo de actualización de estado (en JavaScript)
setInterval(() => {
    fetch('/api/status')...
}, 5000);  // Cambiar al intervalo deseado en ms
```

### Estilos

Modificar la sección `<style>` en la plantilla HTML dentro de `main.py` para personalizar colores, fuentes y diseño.

## Licencia

Licencia MIT - Ver archivo LICENSE en el directorio raíz
