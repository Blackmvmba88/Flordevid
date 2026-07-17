# Hardware Flordevid

Documentación de hardware, diseños de circuitos e instrucciones de ensamblaje para el dispositivo de monitoreo de señales ambientales Flordevid.

## Contenidos

- [circuit_designs.md](circuit_designs.md) - Esquemas de circuitos completos y especificaciones de componentes
- Lista de Materiales (BOM)
- Instrucciones de ensamblaje
- Procedimientos de prueba

## Descripción General del Hardware

El dispositivo Flordevid está construido alrededor de un microcontrolador ESP32 con circuitos front-end analógicos personalizados para acondicionamiento de señal.

### Componentes Clave

1. **ESP32-DevKitC**: Unidad de procesamiento principal
   - Conectividad WiFi/Bluetooth
   - Procesador de doble núcleo
   - Entradas ADC de 12 bits
   - Interfaz de programación USB

2. **Circuito de Sensor de Audio**
   - Micrófono electret o MEMS
   - Etapa de amplificación (op-amp LM358)
   - Ganancia: ~20 dB
   - Ancho de banda: 20 Hz - 20 kHz

3. **Circuito de Sensor EMF**
   - Sensor de bobina personalizado (500-1000 vueltas)
   - Amplificación de dos etapas
   - Alta impedancia de entrada
   - Ganancia: ~20 dB

4. **Fuente de Alimentación**
   - Entrada 5V (USB o batería)
   - Regulación 3.3V (AMS1117)
   - Capacidad de corriente: 500mA+

## Inicio Rápido

### Opción 1: Prototipo en Protoboard

1. Reunir componentes (ver BOM en circuit_designs.md)
2. Seguir diseño de protoboard
3. Conectar pines ESP32:
   - GPIO34 → Salida sensor de audio
   - GPIO35 → Salida sensor EMF
   - 3.3V → Riel de alimentación
   - GND → Riel de tierra
4. Subir firmware desde carpeta `/firmware`
5. Probar con monitor serial

### Opción 2: Diseño PCB

1. Usar esquemas proporcionados para diseñar PCB
2. Exportar archivos Gerber
3. Pedir a fabricante de PCB
4. Ensamblar componentes
5. Probar y programar

## Asignación de Pines

| Pin ESP32 | Función | Conexión |
|-----------|----------|------------|
| GPIO34 | ADC1_CH6 | Salida sensor de audio |
| GPIO35 | ADC1_CH7 | Salida sensor EMF |
| 3.3V | Alimentación | VCC sensor, alimentación op-amp |
| GND | Tierra | Tierra común |
| GPIO2 | LED | LED incorporado (indicador opcional) |

## Especificaciones de Sensores

### Sensor de Audio
- **Tipo**: Electret o MEMS
- **Sensibilidad**: -38 a -44 dB
- **Rango de frecuencia**: 20 Hz - 20 kHz
- **Voltaje de alimentación**: 2.0 - 3.6V
- **Salida**: Voltaje analógico (0-3.3V)

### Sensor EMF
- **Tipo**: Bobina inductiva
- **Inductancia**: ~50-100 mH
- **Rango de frecuencia**: 50 Hz - 10 kHz
- **Sensibilidad**: Detecta campos electromagnéticos cercanos
- **Salida**: Voltaje analógico (0-3.3V)

## Guía de Ensamblaje

### Instrucciones Paso a Paso

1. **Preparar espacio de trabajo**
   - Área limpia y bien iluminada
   - Tapete antiestático (recomendado)
   - Soldador y suministros

2. **Construir fuente de alimentación**
   - Soldar circuito regulador de voltaje
   - Probar voltaje de salida (debe ser 3.3V)

3. **Construir circuito de audio**
   - Soldar circuito op-amp
   - Conectar micrófono
   - Probar con entrada de audio

4. **Construir circuito EMF**
   - Bobinar bobina (si es DIY)
   - Soldar amplificador de dos etapas
   - Probar con imán o teléfono

5. **Conectar a ESP32**
   - Cablear salida de audio a GPIO34
   - Cablear salida EMF a GPIO35
   - Conectar alimentación y tierra

