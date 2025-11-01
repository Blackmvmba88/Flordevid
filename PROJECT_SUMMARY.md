# Resumen del Proyecto Flordevid

## Descripción General
Dispositivo mecatrónico modular completo para monitoreo de señales ambientales y detección de anomalías.

## Componentes Implementados

### 1. Firmware (ESP32) ✓
- **Ubicación**: `/firmware/`
- **Características**:
  - Captura de audio vía GPIO34 (muestreo 8kHz)
  - Sensor EMF vía GPIO35
  - Conectividad WiFi con servidor web
  - Salida de datos JSON por serial (115200 baud)
  - Clases de sensores modulares (audio_capture.h, emf_sensor.h)
- **Sistema de Compilación**: PlatformIO
- **Documentación**: firmware/README.md

### 2. Núcleo IA (Python + TensorFlow Lite) ✓
- **Ubicación**: `/ai_core/`
- **Módulos**:
  - `main.py`: Punto de entrada y orquestación
  - `data_processor.py`: Extracción de características (10 características)
  - `signal_analyzer.py`: Análisis de señales y detección de patrones
  - `anomaly_detector.py`: Inferencia TFLite con respaldo basado en reglas
  - `train_model.py`: Script de entrenamiento de modelo
- **Clases**: Normal, Pico, Sostenido, Oscilante
- **Documentación**: ai_core/README.md

### 3. Documentación de Hardware ✓
- **Ubicación**: `/hardware/`
- **Contenidos**:
  - Esquemas de circuitos (amplificación audio y EMF)
  - Lista de Materiales (BOM)
  - Especificaciones de componentes
  - Instrucciones de ensamblaje
  - Guías de diseño PCB
- **Documentación**: hardware/README.md, circuit_designs.md

### 4. Panel UI (FastAPI) ✓
- **Ubicación**: `/ui/`
- **Características**:
  - Transmisión WebSocket en tiempo real
  - Endpoints REST API (estado, datos, anomalías)
  - Panel HTML embebido con diseño glass-morphism
  - Visualización de lecturas de sensores en vivo
  - Sistema de alertas de anomalías
- **Stack Tecnológico**: FastAPI, Uvicorn, WebSockets
- **Documentación**: ui/README.md

### 5. Documentación ✓
- **Ubicación**: `/docs/`
- **Guías**:
  - `hardware_setup.md`: Guía completa de ensamblaje
  - `firmware_guide.md`: Personalización de firmware
  - `ai_training.md`: Entrenamiento de modelo ML
  - `api_reference.md`: Documentación completa de API

## Estructura del Proyecto
```
Flordevid/
├── firmware/          # Código C++ ESP32
│   ├── src/
│   ├── include/
│   └── platformio.ini
├── ai_core/           # Backend ML Python
│   ├── main.py
│   ├── data_processor.py
│   ├── signal_analyzer.py
│   ├── anomaly_detector.py
│   ├── train_model.py
│   └── requirements.txt
├── hardware/          # Esquemas y BOM
│   ├── circuit_designs.md
│   └── README.md
├── docs/              # Documentación técnica
│   ├── hardware_setup.md
│   ├── firmware_guide.md
│   ├── ai_training.md
│   └── api_reference.md
├── ui/                # Panel FastAPI
│   ├── main.py
│   └── requirements.txt
├── README.md          # README principal del proyecto
├── LICENSE            # Licencia MIT
└── .gitignore        # Reglas de ignore de Git
```

## Inicio Rápido

### 1. Construir Hardware
```bash
# Ver hardware/circuit_designs.md para esquemas
# Ensamblar en protoboard o PCB
```

### 2. Flashear Firmware
```bash
cd firmware
pio run --target upload
```

### 3. Ejecutar Núcleo IA
```bash
cd ai_core
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py --port /dev/ttyUSB0
```

### 4. Iniciar Panel
```bash
cd ui
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
# Abrir http://localhost:8000
```

## Características

### Detección de Audio
- Resolución ADC de 12 bits
- Cálculo de niveles pico y RMS
- Tasa de muestreo ~8kHz
- Acondicionamiento de señal amplificada

### Detección EMF
- Sensor de bobina personalizado
- Buffer de alta impedancia
- Amplificación de dos etapas
- Rango DC a 10kHz

### Clasificación IA
- Detección de anomalías de 4 clases
- Inferencia TensorFlow Lite
- Respaldo basado en reglas
- Procesamiento en tiempo real

### Panel
- Actualizaciones WebSocket en tiempo real
- Acceso REST API
- Diseño responsivo
- Alertas de anomalías

## Stack Tecnológico

### Hardware
- ESP32-DevKitC (Doble núcleo, WiFi)
- Op-Amps LM358
- Regulador AMS1117-3.3
- Micrófono Electret/MEMS
- Bobina EMF personalizada

### Firmware
- C++ (framework Arduino)
- PlatformIO
- ArduinoJson
- Librerías WiFi y WebServer

### Backend
- Python 3.8+
- TensorFlow Lite
- NumPy, SciPy, Pandas
- PySerial

### Frontend
- FastAPI
- WebSockets
- HTML5/CSS3/JavaScript
- Diseño responsivo

## Estado de Desarrollo

✅ Estructura completa del proyecto
✅ Firmware ESP32 con sensores duales
✅ Núcleo IA Python con TFLite
✅ Panel FastAPI con WebSocket
✅ Esquemas de hardware y BOM
✅ Documentación completa
✅ Licencia MIT
✅ .gitignore configurado
✅ Todos los archivos Python verificados sintácticamente
✅ Panel probado y funcionando

## Próximos Pasos (Dirigidos por el Usuario)

1. **Construir Hardware**: Ensamblar circuito en protoboard
2. **Probar Firmware**: Subir a ESP32 y verificar sensores
3. **Recolectar Datos**: Reunir datos de entrenamiento para modelo ML
4. **Entrenar Modelo**: Ejecutar train_model.py con datos reales
5. **Desplegar**: Integrar todos los componentes
6. **Personalizar**: Extender con características adicionales

## Licencia
Licencia MIT - Ver archivo LICENSE

## Contribuidores
- BlackMamba (Blackmvmba88)
- GitHub Copilot

## Repositorio
https://github.com/Blackmvmba88/Flordevid
