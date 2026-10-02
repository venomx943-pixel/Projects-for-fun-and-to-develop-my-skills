#include <Arduino.h>

// Hardware pin definitions using constant variables for memory safety
const uint8_t SOIL_SENSOR_PIN = A1; // Analog soil moisture sensor input pin
const uint8_t PUMP_PIN = 7;         // Water pump relay output pin

// Security and operational thresholds (Input Validation and Bounds)
const int MIN_ANALOG_VALUE = 0;     // Minimum raw sensor reading
const int MAX_ANALOG_VALUE = 1023;  // Maximum raw sensor reading
const int DRY_THRESHOLD = 700;      // Threshold above which soil is considered dry (requires water)
const int WET_THRESHOLD = 400;      // Threshold below which soil is sufficiently moist

void setup() {
    // Initialize serial communication for security monitoring and system logs
    Serial.begin(9600);
    
    // Configure electrical pin directions
    pinMode(SOIL_SENSOR_PIN, INPUT);
    pinMode(PUMP_PIN, OUTPUT);
    
    // Fail-safe default: Ensure pump starts in a safe OFF state upon boot
    digitalWrite(PUMP_PIN, LOW);
    
    Serial.println("[SECURITY_INIT] Smart irrigation system initialized in a safe state...");
}

void loop() {
    // Rate limiting: Delay to prevent power surges and excessive sensor polling
    delay(2000);

    // Read raw soil moisture input from the hardware pin
    int rawSoilValue = analogRead(SOIL_SENSOR_PIN);

    // Input sanitization and bounds checking to prevent invalid hardware states or fault injection
    if (rawSoilValue < MIN_ANALOG_VALUE) {
        rawSoilValue = MIN_ANALOG_VALUE;
        Serial.println("[WARNING] Soil sensor reading below minimum bound. Clamped.");
    } else if (rawSoilValue > MAX_ANALOG_VALUE) {
        rawSoilValue = MAX_ANALOG_VALUE;
        Serial.println("[WARNING] Soil sensor reading above maximum bound. Clamped.");
    }

    // Active state logic with safety thresholds (Hysteresis control to protect hardware)
    if (rawSoilValue > DRY_THRESHOLD) {
        // Soil is critically dry: activate water pump safely
        digitalWrite(PUMP_PIN, HIGH);
        Serial.println("[WARNING] Soil is critically dry! Water pump activated.");
    } 
    else if (rawSoilValue < WET_THRESHOLD) {
        // Soil is sufficiently moist: deactivate pump
        digitalWrite(PUMP_PIN, LOW);
        Serial.println("[INFO] Soil moisture level is optimal. Pump deactivated.");
    }
    
    // Log current sanitized sensor value for system transparency
    Serial.print("[DATA_LOG] Sanitized Soil Moisture Reading: ");
    Serial.println(rawSoilValue);
}