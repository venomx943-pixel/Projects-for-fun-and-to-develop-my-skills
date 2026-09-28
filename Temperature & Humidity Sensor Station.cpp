#include <Arduino.h>
#include <DHT.h>


const uint8_t DHT_PIN = 4;       
#define DHTTYPE DHT11           

// تهيئة كائن المستشعر
DHT dht(DHT_PIN, DHTTYPE);

// Range Validation & Bounds Checking

const float MIN_SAFE_TEMP = 0.0;      
const float MAX_SAFE_TEMP = 50.0;  
const float MIN_SAFE_HUMID = 0.0; 
const float MAX_SAFE_HUMID = 100.0;  

void setup() {
    
    Serial.begin(9600);
    
    
    dht.begin();
    
    Serial.println("[SECURITY_INIT] Environmental sensor station online and validating inputs...");
}

void loop() {
   // (Rate Limiting)
  
    delay(2000);

    
    float rawHumidity = dht.readHumidity();
    float rawTemperature = dht.readTemperature();

    // (Sensor Failure or Disconnection)
    if (isnan(rawHumidity) || isnan(rawTemperature)) {
        Serial.println("[ERROR] Sensor read failure! Possible hardware disconnection or fault injection.");
        return; // (Fail-Safe)
    }

     //Input Sanitization & Bounds Enforcement
    float secureTemperature = rawTemperature;
    float secureHumidity = rawHumidity;


    if (secureTemperature < MIN_SAFE_TEMP) {
        secureTemperature = MIN_SAFE_TEMP;
        Serial.println("[WARNING] Temperature below safe threshold, clamped to minimum.");
    } else if (secureTemperature > MAX_SAFE_TEMP) {
        secureTemperature = MAX_SAFE_TEMP;
        Serial.println("[WARNING] Temperature above safe threshold, clamped to maximum.")
    }
    if (secureHumidity < MIN_SAFE_HUMID) {
        secureHumidity = MIN_SAFE_HUMID;
        Serial.println("[WARNING] Humidity below safe threshold, clamped to minimum.");
    } else if (secureHumidity > MAX_SAFE_HUMID) {
        secureHumidity = MAX_SAFE_HUMID;
        Serial.println("[WARNING] Humidity above safe threshold, clamped to maximum.");
    }

    
    Serial.print("[DATA_LOG] Secure Temperature: ");
    Serial.print(secureTemperature);
    Serial.print(" °C | Secure Humidity: ");
    Serial.print(secureHumidity);
    Serial.println(" %");
}