# Hardware Setup Guide

Complete guide to assembling and configuring the Flordevid hardware.

## Prerequisites

- Basic electronics knowledge
- Soldering skills (for permanent assembly)
- Required tools and components (see hardware/README.md)

## Overview

This guide walks through:
1. Component preparation
2. Circuit assembly
3. Connection to ESP32
4. Initial testing
5. Enclosure assembly

## Step 1: Component Preparation

### Verify Components

Check that you have all required components:

- [ ] ESP32-DevKitC or compatible board
- [ ] LM358 dual op-amp (2 pieces)
- [ ] AMS1117-3.3 voltage regulator
- [ ] Electret microphone or INMP441 MEMS microphone
- [ ] Coil for EMF sensing (purchased or DIY)
- [ ] Resistors: 10kΩ (3x), 100kΩ (2x), 1MΩ (2x)
- [ ] Capacitors: 10µF (4x), 100nF (2x), 22µF (1x)
- [ ] Breadboard or PCB
- [ ] Jumper wires
- [ ] USB cable for programming/power

### DIY Coil Sensor (Optional)

If making your own EMF coil:

1. **Materials needed**:
   - 30-36 AWG enameled copper wire
   - Ferrite rod (5-10 cm) or cardboard tube
   - Tape or adhesive

2. **Winding process**:
   - Secure wire end to rod/tube
   - Wind 500-1000 turns tightly
   - Keep turns even and close together
   - Secure end with tape
   - Strip enamel from wire ends

3. **Testing coil**:
   - Measure resistance: should be 50-500Ω
   - Test inductance if possible: 50-200mH

## Step 2: Circuit Assembly

### Option A: Breadboard Assembly

#### 2.1 Power Rails Setup

```
Top rail (+):    Connect to ESP32 3.3V
Bottom rail (-): Connect to ESP32 GND
```

#### 2.2 Audio Amplifier Circuit

1. Insert LM358 op-amp (IC1) into breadboard
2. Connect power:
   - Pin 8 (VCC) → 3.3V rail
   - Pin 4 (GND) → GND rail

3. Build amplifier circuit:
   ```
   Microphone VCC → 3.3V (through 10kΩ)
   Microphone GND → GND
   Microphone OUT → C1 (10µF) → IC1 pin 3 (IN+)
   IC1 pin 2 (IN-) → R2 (10kΩ) → GND
   IC1 pin 2 → R3 (100kΩ) → IC1 pin 1 (OUT)
   IC1 pin 1 → C2 (10µF) → ESP32 GPIO34
   ```

4. Add decoupling:
   - 100nF capacitor between IC1 VCC and GND (close to chip)

#### 2.3 EMF Amplifier Circuit

1. Insert second LM358 op-amp (IC2) into breadboard
2. Connect power:
   - Pin 8 (VCC) → 3.3V rail
   - Pin 4 (GND) → GND rail

3. Build two-stage circuit:
   
   **Stage 1 (Buffer):**
   ```
   Coil → C3 (100nF) → IC2 pin 3 (IN+)
   IC2 pin 3 → R4 (1MΩ) → GND
   IC2 pin 2 (IN-) → IC2 pin 1 (OUT)
   ```
   
   **Stage 2 (Amplifier):**
   ```
   IC2 pin 1 → IC2 pin 5 (IN+)
   IC2 pin 6 (IN-) → R5 (100kΩ) → GND
   IC2 pin 6 → R6 (1MΩ) → IC2 pin 7 (OUT)
   IC2 pin 7 → C4 (10µF) → ESP32 GPIO35
   ```

4. Add decoupling:
   - 100nF capacitor between IC2 VCC and GND

#### 2.4 ESP32 Connections

Connect to ESP32:
- GPIO34 ← Audio circuit output (through 10µF cap)
- GPIO35 ← EMF circuit output (through 10µF cap)
- 3.3V → Power rail
- GND → Ground rail

### Option B: PCB Assembly

1. Order PCB from manufacturer (design your own or use reference)
2. Apply solder paste to pads (for SMD components)
3. Place components
4. Reflow solder (hot air station or reflow oven)
5. Solder through-hole components
6. Clean flux residue
7. Inspect solder joints

## Step 3: Power Supply

### Using USB Power

Simply connect ESP32 to computer via USB cable. The ESP32's onboard regulator provides 3.3V.

### Using External 5V

1. Build voltage regulator circuit:
   ```
   5V IN → C5 (10µF) → AMS1117 IN
   AMS1117 GND → GND
   AMS1117 OUT → C6 (22µF) → 3.3V rail
   ```

2. Connect 5V source (USB, battery with boost converter, etc.)

### Using Battery

**Option 1: 3x AA batteries**
- Use 4.5V directly with AMS1117 regulator
- Expected runtime: 10-20 hours

