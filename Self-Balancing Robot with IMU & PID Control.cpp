#include <Arduino.h>
#include <Wire.h>
#include <MPU6050.h>

// Initialize MPU6050 IMU sensor object
MPU6050 mpu;

// Motor Driver Pins (e.g., L298N)
const uint8_t ENA_PIN = 3;
const uint8_t IN1_PIN = 4;
const uint8_t IN2_PIN = 5;
const uint8_t IN3_PIN = 6;
const uint8_t IN4_PIN = 7;
const uint8_t ENB_PIN = 9;

// PID Controller Constants (Tuned for balance)
const float Kp = 20.0; // Proportional gain
const float Ki = 0.5;  // Integral gain
const float Kd = 1.0;  // Derivative gain

// PID state variables
float error = 0;
float lastError = 0;
float integral = 0;
float derivative = 0;
const float TARGET_ANGLE = 0.0; // Desired upright balance angle

// Non-blocking timing and rate limiting for the control loop
const unsigned long SAMPLE_TIME_MS = 10; // 10ms loop period (100Hz frequency)
unsigned long lastTime = 0;

void setup() {
    // Initialize serial communication for security and system logs
    Serial.begin(9600);
    Wire.begin();
    
    // Initialize IMU sensor
    mpu.initialize();

    // Configure motor control pins as outputs
    pinMode(ENA_PIN, OUTPUT);
    pinMode(IN1_PIN, OUTPUT);
    pinMode(IN2_PIN, OUTPUT);
    pinMode(IN3_PIN, OUTPUT);
    pinMode(IN4_PIN, OUTPUT);
    pinMode(ENB_PIN, OUTPUT);

    // Fail-safe default: Ensure motors start in a safe STOP state upon boot
    analogWrite(ENA_PIN, 0);
    analogWrite(ENB_PIN, 0);
    digitalWrite(IN1_PIN, LOW);
    digitalWrite(IN2_PIN, LOW);
    digitalWrite(IN3_PIN, LOW);
    digitalWrite(IN4_PIN, LOW);

    // Verify hardware connection securely
    if (!mpu.testConnection()) {
        Serial.println("[SECURITY_ALERT] MPU6050 connection failed! Hardware fault detected.");
    } else {
        Serial.println("[SECURITY_INIT] MPU6050 initialized successfully. Self-balancing loop ready.");
    }
}

// Safe motor control function with PWM bounds checking (Clamping)
void controlMotors(int speed, bool forward) {
    // PWM bounds sanitization to prevent overflows
    if (speed < 0) speed = 0;
    if (speed > 255) speed = 255;

    // Set directions safely for both motors simultaneously
    digitalWrite(IN1_PIN, forward ? HIGH : LOW);
    digitalWrite(IN2_PIN, forward ? LOW : HIGH);
    digitalWrite(IN3_PIN, forward ? HIGH : LOW);
    digitalWrite(IN4_PIN, forward ? LOW : HIGH);

    // Apply PWM speed signals to enable pins
    analogWrite(ENA_PIN, speed);
    analogWrite(ENB_PIN, speed);
}

void loop() {
    unsigned long currentTime = millis();
    
    // Rate limiting: Execute PID control loop strictly every 10ms for mathematical stability
    if (currentTime - lastTime >= SAMPLE_TIME_MS) {
        lastTime = currentTime;

        // Read raw accelerometer and gyro data from IMU
        int16_t ax, ay, az;
        mpu.getAcceleration(&ax, &ay, &az);

        // Input sanitization and error check for sensor failure / fault injection
        if (ax == 0 && ay == 0 && az == 0) {
            Serial.println("[ERROR] IMU data fault injection or disconnection. Executing fail-safe stop.");
            controlMotors(0, true);
            return;
        }

        // Calculate pitch tilt angle from accelerometer values using trigonometry
        float currentAngle = atan2(ay, az) * 180.0 / PI;

        // Input bounds clamping for safety
        if (currentAngle < -90.0) currentAngle = -90.0;
        if (currentAngle > 90.0) currentAngle = 90.0;

        // PID Algorithm calculation
        error = TARGET_ANGLE - currentAngle;
        integral += error;

        // Anti-windup protection: Clamp integral term to prevent runaway values
        if (integral > 400) integral = 400;
        if (integral < -400) integral = -400;

        derivative = error - lastError;
        float output = (Kp * error) + (Ki * integral) + (Kd * derivative);
        lastError = error;

        // Determine direction and speed based on PID controller output
        bool moveForward = (output >= 0);
        int motorSpeed = (int)abs(output);

        // Apply motor control with safety clamping
        controlMotors(motorSpeed, moveForward);

        // Log telemetry for debugging and security monitoring
        Serial.print("[DATA_LOG] Angle: ");
        Serial.print(currentAngle);
        Serial.print(" | PID Output: ");
        Serial.println(output);
    }
}