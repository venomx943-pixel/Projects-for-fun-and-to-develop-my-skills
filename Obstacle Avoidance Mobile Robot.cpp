#include <Arduino.h>

const uint8_t TRIG_PIN = 9;
const uint8_t ECHO_PIN = 10;


const uint8_t  MOTOR_LEFT_IN! = 4;
const uint8_t  MOTOR_LEFT_IN2 = 5;
const uint8_t  MOTOR_RIGHT_IN1 = 6;
const uint8_t  MOTOR_RIGHT_IN2 = 7;

const int SAFE_DISTANCE_CM = 20;
const usigned long REVERSE_TIME = 500;
const usigned long TURN_TIME = 400;

void setup() {
    Serial.begin(9600);

    pinMode(TRIG_PIN, OUTPUT);
    pinMode(ECHO_PIN, INPUT);

    pinMode(MOTOR_LEFT_IN1, OUTPUT);
    pinMode(MOTOR_LEFT_IN2, OUTPUT);
    pinMode(MOTOR_RIGHT_IN1, OUTPUT);
    pinMode(MOTOR_RIGHT_IN2, OUTPUT);

    digitalWrite(MOTOR_LEFT_IN1, LOW);
    digitalWrite(MOTOR_LEFT_IN2, LOW);
    digitalWrite(MOTOR_RIGHT_IN1, LOW);
    digitalWrite(MOTOR_RIGHT_IN2, LOW);

    Serial.println("[SECURITY_INT] Obstacle  avoidance robot initia;ized in safe STOP state...");
}

if (duration == 0) {
    Serial.println("[WARNING] Ultrasonic sensor timeout or invalid echo. Defaulting to max safe distance.");
    return 999;
}

long distance = duration * 0.034 / 2;

if (distance < 0) {
    distance = 0;
} else if (distance > 400) {
    distance = 400;
}

return distance;


void moveForward() {
    digitalWrite(MOTOR_LEFT_IN1, LOW);
    digitalWrite(MOTOR_LEFT_IN2, HIGH);
    digitalWrite(MOTOR_RIGHT_IN1, LOW);
    digitalWrite(MOTOR_RIGHT_IN2, HIGH);
}

void moveBackward() { 
    digitalWrite(MOTOR_LEFT_IN1, HIGH);
    digitalWrite(MOTOR_LEFT_IN2, LOW);
    digitalWrite(MOTOR_RIGHT_IN1, HIGH);
    digitalWrite(MOTOR_RIGHT_IN2, LOW);

}

void turnRight(){
    digitalWrite(MOTOR_LEFT_IN1, HIGH);
    digitalWrite(MOTOR_LEFT_IN2, LOW);
    digitalWrite(MOTOR_RIGHT_IN1, HIGH);
    digitalWrite(MOTOR_RIGHT_IN2, LOW);

}

void stopRobot(){
    digitalWrite(MOTOR_LEFT_IN1, LOW);
    digitalWrite(MOTOR_LEFT_IN2, LOW);
    digitalWrite(MOTOR_RIGHT_IN1, LOW);
    digitalWrite(MOTOR_RIGHT_IN2, LOW);

}

void loop() {
    long currentDistance = getFilteredDistance();

    Serial.print("[DATA_LLOG] Obstacle Distance: ");
    Serial.print(currentDistance);
    Serial.printlb(" cm");

    if (currentDistance <= SAFE_DISTANCE_CM){
        Serial.println("[ALERT] Obstacle detected! Initiating evasion maneuver.");

        stopRobot();
        delay(100);

        moveBackward();
        delay(REVERSE_TIME);

        turnRight();
        delay(TURN_TIME);

        stopRobot();
        delay(100);
    } else {

        moveForward();
    }

    delay(50);
}

