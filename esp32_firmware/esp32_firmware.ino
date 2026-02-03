#include <WiFi.h>
#include <HTTPClient.h>

// WiFi Credentials
const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";
const char* serverName = "http://YOUR_LOCAL_IP:5000/detect";

const int micPin = 34; // ADC pin
const int threshold = 2500; // Increased threshold to avoid heartbeat interference
const int sampleWindow = 100; // Longer window for better signal averaging

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) { delay(500); Serial.print("."); }
  Serial.println("\nWiFi Connected!");
}

unsigned long soundStartTime = 0;
const int MIN_GROWL_DURATION = 1500; // Must be loud for at least 1.5 seconds

void loop() {
  unsigned long startMillis = millis(); 
  unsigned int peakToPeak = 0;   
  unsigned int signalMax = 0;
  unsigned int signalMin = 4095;

  // 1. Capture a 50ms snapshot
  while (millis() - startMillis < 50) {
    int sample = analogRead(micPin);
    if (sample < 4096) {
      if (sample > signalMax) signalMax = sample;
      else if (sample < signalMin) signalMin = sample;
    }
  }
  peakToPeak = signalMax - signalMin;

  // 2. Logic Filter
  if (peakToPeak > threshold) {
    if (soundStartTime == 0) {
      soundStartTime = millis(); // Sound just started
    } else {
      unsigned long duration = millis() - soundStartTime;
      Serial.printf("Sustained sound: %lu ms\n", duration);
      
      // Only trigger if sound has been loud for MIN_GROWL_DURATION
      if (duration > MIN_GROWL_DURATION) {
        Serial.println("REAL GROWL DETECTED!");
        sendTrigger(peakToPeak);
        soundStartTime = 0; // Reset
        delay(60000); // Sleep for 1 minute after ordering
      }
    }
  } else {
    soundStartTime = 0; // Sound stopped or was too quiet, reset timer
  }
}

void sendTrigger(int amplitude) {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(serverName);
    http.addHeader("Content-Type", "application/json");
    String httpRequestData = "{\"amplitude\":" + String(amplitude) + "}";
    http.POST(httpRequestData);
    http.end();
  }
}
