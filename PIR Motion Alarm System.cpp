#include <Arduino.h>


const uint8_t PIR_PIN = 2;       
const uint8_t BUZZER_PIN = 8;    
const uint8_t LED_WARN_PIN = 10; 

// State management variables
volatile uint8_t motionState = LOW; 
unsigned long lastMotionTime = 0;   
const unsigned long ALARM_DURATION = 3000; 

void setup() {
    
    Serial.begin(9600);
    
    
    pinMode(PIR_PIN, INPUT);
    pinMode(BUZZER_PIN, OUTPUT);
    pinMode(LED_WARN_PIN, OUTPUT);
    

    digitalWrite(BUZZER_PIN, LOW);
    digitalWrite(LED_WARN_PIN, LOW);
    
    Serial.println("[SECURITY_INIT] Security system operational and scanning active...");
}

void loop() {
    
    int currentReading = digitalRead(PIR_PIN);
    
    
    if (currentReading == HIGH) {
        motionState = HIGH;
        lastMotionTime = millis(); 

        
        digitalWrite(BUZZER_PIN, HIGH);
        digitalWrite(LED_WARN_PIN, HIGH);
        
        Serial.println("[ALERT] Warning: Suspicious motion detected in the perimeter!");
    } 
    else {
        
        if (motionState == HIGH && (millis() - lastMotionTime >= ALARM_DURATION)) {
            motionState = LOW;
            
           
            digitalWrite(BUZZER_PIN, LOW);
            digitalWrite(LED_WARN_PIN, LOW);
            
            Serial.println("[INFO] System returned to secure state (Perimeter stable).");
        }
    }
    
    delay(100);
}