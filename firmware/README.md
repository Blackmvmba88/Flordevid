# Firmware Flordevid

Firmware ESP32 para adquisición de datos multi-sensor compatible con detección de audio y EMF (campo electromagnético).

## Características

- **Captura de Audio**: Tasa de muestreo de 8kHz con cálculo de niveles pico y RMS
- **Detección EMF**: Monitoreo continuo de campo electromagnético
- **Conectividad WiFi**: Transmisión de datos en tiempo real por WiFi
- **API HTTP**: Endpoints RESTful para acceso a datos de sensores
- **Salida Serial**: Salida de datos en formato JSON para conexión directa

## Conexiones de Hardware

### Sensor de Audio
- **Pin**: GPIO34 (ADC1_CH6)
- **Sensor**: Módulo de micrófono MAX4466 o INMP441
- **Conexión**: Salida analógica a GPIO34

### Sensor EMF
- **Pin**: GPIO35 (ADC1_CH7)
- **Sensor**: Bobina personalizada con amplificador o AD8232
- **Conexión**: Salida analógica a GPIO35

### Alimentación
- **VCC**: 5V vía USB o 3.3V regulado
- **GND**: Tierra común para todos los componentes

## Compilación y Flasheo

### Usando PlatformIO (Recomendado)

1. Instalar PlatformIO:
```bash
pip install platformio
```

2. Compilar el firmware:
```bash
cd firmware
pio run
```

3. Subir a ESP32:
```bash
pio run --target upload
```

4. Monitorear salida serial:
```bash
pio device monitor
```

### Usando Arduino IDE

1. Instalar soporte para placa ESP32
2. Abrir `src/main.cpp` en Arduino IDE
3. Seleccionar placa: "ESP32 Dev Module"
4. Seleccionar puerto COM correcto
5. Subir

## Configuración

Editar `src/main.cpp` para configurar:

```cpp
// Credenciales WiFi
const char* ssid = "TU_SSID_WIFI";
const char* password = "TU_CONTRASEÑA_WIFI";

// Parámetros de muestreo
const int BUFFER_SIZE = 512;
const unsigned long SENSOR_INTERVAL = 100; // ms
```

## Endpoints API

Una vez conectado a WiFi, acceder a:

- `http://<IP_ESP32>/` - Página de inicio
- `http://<IP_ESP32>/status` - Estado del sistema
- `http://<IP_ESP32>/data` - Datos actuales de sensores

## Protocolo Serial

Los datos se envían en formato JSON a 115200 baudios:

```json
{
  "timestamp": 12345,
  "audio_peak": 0.45,
  "audio_rms": 0.23,
  "emf_avg": 1.2,
  "emf_peak": 2.1
}
```

## Solución de Problemas

### Sin conexión WiFi
- Verificar SSID y contraseña
- Verificar intensidad de señal
- El dispositivo continuará en modo independiente

### Sin lecturas de sensores
- Verificar conexiones de pines GPIO
- Verificar fuente de alimentación del sensor
- Verificar monitor serial para mensajes de inicialización

### Errores de compilación
- Asegurarse de que todas las dependencias estén instaladas
- Actualizar plataforma PlatformIO: `pio platform update`

## Dependencias

- Framework Arduino ESP32
- ArduinoJson (^6.21.0)
- arduinoFFT (^1.6.0) - Para análisis FFT futuro

## Licencia

Licencia MIT - Ver archivo LICENSE en el directorio raíz
