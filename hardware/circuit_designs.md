# Circuit Designs and Schematics

Hardware designs for the Flordevid mechatronic device.

## Overview

The Flordevid device consists of:
1. ESP32 microcontroller (main processing unit)
2. Audio sensor with amplification circuit
3. EMF sensor with amplification circuit
4. Power supply and regulation
5. Optional display and indicators

## System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Power Supply                         │
│  5V USB/Battery → 3.3V Regulator (AMS1117-3.3)         │
└────────────────┬────────────────────────────────────────┘
                 │
    ┌────────────┴────────────┐
    │                         │
┌───▼────────┐        ┌───────▼──────────┐
│   ESP32    │        │   Amplification  │
│            │◄───────┤     Circuits     │
│  DevKit-C  │        │                  │
└────────────┘        └──────────────────┘
     │                        ▲
     │                   ┌────┴─────┐
     └───────────────────┤ Sensors  │
                         └──────────┘
```

## Audio Capture Circuit

### Components
- Electret Microphone or MEMS Microphone (INMP441)
- Operational Amplifier (LM358 or TL072)
- Capacitors: 10µF, 100nF
- Resistors: 10kΩ, 100kΩ (for gain adjustment)

### Circuit Description

```
Microphone → C1 (10µF) → [Op-Amp] → C2 (10µF) → ESP32 GPIO34
                              │
                         Gain Control
                         (R1, R2, R3)
```

### Schematic (Text Format)

```
        +3.3V
          │
          ├─── R1 (10kΩ) ─── Microphone VCC
          │
     Microphone
          │
          │ Audio Out
          │
          ├─── C1 (10µF) ───┐
          │                  │
        GND              ┌───▼───┐
                         │ + IN  │
                    R2   │       │ LM358
              ┌────▶(10k)│ - IN  │ (Op-Amp)
              │          │       │
              │     ┌────┤ OUT   ├─── C2 (10µF) ─── ESP32 GPIO34
              │     │    └───────┘
              │     │         │
              │     R3        │
              │    (100k)  +3.3V
              │     │
              └─────┘
                   GND
```

### Gain Calculation

Gain = 1 + (R3 / R2) = 1 + (100kΩ / 10kΩ) = 11 (20.8 dB)

### PCB Considerations
- Keep microphone away from power supply noise
- Use ground plane for noise reduction
- Add decoupling capacitors near op-amp power pins

## EMF Sensor Circuit

### Components
- Coil (handmade or ready-made sensor coil)
- Operational Amplifier (LM358 or TL072)
- Capacitors: 100nF, 10µF
- Resistors: 1MΩ, 100kΩ (for high impedance input)

### DIY Coil Sensor
- Wire: 30-36 AWG enameled copper wire
- Turns: 500-1000 turns
- Core: Ferrite rod or air core
- Diameter: 2-5 cm

### Circuit Description

```
Coil Sensor → [High-Z Op-Amp Buffer] → [Amplifier] → ESP32 GPIO35
```

### Schematic (Text Format)

```
        Coil Sensor
           │  │
           │  └─── GND
           │
           ├─── C1 (100nF) ───┐
           │                   │
           R1 (1MΩ)       ┌────▼────┐
           │              │ +  IN   │
           ├──────────────┤         │ LM358
           │              │ -  IN   │ Buffer
           └─── GND       │         │
                          │   OUT   ├───┐
                          └─────────┘   │
                               │        │
                            +3.3V       │
                                        │
                                    ┌───▼───┐
                                    │ + IN  │
                              ┌────▶│       │ LM358
                              │     │ - IN  │ Amplifier
                              │     │       │
                              │  ┌──┤ OUT   ├─── C2 (10µF) ─── ESP32 GPIO35
                              │  │  └───────┘
                              │  │       │
                              │  R2    +3.3V
                             R3 (100k)
                            (1M) │
                              └──┘
                                GND
