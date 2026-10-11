#include <Arduino.h>

// Definition of hardware pins using constant variables for memory safety
const uint8_t TRIG_PIN = 9;      // Ultrasonic sensor Trigger pin
const uint8_t ECHO_PIN = 10;     // Ultrasonic sensor Echo pin

// Motor Driver Pins (e.g., L298N) controlling left and right motors
const uint8_t MOTOR_LEFT_IN1 = 4;
const uint8_t MOTOR_LEFT_IN2 = 5;
const uint8_t MOTOR_RIGHT_IN1 = 6;
const uint8_t MOTOR_RIGHT_IN2 = 7;

// Safety and operational thresholds
const int SAFE_DISTANCE_CM = 20;     // Minimum safe distance before obstacle avoidance triggers
const unsigned long REVERSE_TIME = 500; // Duration to reverse in milliseconds
const unsigned long TURN_TIME = 400;    // Duration to turn in milliseconds

void setup() {
    // Initialize serial communication for security monitoring and system logs
    Serial.begin(9600);
    
    // Configure sensor pins directions
    pinMode(TRIG_PIN, OUTPUT);
    pinMode(ECHO_PIN, INPUT);
    
    // Configure motor control pins as outputs
    pinMode(MOTOR_LEFT_IN1, OUTPUT);
    pinMode(MOTOR_LEFT_IN2, OUTPUT);
    pinMode(MOTOR_RIGHT_IN1, OUTPUT);
    pinMode(MOTOR_RIGHT_IN2, OUTPUT);
    
    // Fail-safe default: Ensure motors start in a safe STOP state upon boot
    digitalWrite(MOTOR_LEFT_IN1, LOW);
    digitalWrite(MOTOR_LEFT_IN2, LOW);
    digitalWrite(MOTOR_RIGHT_IN1, LOW);
    digitalWrite(MOTOR_RIGHT_IN2, LOW);
    
    Serial.println("[SECURITY_INIT] Obstacle avoidance robot initialized in safe STOP state...");
}

// Function to safely measure distance using ultrasonic sensor with noise filtering and timeout protection
long getFilteredDistance() {
    // Clear trigger pin to ensure a clean low signal
    digitalWrite(TRIG_PIN, LOW);
    delayMicroseconds(2);
    
    // Send a 10 microsecond high pulse to trigger distance measurement
    digitalWrite(TRIG_PIN, HIGH);
    delayMicroseconds(10);
    digitalWrite(TRIG_PIN, LOW);
    
    // Read echo pulse duration with a safety timeout (30ms max to prevent code freezing)
    long duration = pulseIn(ECHO_PIN, HIGH, 30000);
    
    // Input sanitization and error check for sensor timeout or fault injection
    if (duration == 0) {
        Serial.println("[WARNING] Ultrasonic sensor timeout or invalid echo. Defaulting to max safe distance.");
        return 999; // Default large value assuming clear path
    }
    
    // Calculate distance in centimeters (Speed of sound = 0.034 cm/us, divided by 2 for round trip)
    long distance = duration * 0.034 / 2;
    
    // Bounds checking and sanitization to prevent abnormal sensor spikes or hardware anomalies
    if (distance < 0) {
        distance = 0;
    } else if (distance > 400) { // HC-SR04 max range is approx 400cm
        distance = 400;
    }
    
    return distance;
}

void moveForward() {
    digitalWrite(MOTOR_LEFT_IN1, HIGH);
    digitalWrite(MOTOR_LEFT_IN2, LOW);
    digitalWrite(MOTOR_RIGHT_IN1, HIGH);
    digitalWrite(MOTOR_RIGHT_IN2, LOW);
}

void moveBackward() {
    digitalWrite(MOTOR_LEFT_IN1, LOW);
    digitalWrite(MOTOR_LEFT_IN2, HIGH);
    digitalWrite(MOTOR_RIGHT_IN1, LOW);
    digitalWrite(MOTOR_RIGHT_IN2, HIGH);
}

void turnRight() {
    digitalWrite(MOTOR_LEFT_IN1, HIGH);
    digitalWrite(MOTOR_LEFT_IN2, LOW);
    digitalWrite(MOTOR_RIGHT_IN1, LOW);
    digitalWrite(MOTOR_RIGHT_IN2, HIGH);
}

void stopRobot() {
    digitalWrite(MOTOR_LEFT_IN1, LOW);
    digitalWrite(MOTOR_LEFT_IN2, LOW);
    digitalWrite(MOTOR_RIGHT_IN1, LOW);
    digitalWrite(MOTOR_RIGHT_IN2, LOW);
}

void loop() {
    // Get sanitized distance reading from sensor
    long currentDistance = getFilteredDistance();
    
    Serial.print("[DATA_LOG] Obstacle Distance: ");
    Serial.print(currentDistance);
    Serial.println(" cm");
    
    // Decision making with safety thresholds
    if (currentDistance <= SAFE_DISTANCE_CM) {
        Serial.println("[ALERT] Obstacle detected! Initiating evasion maneuver.");
        
        // Stop briefly to stabilize hardware state
        stopRobot();
        delay(100);
        
        // Back up safely
        moveBackward();
        delay(REVERSE_TIME);
        
        // Turn to clear obstacle
        turnRight();
        delay(TURN_TIME);
        
        // Stop again before reassessing path
        stopRobot();
        delay(100);
    } else {
        // Path is clear, move forward continuously
        moveForward();
    }
    
    // Rate limiting to prevent CPU exhaustion and ensure stability
    delay(50);
}