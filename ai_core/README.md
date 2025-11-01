# Núcleo IA Flordevid

Backend Python con TensorFlow Lite para clasificación de señales ambientales en tiempo real y detección de anomalías.

## Características

- **Procesamiento en Tiempo Real**: Procesar flujos de datos de sensores desde ESP32
- **TensorFlow Lite**: Inferencia eficiente en el borde con modelos cuantizados
- **Extracción de Características**: Cálculo de características estadísticas y espectrales
- **Detección de Anomalías**: Clasificación multi-clase (normal, pico, sostenido, oscilante)
- **Análisis de Señales**: Cálculo SNR, detección de patrones, filtrado digital

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

## Uso

### Entrenar Modelo

Generar y entrenar un modelo TensorFlow Lite:

```bash
python train_model.py
```

Esto crea `models/anomaly_model.tflite` con un clasificador entrenado.

### Ejecutar Núcleo IA

Procesar datos desde ESP32 vía serial:

```bash
# Linux/Mac
python main.py --port /dev/ttyUSB0

# Windows
python main.py --port COM3

# Modo de prueba (sin conexión serial)
python main.py
```

Argumentos opcionales:
- `--port`: Puerto serial para conexión ESP32
- `--duration`: Duración de ejecución en segundos (por defecto: infinito)
- `--model`: Ruta al modelo TFLite (por defecto: models/anomaly_model.tflite)

### Salida de Ejemplo

```
Núcleo IA Flordevid iniciado
==================================================
Conectado a /dev/ttyUSB0
✓ Operación normal | Audio: 0.125V | EMF: 0.543V

⚠️  ANOMALÍA DETECTADA en 1234567890
   Confianza: 87.3%
   Clase: pico
   Audio Pico: 1.523V
   EMF Promedio: 0.621V
```

## Arquitectura

### Flujo de Datos

```
Sensores ESP32 → Serial/JSON → DataProcessor → Extracción de Características
                                                      ↓
                                            SignalAnalyzer
                                                      ↓
                                            AnomalyDetector (TFLite)
                                                      ↓
                                            Resultados/Alertas
```

### Módulos

- **main.py**: Punto de entrada y orquestación
- **data_processor.py**: Extracción de características y preprocesamiento
- **signal_analyzer.py**: Análisis de señales y detección de patrones
- **anomaly_detector.py**: Inferencia TensorFlow Lite
- **train_model.py**: Script de entrenamiento de modelo

## Ingeniería de Características

El sistema extrae 10 características por muestra:

1. **Instantáneas** (4 características):
   - Nivel pico de audio
   - Nivel RMS de audio
   - Nivel promedio EMF
   - Nivel pico EMF

2. **Temporales** (6 características, calculadas sobre las últimas 5 muestras):
   - Media, desviación estándar, máximo de audio
   - Media, desviación estándar, máximo de EMF

## Arquitectura del Modelo

Modelo por defecto (entrenado por `train_model.py`):

```
Capa de Entrada: 10 características
Dense(32) + ReLU + Dropout(0.2)
Dense(16) + ReLU
Dense(4) + Softmax
Salida: 4 clases [normal, pico, sostenido, oscilante]
```

Optimizado a TensorFlow Lite con cuantización para despliegue en el borde.

## Clases

- **Normal**: Señales ambientales de línea base
- **Pico**: Aumento súbito breve en niveles de señal
- **Sostenido**: Niveles de señal elevados prolongados
- **Oscilante**: Patrón de fluctuación rítmica

## Personalización

### Entrenar con Datos Reales

Recolectar datos etiquetados y modificar `train_model.py`:

```python
# Cargar tus datos
X_train = np.load('tus_características.npy')
y_train = np.load('tus_etiquetas.npy')

# Entrenar
detector = AnomalyDetector()
model, history = detector.train_model(X_train, y_train, epochs=100)
detector.convert_to_tflite(model, 'models/modelo_personalizado.tflite')
```

### Ajustar Umbrales

Editar `signal_analyzer.py`:

```python
self.baseline_audio = 0.1  # Nivel de audio de línea base
self.baseline_emf = 0.5    # Nivel EMF de línea base
self.threshold_multiplier = 3.0  # Umbral de anomalía
```

### Agregar Nuevas Características

Extender `data_processor.py`:

```python
def extract_features(self, sensor_data):
    # ... características existentes ...
    
    # Agregar característica personalizada
    caracteristica_personalizada = self.compute_custom_feature(sensor_data)
    features.append(caracteristica_personalizada)
    
    return np.array(features)
```

## Pruebas

Ejecutar pruebas (si están disponibles):

```bash
pytest tests/
```

## Rendimiento

- **Tiempo de inferencia**: < 5ms por muestra en CPU
- **Huella de memoria**: ~500KB (modelo TFLite)
- **Throughput**: 100+ muestras/segundo

## Solución de Problemas

### Modelo no encontrado
Ejecutar `python train_model.py` para generar el modelo.

### Problemas de conexión serial
- Verificar nombre del puerto (`ls /dev/tty*` en Linux)
- Asegurarse de que ESP32 esté conectado y reconocido
- Verificar velocidad en baudios (115200)

### Errores de importación
```bash
pip install --upgrade tensorflow numpy scipy
```

## Licencia

Licencia MIT - Ver archivo LICENSE en el directorio raíz
