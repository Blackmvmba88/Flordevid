# Flordevid

Dispositivo mecatrónico modular para registrar, amplificar y analizar señales ambientales para detectar patrones anómalos. El sistema combina firmware basado en ESP32 para adquisición de datos multi-sensor, circuitos de amplificación analógica y reconocimiento de patrones impulsado por IA usando TensorFlow Lite.

## 🚀 Características

- **Adquisición de Datos Multi-Sensor**: Detección de audio y EMF (campo electromagnético) vía ESP32
- **Amplificación de Señal**: Circuitos analógicos personalizados para amplificación de señales débiles
- **Análisis Impulsado por IA**: Modelos TensorFlow Lite para clasificación de anomalías en tiempo real
- **Panel Web**: Interfaz basada en FastAPI para monitoreo y visualización
- **Diseño Modular**: Arquitectura organizada para fácil extensión y mantenimiento

## 📁 Estructura del Proyecto

```
Flordevid/
├── firmware/          # Firmware ESP32 para captura de datos de sensores
├── ai_core/           # Backend Python con TensorFlow Lite para clasificación
├── hardware/          # Esquemas de circuitos y documentación de hardware
├── docs/              # Documentación técnica y guías
├── ui/                # Panel FastAPI e interfaz web
├── README.md          # Este archivo
├── LICENSE            # Licencia MIT
└── .gitignore        # Reglas de ignore de Git
```

## 🔧 Requisitos de Hardware

- Placa de desarrollo ESP32 (ESP32-DevKitC o similar)
- Micrófono/sensor de audio (ej. MAX4466, INMP441)
- Sensor EMF (ej. AD8232, sensor de bobina personalizado)
- Amplificadores operacionales para acondicionamiento de señal
- Fuente de alimentación (5V/3.3V)
- Componentes adicionales (ver carpeta `hardware/`)

## 📦 Requisitos de Software

### Firmware (ESP32)
- PlatformIO o Arduino IDE
- Paquete de soporte para placa ESP32

### Núcleo IA (Python)
- Python 3.8+
- TensorFlow Lite
- NumPy, SciPy
- Ver `ai_core/requirements.txt`

### Panel (FastAPI)
- Python 3.8+
- FastAPI
- Uvicorn
- Ver `ui/requirements.txt`

## 🚀 Inicio Rápido

### 1. Flashear Firmware ESP32
```bash
cd firmware
# Usando PlatformIO
pio run --target upload
```

### 2. Configurar Núcleo IA
```bash
cd ai_core
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

### 3. Lanzar Panel
```bash
cd ui
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Accede al panel en `http://localhost:8000`

## 📖 Documentación

Documentación detallada disponible en la carpeta `docs/`:
- [Guía de Configuración de Hardware](docs/hardware_setup.md)
- [Guía de Firmware](docs/firmware_guide.md)
- [Entrenamiento de Modelo IA](docs/ai_training.md)
- [Documentación de API](docs/api_reference.md)

## 🤖 Modelo IA

El sistema usa TensorFlow Lite para inferencia eficiente en el borde:
- Clasificación de señales en tiempo real
- Detección de patrones anómalos
- Procesamiento de baja latencia
- Soporte para entrenamiento de modelos personalizados

## 🔌 Endpoints API

Endpoints FastAPI principales:
- `GET /api/status` - Estado del sistema
- `GET /api/sensors/data` - Últimas lecturas de sensores
- `POST /api/analyze` - Activar análisis
- `WebSocket /ws/stream` - Transmisión de datos en tiempo real

## 🛠️ Desarrollo

### Pruebas
```bash
# Probar núcleo IA
cd ai_core
pytest tests/

# Probar API
cd ui
pytest tests/
```

### Construir Modelos Personalizados
Ver `docs/ai_training.md` para instrucciones sobre el entrenamiento de modelos TensorFlow Lite personalizados.

## 📄 Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Por favor, no dudes en enviar un Pull Request.

## 📧 Contacto

Para preguntas o soporte, por favor abre un issue en GitHub.

---

**Nota**: Este dispositivo está diseñado para monitoreo de señales ambientales y detección de anomalías. Asegúrese de cumplir con las regulaciones locales con respecto a equipos de monitoreo electromagnético.
