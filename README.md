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

**This is an educational project for demonstration purposes.**

### Two Operating Modes:

#### 1. **Mock Mode (Default - Safe)** ✅
- Simulates food ordering without placing real orders
- No money is charged
- Perfect for testing and demonstration
- Safe to use without any risk

#### 2. **Real Order Mode (Optional - Advanced)** ⚠️
- Uses web automation (Selenium) to place actual orders on Zomato/Swiggy
- **Will charge your account and place real orders**
- Requires manual OTP entry for login
- May violate platform Terms of Service
- **Use at your own risk**

**For instructions on enabling real orders, see [REAL_ORDERING_GUIDE.md](REAL_ORDERING_GUIDE.md)**

### Legal Notice
- Zomato and Swiggy do not provide public APIs for consumer ordering
- Web automation may violate their Terms of Service
- This project is for educational purposes only
- The authors are not responsible for any misuse or account suspension
- Always test in mock mode first before enabling real orders

## Features

- 🎤 **Stomach Growl Detection** - Uses stethoscope + microphone to detect hunger
- 🤖 **AI-Powered Recommendations** - Claude analyzes medical profile and recommends appropriate meals
- 🏥 **Medical Profile Integration** - Considers diabetes, allergies, BP, and other conditions
- 📍 **Location-Based** - Finds nearby restaurants in Mangaluru
- 🔄 **Two Modes** - Mock simulation (safe) or real ordering (advanced)
- 🍕 **Multi-Platform** - Supports both Zomato and Swiggy

## Project Status

✅ **Working Components:**
- ESP32 growl detection
- Flask server with AI integration
- Medical profile management
- Mock ordering system
- Web automation scripts for real ordering

⚠️ **Limitations:**
- Real ordering requires manual OTP entry
- Web automation may break if platform UI changes
- No official API support from food delivery platforms

