#include <Arduino.h>

// Definition of L298N motor driver pins using constant variables for memory safety
const uint8_t ENA_PIN = 3;  // PWM speed control for Left Motor
const uint8_t IN1_PIN = 4;  // Direction control 1 for Left Motor
const uint8_t IN2_PIN = 5;  // Direction control 2 for Left Motor
const uint8_t ENB_PIN = 9;  // PWM speed control for Right Motor
const uint8_t IN3_PIN = 6;  // Direction control 1 for Right Motor
const uint8_t IN4_PIN = 7;  // Direction control 2 for Right Motor

// Security and operational constants for PWM limits
const uint8_t MIN_PWM = 0;      // Minimum speed (Fully stopped)
const uint8_t MAX_PWM = 255;    // Maximum speed (Full power)
const uint8_t DEFAULT_SPEED = 180; // Safe operational cruise speed

void setup() {
    // Initialize serial communication for system monitoring and logs
    Serial.begin(9600);

    // Configure all motor control pins as outputs
    pinMode(ENA_PIN, OUTPUT);
    pinMode(IN1_PIN, OUTPUT);
    pinMode(IN2_PIN, OUTPUT);
    pinMode(ENB_PIN, OUTPUT);
    pinMode(IN3_PIN, OUTPUT);
    pinMode(IN4_PIN, OUTPUT);

    // Fail-safe default: Ensure motors are completely stopped upon boot
    analogWrite(ENA_PIN, 0);
    analogWrite(ENB_PIN, 0);
    digitalWrite(IN1_PIN, LOW);
    digitalWrite(IN2_PIN, LOW);
    digitalWrite(IN3_PIN, LOW);
    digitalWrite(IN4_PIN, LOW);

    Serial.println("[SECURITY_INIT] Dual motor driver initialized in safe STOP state...");
}

// Function to safely set motor speeds and directions with bounds checking (Clamping)
void setMotors(int leftSpeed, bool leftForward, int rightSpeed, bool rightForward) {
    // Input sanitization and PWM bounds checking to prevent hardware failure or overflow
    if (leftSpeed < MIN_PWM) {
        leftSpeed = MIN_PWM;
    } else if (leftSpeed > MAX_PWM) {
        leftSpeed = MAX_PWM;
    }

    if (rightSpeed < MIN_PWM) {
        rightSpeed = MIN_PWM;
    } else if (rightSpeed > MAX_PWM) {
        rightSpeed = MAX_PWM;
    }

    // Set left motor direction safely
    if (leftForward) {
        digitalWrite(IN1_PIN, HIGH);
        digitalWrite(IN2_PIN, LOW);
    } else {
        digitalWrite(IN1_PIN, LOW);
        digitalWrite(IN2_PIN, HIGH);
    }

    // Set right motor direction safely
    if (rightForward) {
        digitalWrite(IN3_PIN, HIGH);
        digitalWrite(IN4_PIN, LOW);
    } else {
        digitalWrite(IN3_PIN, LOW);
        digitalWrite(IN4_PIN, HIGH);
    }

    // Apply PWM speed signals to driver enable pins
    analogWrite(ENA_PIN, leftSpeed);
    analogWrite(ENB_PIN, rightSpeed);
}

void loop() {
    // Execution sequence demonstrating precise dual-motor control
    Serial.println("[EXECUTION] Moving Forward at controlled safe speed.");
    setMotors(DEFAULT_SPEED, true, DEFAULT_SPEED, true);
    delay(2000);

    Serial.println("[EXECUTION] Braking / Stopping temporarily.");
    setMotors(0, true, 0, true);
    delay(1000);

    Serial.println("[EXECUTION] Reversing at controlled safe speed.");
    setMotors(DEFAULT_SPEED, false, DEFAULT_SPEED, false);
    delay(2000);

    Serial.println("[EXECUTION] Stopping before loop reset.");
    setMotors(0, true, 0, true);
    delay(2000);
}