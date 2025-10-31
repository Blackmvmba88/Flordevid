# Flordevid Hardware

Hardware documentation, circuit designs, and assembly instructions for the Flordevid environmental signal monitoring device.

## Contents

- [circuit_designs.md](circuit_designs.md) - Complete circuit schematics and component specifications
- Bill of Materials (BOM)
- Assembly instructions
- Testing procedures

## Hardware Overview

The Flordevid device is built around an ESP32 microcontroller with custom analog front-end circuits for signal conditioning.

### Key Components

1. **ESP32-DevKitC**: Main processing unit
   - WiFi/Bluetooth connectivity
   - Dual-core processor
   - 12-bit ADC inputs
   - USB programming interface

2. **Audio Sensor Circuit**
   - Electret or MEMS microphone
   - Amplification stage (LM358 op-amp)
   - Gain: ~20 dB
   - Bandwidth: 20 Hz - 20 kHz

3. **EMF Sensor Circuit**
   - Custom coil sensor (500-1000 turns)
   - Two-stage amplification
   - High input impedance
   - Gain: ~20 dB

4. **Power Supply**
   - 5V input (USB or battery)
   - 3.3V regulation (AMS1117)
   - Current capacity: 500mA+

## Quick Start

### Option 1: Breadboard Prototype

1. Gather components (see BOM in circuit_designs.md)
2. Follow breadboard layout
3. Connect ESP32 pins:
   - GPIO34 → Audio sensor output
   - GPIO35 → EMF sensor output
   - 3.3V → Power rail
   - GND → Ground rail
4. Upload firmware from `/firmware` folder
5. Test with serial monitor

### Option 2: PCB Design

1. Use provided schematics to design PCB
2. Export Gerber files
3. Order from PCB manufacturer
4. Assemble components
5. Test and program

## Pin Assignments

| ESP32 Pin | Function | Connection |
|-----------|----------|------------|
| GPIO34 | ADC1_CH6 | Audio sensor output |
| GPIO35 | ADC1_CH7 | EMF sensor output |
| 3.3V | Power | Sensor VCC, op-amp power |
| GND | Ground | Common ground |
| GPIO2 | LED | Built-in LED (optional indicator) |

## Sensor Specifications

### Audio Sensor
- **Type**: Electret or MEMS
- **Sensitivity**: -38 to -44 dB
- **Frequency range**: 20 Hz - 20 kHz
- **Supply voltage**: 2.0 - 3.6V
- **Output**: Analog voltage (0-3.3V)

### EMF Sensor
- **Type**: Inductive coil
- **Inductance**: ~50-100 mH
- **Frequency range**: 50 Hz - 10 kHz
- **Sensitivity**: Detects nearby electromagnetic fields
- **Output**: Analog voltage (0-3.3V)

## Assembly Guide

### Step-by-Step Instructions

1. **Prepare workspace**
   - Clear, well-lit area
   - Anti-static mat (recommended)
   - Soldering iron and supplies

2. **Build power supply**
   - Solder voltage regulator circuit
   - Test output voltage (should be 3.3V)

3. **Build audio circuit**
   - Solder op-amp circuit
   - Connect microphone
   - Test with audio input

4. **Build EMF circuit**
   - Wind coil (if DIY)
   - Solder two-stage amplifier
   - Test with magnet or phone

5. **Connect to ESP32**
   - Wire audio output to GPIO34
   - Wire EMF output to GPIO35
   - Connect power and ground

6. **Final assembly**
   - Secure components
   - Add enclosure (optional)
   - Label connectors

## Testing

### Initial Power-On Test
```bash
# Check voltage levels
3.3V rail: 3.2-3.4V ✓
5V rail: 4.8-5.2V ✓
Current draw: 80-250mA ✓
```

### Audio Test
```bash
# Upload test firmware
# Speak near microphone
# Observe serial output for voltage changes
Expected: 0.5-2.5V varying with sound
```

### EMF Test
```bash
# Upload test firmware
# Move phone near EMF sensor
# Observe serial output for voltage changes
Expected: 0.3-2.0V varying with EMF source
```

## Troubleshooting

### Common Issues

**No power**
- Check USB connection
- Verify voltage regulator
- Measure 3.3V output

**No audio readings**
- Check microphone power
- Verify GPIO34 connection
- Test op-amp output

**No EMF readings**
- Check coil connections
- Verify GPIO35 connection
- Test with strong magnet

**Erratic readings**
- Add decoupling capacitors
- Improve ground connections
- Check for loose wires

## Enclosure Design

### Recommended Enclosure Features

- Ventilation holes
- Microphone opening (acoustic port)
- EMF sensor positioning (external or window)
- USB access port
- LED indicators visible
- Mounting points

### 3D Printable Case (Optional)

Design considerations:
- Internal dimensions: 100mm x 80mm x 40mm
- Wall thickness: 2-3mm
- Mounting bosses for PCB
- Cable management clips

## Modifications and Extensions

### Add Display
- Connect I2C OLED display to ESP32
- Show real-time sensor values
- Display anomaly alerts

### Add More Sensors
- Temperature sensor (DHT22, BME280)
- Vibration sensor (SW-420)
- Light sensor (LDR, BH1750)

### Improve Sensitivity
- Use precision op-amps (OPA2134)
- Add programmable gain amplifiers
- Implement hardware filtering

## Maintenance

### Regular Checks
- Clean microphone opening
- Check battery voltage (if battery-powered)
- Verify WiFi connectivity
- Update firmware as needed

### Calibration
- Record baseline values in quiet environment
- Adjust thresholds in firmware
- Test with known EMF sources

## Safety Notes

- All components operate at safe voltages (< 5V)
- Avoid short circuits
- Use proper polarity when connecting power
- Handle ESP32 with anti-static precautions
- Do not expose to water or extreme temperatures

## Resources

### Datasheets
- ESP32: https://www.espressif.com/en/products/socs/esp32
- LM358: Texas Instruments
- AMS1117: Advanced Monolithic Systems

### Tools
- Soldering iron
- Multimeter
- Oscilloscope (optional, for debugging)
- Wire strippers
- Flush cutters

### Suppliers
- ESP32 boards: AliExpress, Amazon, Adafruit
- Electronic components: Digi-Key, Mouser, LCSC
- PCB fabrication: JLCPCB, PCBWay, OSH Park

## Contributing

Improvements to hardware designs are welcome! Please submit:
- Circuit improvements
- PCB layouts
- 3D printable enclosure designs
- Alternative component suggestions

## License

MIT License - Hardware designs are open source
