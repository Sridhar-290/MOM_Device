# MOM (Meal Ordering Module) 🍕

This project recreates the viral AI-powered belt that detects stomach growls and automatically orders food on Zomato.

## Components

1. **Hardware (The "Belt")**:
   - **ESP32 microcontroller**: Brain of the device.
   - **Stethoscope + Microphone (MAX4466)**: Captured heartbeats/growls.
   - **3D Printed Case**: To mount on a belt.
   - **Battery**: Mobile power.

2. **Software**:
   - **ESP32 Firmware**: Written in Arduino/C++. Monitors sound amplitude and hits a local server.
   - **Local Server**: Flask (Python). Analyzes the duration/frequency of sound triggers.
   - **AI Integration**: Claude 3.5 Sonnet to decide the best meal based on "growl size" and preferences.
   - **Food Ordering**: Mock Zomato MCP (Model Context Protocol) integration.

## Setup Instructions

### 1. Hardware Setup
- Connect the Microphone OUT pin to Pin 34 (ADC) of your ESP32.
- Power the ESP32 via a lipo battery or power bank.
- Assemble into a belt-mounted case.

### 2. ESP32 Firmware
- Open `esp32_firmware/esp32_firmware.ino` in Arduino IDE.
- Update `ssid`, `password`, and `serverName` (your computer's local IP).
- Flash to your ESP32.

### 3. Server Setup
- Navigate to `server/` directory.
- Install dependencies: `pip install -r requirements.txt`.
- Copy `.env.example` to `.env` and add your **Anthropic API Key**.
- Run the server: `python app.py`.

## Logic
- **Small Growl**: 1 trigger detected. Claude orders a light snack.
- **Long/Loud Growl**: Multiple triggers within 10 seconds. Claude orders a feast (e.g., 2 Pizzas or Biryani).

## Disclaimer
This is a recreation for educational purposes. Zomato does not have a public "Auto-Order" API for consumers, so the ordering part is simulated via a mock MCP logic.
