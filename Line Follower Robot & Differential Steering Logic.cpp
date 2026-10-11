#include <Arduino.h>

// Definition of L298N motor driver pins using constant variables for memory safety
const uint8_t ENA_PIN = 3;  // Left motor PWM speed control
const uint8_t IN1_PIN = 4;  // Left motor direction 1
const uint8_t IN2_PIN = 5;  // Left motor direction 2
const uint8_t IN3_PIN = 6;  // Right motor direction 1
const uint8_t IN4_PIN = 7;  // Right motor direction 2
const uint8_t ENB_PIN = 10; // Right motor PWM speed control

// Definition of Line Tracking IR Sensor pins
const uint8_t LEFT_IR_PIN = A0;   // Left line tracking sensor input
const uint8_t RIGHT_IR_PIN = A1;  // Right line tracking sensor input

// Operational constants and speed configurations
const uint8_t CRUISE_SPEED = 150; // Safe forward cruise speed
const uint8_t TURN_SPEED = 120;   // Differential correction steering speed
const int LINE_THRESHOLD = 500;   // Analog threshold distinguishing line vs surface

void setup() {
    // Initialize serial communication for security and system monitoring
    Serial.begin(9600);

    // Configure motor control pins as outputs
    pinMode(ENA_PIN, OUTPUT);
    pinMode(IN1_PIN, OUTPUT);
    pinMode(IN2_PIN, OUTPUT);
    pinMode(IN3_PIN, OUTPUT);
    pinMode(IN4_PIN, OUTPUT);
    pinMode(ENB_PIN, OUTPUT);

    // Configure IR tracking sensor pins as inputs
    pinMode(LEFT_IR_PIN, INPUT);
    pinMode(RIGHT_IR_PIN, INPUT);

    // Fail-safe default: Ensure motors are completely stopped upon boot
    analogWrite(ENA_PIN, 0);
    analogWrite(ENB_PIN, 0);
    digitalWrite(IN1_PIN, LOW);
    digitalWrite(IN2_PIN, LOW);
    digitalWrite(IN3_PIN, LOW);
    digitalWrite(IN4_PIN, LOW);

    Serial.println("[SECURITY_INIT] Line follower robot initialized in safe STOP state...");
}

// Safe motor control function with PWM bounds checking (Clamping)
void controlMotors(int leftSpeed, bool leftForward, int rightSpeed, bool rightForward) {
    // PWM bounds sanitization to prevent overflows
    if (leftSpeed < 0) leftSpeed = 0;
    if (leftSpeed > 255) leftSpeed = 255;
    if (rightSpeed < 0) rightSpeed = 0;
    if (rightSpeed > 255) rightSpeed = 255;

    // Set left motor direction safely
    digitalWrite(IN1_PIN, leftForward ? HIGH : LOW);
    digitalWrite(IN2_PIN, leftForward ? LOW : HIGH);

    // Set right motor direction safely
    digitalWrite(IN3_PIN, rightForward ? HIGH : LOW);
    digitalWrite(IN4_PIN, rightForward ? LOW : HIGH);

    // Apply PWM speed signals to driver enable pins
    analogWrite(ENA_PIN, leftSpeed);
    analogWrite(ENB_PIN, rightSpeed);
}

void loop() {
    // Rate limiting delay to stabilize sensor readings and prevent CPU exhaustion
    delay(20);

    // Read raw analog values from line tracking IR sensors
    int leftRaw = analogRead(LEFT_IR_PIN);
    int rightRaw = analogRead(RIGHT_IR_PIN);

    // Input sanitization and bounds checking (0 to 1023)
    if (leftRaw < 0) leftRaw = 0;
    if (leftRaw > 1023) leftRaw = 1023;
    if (rightRaw < 0) rightRaw = 0;
    if (rightRaw > 1023) rightRaw = 1023;

    // Determine line position based on threshold logic
    bool leftOnLine = (leftRaw > LINE_THRESHOLD);
    bool rightOnLine = (rightRaw > LINE_THRESHOLD);

    // Navigation decision logic based on sensor feedback
    if (leftOnLine && !rightOnLine) {
        // Left sensor drifted off or onto line: corrective differential steering left
        Serial.println("[NAVIGATION] Correcting trajectory: Steering Left.");
        controlMotors(TURN_SPEED, false, CRUISE_SPEED, true);
    } 
    else if (!leftOnLine && rightOnLine) {
        // Right sensor drifted: corrective differential steering right
        Serial.println("[NAVIGATION] Correcting trajectory: Steering Right.");
        controlMotors(CRUISE_SPEED, true, TURN_SPEED, false);
    } 
    else if (leftOnLine && rightOnLine) {
        // Both sensors aligned with line: move straight forward
        Serial.println("[NAVIGATION] Line centered: Moving Forward.");
        controlMotors(CRUISE_SPEED, true, CRUISE_SPEED, true);
    } 
    else {
        // Line lost (both on white surface): slow forward search pattern (Fail-safe default)
        Serial.println("[WARNING] Line lost! Slowing down to search safely.");
        controlMotors(50, true, 50, true);
    }
}