```

### Gain Calculation

- Buffer stage: Unity gain (1x)
- Amplifier stage: 1 + (R3 / R2) = 1 + (1MΩ / 100kΩ) = 11 (20.8 dB)
- Total gain: ~11x (20.8 dB)

## Power Supply

### Components
- AMS1117-3.3 voltage regulator
- Capacitors: 10µF (input), 22µF (output)
- Optional: USB Type-C connector or battery holder

### Circuit

```
5V Input ─── C1 (10µF) ─── [AMS1117-3.3] ─── C2 (22µF) ─── 3.3V Output
                │                  │                  │
               GND                GND                GND
```

### Power Consumption

- ESP32: ~160mA (WiFi active), ~80mA (WiFi idle)
- Op-amps: ~5mA each
- Total: ~200-250mA peak

### Recommended Power Sources
- USB 5V (500mA+)
- 3x AA batteries with boost converter
- 18650 Li-ion battery (3.7V) with boost converter

## Component List (BOM)

| Component | Quantity | Description | Approx. Price |
|-----------|----------|-------------|---------------|
| ESP32-DevKitC | 1 | Main MCU | $5-10 |
| LM358 | 2 | Dual op-amp | $0.50 |
| AMS1117-3.3 | 1 | Voltage regulator | $0.30 |
| Electret Microphone | 1 | Audio sensor | $1-2 |
| Coil (DIY) | 1 | EMF sensor | $2-5 |
| Resistors (assorted) | 10 | Various values | $0.50 |
| Capacitors (assorted) | 10 | Various values | $1.00 |
| Breadboard/PCB | 1 | Prototyping | $3-10 |
| Jumper wires | 1 set | Connections | $2 |
| USB cable | 1 | Power/programming | $2 |

**Total estimated cost: $20-35**

## Assembly Instructions

### Breadboard Prototype

1. **Mount ESP32** on breadboard
2. **Power rails**: Connect 3.3V and GND to power rails
3. **Audio circuit**:
   - Build op-amp circuit on breadboard
   - Connect microphone to input
   - Connect output to GPIO34
4. **EMF circuit**:
   - Build two-stage op-amp circuit
   - Connect coil sensor to input
   - Connect output to GPIO35
5. **Power supply**:
   - Connect USB to ESP32 or add voltage regulator

### PCB Design (Future)

For a permanent installation, design a PCB with:
- ESP32 module footprint
- SMD op-amps for compact design
- Proper ground plane
- Screw terminals for sensors
- Mounting holes

## Testing Procedures

### Audio Circuit Test
1. Power on the circuit
2. Speak near microphone
3. Measure voltage on GPIO34 - should vary between 0-3.3V
4. Check for ~1.65V DC offset at rest

### EMF Circuit Test
1. Power on the circuit
2. Bring strong magnet near coil
3. Measure voltage on GPIO35 - should show changes
4. Move phone/electronic device near sensor to verify detection

### Power Supply Test
1. Measure 3.3V output under no load
2. Measure 3.3V output under ~200mA load
3. Check for ripple with oscilloscope (should be < 50mV)

## Safety Considerations

- **Voltage levels**: All signals are low voltage (< 5V), safe to touch
- **Current limits**: Use appropriate fuses or current-limiting resistors
- **ESD protection**: Handle ESP32 with care to avoid static discharge
- **Enclosure**: Enclose electronics to prevent shorts

## Troubleshooting

| Problem | Possible Cause | Solution |
|---------|---------------|----------|
| No audio reading | Microphone not powered | Check VCC connection |
| Saturated audio | Gain too high | Reduce R3 value |
| No EMF reading | Coil polarity | Reverse coil connections |
| Noisy signals | Poor grounding | Improve ground connections |
| ESP32 won't boot | Power supply issue | Check 3.3V regulation |

## References

- ESP32 Datasheet: [espressif.com](https://www.espressif.com/en/products/socs/esp32)
- LM358 Datasheet: Texas Instruments
- Op-Amp Design Guide: Analog Devices

## License

Hardware designs are open source under MIT License.