**Option 2: 18650 Li-ion**
- Use boost converter to 5V
- Then AMS1117 to 3.3V
- Expected runtime: 20-40 hours

## Step 4: Initial Testing

### Pre-Power Checks

Before connecting power:

1. **Visual inspection**:
   - [ ] Check for short circuits
   - [ ] Verify all connections
   - [ ] Ensure correct polarity

2. **Continuity tests**:
   - [ ] Test power rails (should NOT be connected)
   - [ ] Test ground connections (should be connected)
   - [ ] Verify GPIO connections

### Power-On Test

1. Connect USB cable to ESP32
2. Check LED on ESP32 (should light up)
3. Measure voltages:
   - 3.3V rail: 3.2-3.4V ✓
   - Audio circuit output (idle): ~1.65V ✓
   - EMF circuit output (idle): ~0.5-1.5V ✓

### Functional Tests

#### Audio Test

1. Upload test sketch:
   ```cpp
   void loop() {
     int val = analogRead(34);
     Serial.println(val);
     delay(10);
   }
   ```

2. Open serial monitor (115200 baud)
3. Speak near microphone
4. Observe values changing: 500-3000 range
5. Should vary with sound intensity

#### EMF Test

1. Upload test sketch:
   ```cpp
   void loop() {
     int val = analogRead(35);
     Serial.println(val);
     delay(10);
   }
   ```

2. Open serial monitor (115200 baud)
3. Move phone or magnet near coil
4. Observe values changing: 200-3000 range
5. Should respond to electromagnetic fields

## Step 5: Firmware Upload

1. Install PlatformIO or Arduino IDE
2. Navigate to `/firmware` directory
3. Update WiFi credentials in `src/main.cpp`:
   ```cpp
   const char* ssid = "YourWiFiName";
   const char* password = "YourPassword";
   ```

4. Build and upload:
   ```bash
   # Using PlatformIO
   cd firmware
   pio run --target upload
   
   # Or using Arduino IDE
   # Open src/main.cpp and click Upload
   ```

5. Open serial monitor to verify operation

## Step 6: Enclosure Assembly

### 3D Printed Case

1. Print case parts (top, bottom, mounting brackets)
2. Insert PCB/breadboard into case
3. Align sensor openings:
   - Microphone facing forward
   - EMF coil accessible or external
4. Route USB cable through port
5. Close case and secure with screws

### DIY Enclosure

Materials:
- Plastic project box (100mm x 80mm x 40mm)
- Drill for cable holes
- Hot glue or standoffs for mounting

Steps:
1. Drill holes for:
   - USB cable
   - Microphone opening
   - Mounting screws
2. Mount PCB/breadboard with standoffs
3. Secure components with hot glue
4. Label external features
5. Close enclosure

## Step 7: Final Configuration

### WiFi Setup

1. Connect to serial monitor
2. ESP32 will display IP address
3. Note IP address for dashboard access

### Sensor Calibration

1. Place device in quiet environment
2. Record baseline values:
   - Audio: typically 0.05-0.15V
   - EMF: typically 0.3-0.8V
3. Update thresholds in firmware if needed

### Test Complete System

1. Start AI core backend:
   ```bash
   cd ai_core
   python main.py --port /dev/ttyUSB0
   ```

2. Start dashboard:
   ```bash
   cd ui
   uvicorn main:app --reload
   ```

3. Open browser to `http://localhost:8000`
4. Verify real-time data display
5. Test anomaly detection with loud sound or EMF source

## Troubleshooting

### No Power
- Check USB cable
- Verify ESP32 LED is on
- Test USB port with another device

### No Serial Communication
- Check driver installation (CP210x or CH340)
- Verify COM port selection
- Try different USB cable
- Press BOOT button during upload

### Audio Not Working
- Check microphone power connection
- Verify GPIO34 connection
- Test microphone with multimeter (should show ~1.65V DC)
- Adjust gain if signal too weak/strong

### EMF Not Working
- Check coil connections (reverse if needed)
- Verify GPIO35 connection
- Test with strong magnet
- Ensure coil is properly wound

### Noisy Readings
- Add more decoupling capacitors
- Improve ground connections
- Keep sensor wires short
- Add shielding to coil

## Next Steps

- Proceed to [firmware_guide.md](firmware_guide.md) for firmware customization
- See [api_reference.md](api_reference.md) for API integration
- Train custom models with [ai_training.md](ai_training.md)

## Safety Notes

- Always disconnect power before modifying circuits
- Use proper ESD protection when handling ESP32
- Ensure proper ventilation when soldering
- Keep away from water and extreme temperatures
- Monitor temperature during operation (ESP32 may warm up)

## Support

For issues or questions:
- Check troubleshooting section
- Review hardware documentation
- Open issue on GitHub
- Consult ESP32 community forums
