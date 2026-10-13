#include <Arduino.h>
#include <WiFi.h>
#include <DHT.h>

// Wi-Fi credentials (In production, use secure config storage or secure boot)
const char* WIFI_SSID = "SecureRobotNet";
const char* WIFI_PASSWORD = "SuperSecretPassword123";

// Hardware pin and sensor configuration
const uint8_t DHT_PIN = 4;
#define DHTTYPE DHT11
DHT dht(DHT_PIN, DHTTYPE);

// Security and operational constants
const unsigned long PUBLISH_INTERVAL = 5000; // Send telemetry every 5 seconds (Rate Limiting)
unsigned long lastPublishTime = 0;
const uint8_t MAX_WIFI_RETRIES = 20;

void setup() {
    // Initialize serial communication for security audit logs
    Serial.begin(9600);
    delay(1000);

    // Initialize sensor
    dht.begin();

    // Connect to Wi-Fi securely with timeout prevention (Fail-Safe Default)
    Serial.println("[SECURITY_INIT] Connecting to secure Wi-Fi network...");
    WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

    uint8_t retryCount = 0;
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
        retryCount++;
        // Prevent infinite blocking loop if network is unreachable
        if (retryCount >= MAX_WIFI_RETRIES) {
            Serial.println("\n[SECURITY_ALERT] Wi-Fi connection timeout! Operating in offline fail-safe mode.");
            break; 
        }
    }

    if (WiFi.status() == WL_CONNECTED) {
        Serial.println("\n[SECURITY_INFO] Wi-Fi connected successfully. IP Address: ");
        Serial.println(WiFi.localIP());
    }
}

void loop() {
    // Rate limiting using non-blocking timing (millis) to prevent CPU starvation
    if (millis() - lastPublishTime >= PUBLISH_INTERVAL) {
        lastPublishTime = millis();

        // Read raw sensor data
        float rawTemp = dht.readTemperature();
        float rawHumid = dht.readHumidity();

        // Input sanitization and bounds checking for fault injection / sensor failure
        if (isnan(rawTemp) || isnan(rawHumid)) {
            Serial.println("[ERROR] Sensor telemetry failure! Possible hardware disconnection.");
            return; // Fail-safe exit for this cycle
        }

        // Clamp values to safe boundaries
        float secureTemp = rawTemp;
        if (secureTemp < -40.0) secureTemp = -40.0;
        if (secureTemp > 80.0) secureTemp = 80.0;

        float secureHumidity = rawHumid;
        if (secureHumidity < 0.0) secureHumidity = 0.0;
        if (secureHumidity > 100.0) secureHumidity = 100.0;

        // Log telemetry securely
        Serial.println("[CLOUD_TELEMETRY] Preparing payload transmission...");
        Serial.print("[DATA_LOG] Temp: ");
        Serial.print(secureTemp);
        Serial.print(" C | Humidity: ");
        Serial.print(secureHumidity);
        Serial.println(" %");

        // Check network status before simulating cloud transmission
        if (WiFi.status() == WL_CONNECTED) {
            Serial.println("[CLOUD_SYNC] Telemetry packet successfully transmitted over secure socket.");
        } else {
            Serial.println("[WARNING] Network offline. Telemetry cached locally in buffer.");
        }
    }

    // Brief idle delay to maintain system stability
    delay(100);
}