6. **Ensamblaje final**
   - Asegurar componentes
   - Agregar caja (opcional)
   - Etiquetar conectores

## Pruebas

### Prueba Inicial de Encendido
```bash
# Verificar niveles de voltaje
Riel 3.3V: 3.2-3.4V ✓
Riel 5V: 4.8-5.2V ✓
Consumo de corriente: 80-250mA ✓
```

### Prueba de Audio
```bash
# Subir firmware de prueba
# Hablar cerca del micrófono
# Observar salida serial para cambios de voltaje
Esperado: 0.5-2.5V variando con sonido
```

### Prueba EMF
```bash
# Subir firmware de prueba
# Mover teléfono cerca del sensor EMF
# Observar salida serial para cambios de voltaje
Esperado: 0.3-2.0V variando con fuente EMF
```

## Solución de Problemas

### Problemas Comunes

**Sin alimentación**
- Verificar conexión USB
- Verificar regulador de voltaje
- Medir salida 3.3V

**Sin lecturas de audio**
- Verificar alimentación del micrófono
- Verificar conexión GPIO34
- Probar salida del op-amp

**Sin lecturas EMF**
- Verificar conexiones de bobina
- Verificar conexión GPIO35
- Probar con imán fuerte

**Lecturas erráticas**
- Agregar condensadores de desacoplamiento
- Mejorar conexiones de tierra
- Verificar cables sueltos

## Diseño de Caja

### Características Recomendadas de Caja

- Agujeros de ventilación
- Abertura de micrófono (puerto acústico)
- Posicionamiento del sensor EMF (externo o ventana)
- Puerto de acceso USB
- Indicadores LED visibles
- Puntos de montaje

### Caja Imprimible en 3D (Opcional)

Consideraciones de diseño:
- Dimensiones internas: 100mm x 80mm x 40mm
- Espesor de pared: 2-3mm
- Soportes de montaje para PCB
- Clips de gestión de cables

## Modificaciones y Extensiones

### Agregar Pantalla
- Conectar pantalla OLED I2C a ESP32
- Mostrar valores de sensores en tiempo real
- Mostrar alertas de anomalías

### Agregar Más Sensores
- Sensor de temperatura (DHT22, BME280)
- Sensor de vibración (SW-420)
- Sensor de luz (LDR, BH1750)

### Mejorar Sensibilidad
- Usar op-amps de precisión (OPA2134)
- Agregar amplificadores de ganancia programable
- Implementar filtrado de hardware

## Mantenimiento

### Verificaciones Regulares
- Limpiar abertura del micrófono
- Verificar voltaje de batería (si funciona con batería)
- Verificar conectividad WiFi
- Actualizar firmware según sea necesario

### Calibración
- Registrar valores de línea base en entorno silencioso
- Ajustar umbrales en firmware
- Probar con fuentes EMF conocidas

## Notas de Seguridad

- Todos los componentes operan a voltajes seguros (< 5V)
- Evitar cortocircuitos
- Usar polaridad adecuada al conectar alimentación
- Manejar ESP32 con precauciones antiestáticas
- No exponer a agua o temperaturas extremas

## Recursos

### Hojas de Datos
- ESP32: https://www.espressif.com/en/products/socs/esp32
- LM358: Texas Instruments
- AMS1117: Advanced Monolithic Systems

### Herramientas
- Soldador
- Multímetro
- Osciloscopio (opcional, para depuración)
- Pelacables
- Cortadores al ras

### Proveedores
- Placas ESP32: AliExpress, Amazon, Adafruit
- Componentes electrónicos: Digi-Key, Mouser, LCSC
- Fabricación PCB: JLCPCB, PCBWay, OSH Park

## Contribuir

¡Las mejoras a los diseños de hardware son bienvenidas! Por favor envía:
- Mejoras de circuitos
- Diseños de PCB
- Diseños de cajas imprimibles en 3D
- Sugerencias de componentes alternativos

## Licencia

Licencia MIT - Los diseños de hardware son de código abierto
