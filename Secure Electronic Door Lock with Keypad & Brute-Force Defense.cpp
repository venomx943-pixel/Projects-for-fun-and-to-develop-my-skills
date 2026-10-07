#include <Arduino.h>
#include <Keypad.h>
#include <Servo.h>

// Keypad matrix configuration
const byte ROWS = 4; 
const byte COLS = 4; 
char keys[ROWS][COLS] = {
  {'1','2','3','A'},
  {'4','5','6','B'},
  {'7','8','9','C'},
  {'*','0','#','D'}
};
byte rowPins[ROWS] = {9, 8, 7, 6}; 
byte colPins[COLS] = {5, 4, 3, 2}; 

// Initialize Keypad instance
Keypad customKeypad = Keypad(makeKeymap(keys), rowPins, colPins, ROWS, COLS);

// Lock mechanism pin and Servo object configuration
const uint8_t LOCK_SERVO_PIN = 10;
Servo lockServo;

// Security & Password configuration
const char CORRECT_PIN[5] = "1234"; // 4-digit secure code + null terminator
char inputBuffer[5];               // Buffer for user input with overflow protection
uint8_t inputIndex = 0;

// Brute-force defense variables and rate limiting
uint8_t failedAttempts = 0;
const uint8_t MAX_FAILED_ATTEMPTS = 3;
unsigned long lockoutStartTime = 0;
const unsigned long LOCKOUT_DURATION = 10000; // 10 seconds penalty lockout
bool isLockedOut = false;

void setup() {
    // Initialize serial communication for security audit logs
    Serial.begin(9600);
    
    // Attach servo motor to hardware pin
    lockServo.attach(LOCK_SERVO_PIN);
    
    // Fail-safe default: Ensure lock starts in a secure LOCKED position (0 degrees)
    lockServo.write(0);
    
    // Secure memory clearing upon boot
    memset(inputBuffer, 0, sizeof(inputBuffer));
    
    Serial.println("[SECURITY_INIT] Electronic lock system online. Locked state enforced.");
}

void loop() {
    // Check if system is under brute-force penalty lockout
    if (isLockedOut) {
        if (millis() - lockoutStartTime >= LOCKOUT_DURATION) {
            isLockedOut = false;
            failedAttempts = 0;
            Serial.println("[SECURITY_INFO] Lockout period expired. System re-enabled.");
        } else {
            return; // Block execution during penalty period
        }
    }

    char customKey = customKeypad.getKey();
    
    if (customKey) {
        // If user presses '#' (Submit / Verify)
        if (customKey == '#') {
            // Null-terminate string safely
            inputBuffer[inputIndex] = '\0'; 
            
            // Secure string comparison against correct PIN
            if (strcmp(inputBuffer, CORRECT_PIN) == 0) {
                Serial.println("[ACCESS_GRANTED] PIN verified. Unlocking door...");
                lockServo.write(90); // Unlock position (90 degrees)
                delay(5000);         // Keep unlocked for 5 seconds safely
                lockServo.write(0);  // Relock automatically
                Serial.println("[ACCESS_INFO] Door relocked securely.");
                failedAttempts = 0;  // Reset failed attempts counter on success
            } else {
                failedAttempts++;
                Serial.print("[SECURITY_ALERT] Invalid PIN attempt. Failed count: ");
                Serial.println(failedAttempts);
                
                // Trigger brute-force defense lockdown if threshold is exceeded
                if (failedAttempts >= MAX_FAILED_ATTEMPTS) {
                    isLockedOut = true;
                    lockoutStartTime = millis();
                    Serial.println("[SECURITY_LOCKOUT] Maximum failed attempts reached! System locked down for 10 seconds.");
                }
            }
            
            // Securely wipe input buffer from RAM to prevent information leakage
            memset(inputBuffer, 0, sizeof(inputBuffer));
            inputIndex = 0;
        } 
        // If user presses '*' (Clear buffer manually)
        else if (customKey == '*') {
            memset(inputBuffer, 0, sizeof(inputBuffer));
            inputIndex = 0;
            Serial.println("[INFO] Input buffer cleared by user.");
        } 
        // Regular digit input with buffer overflow protection
        else {
            if (inputIndex < 4) {
                inputBuffer[inputIndex] = customKey;
                inputIndex++;
                Serial.print("[INPUT] Key registered: *"); // Masked logging for security
            } else {
                Serial.println("[WARNING] Input buffer overflow attempt detected! Resetting buffer.");
                memset(inputBuffer, 0, sizeof(inputBuffer));
                inputIndex = 0;
            }
        }
    }
}