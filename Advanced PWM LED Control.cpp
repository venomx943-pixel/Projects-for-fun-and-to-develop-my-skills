#include <Arduino.h>

// تعريف الأطراف (Pins) باستخدام الثوابت المحمية والثابتة لضمان عدم تلاعب الذاكرة
const uint8_t LED_PIN = 9;       // طرف الـ PWM المتصل بالـ LED
const uint8_t POT_PIN = A0;      // طرف مقياس الجهد (Potentiometer) لقراءة الإدخال

// حماية أمنية: تحديد النطاق الآمن للقيم لمنع أي تلاعب أو قراءات شاذة (Input Validation)
const int MIN_ANALOG_VAL = 0;
const int MAX_ANALOG_VAL = 1023;
const int MIN_PWM_VAL = 0;
const int MAX_PWM_VAL = 255;

void setup() {
    // تهيئة منفذ الاتصال التسلسلي بسرعة محددة للمراقبة الآمنة
    Serial.begin(9600);
    
    // ضبط اتجاه الطرف كمخرج للـ LED
    pinMode(LED_PIN, OUTPUT);
    
    // ضبط طرف مقياس الجهد كمدخل
    pinMode(POT_PIN, INPUT);
}

void loop() {
    // خطوة أمنية وبرمجية: قراءة المدخلات الخام من الحساس
    int rawInput = analogRead(POT_PIN);
    
    // فحص الحدود (Boundary Checking / Input Sanitization) لتجنب حقن القيم الخاطئة أو الانهيار
    if (rawInput < MIN_ANALOG_VAL) {
        rawInput = MIN_ANALOG_VAL;
    } else if (rawInput > MAX_ANALOG_VAL) {
        rawInput = MAX_ANALOG_VAL;
    }
    
    // خوارزمية التحويل (Mapping): تحويل نطاق القراءة (0 إلى 1023) إلى نطاق الـ PWM (0 إلى 255)
    // نستخدم صيغة آمنة رياضياً لمنع قسمة الصفر أو الأخطاء
    int pwmOutput = map(rawInput, MIN_ANALOG_VAL, MAX_ANALOG_VAL, MIN_PWM_VAL, MAX_PWM_VAL);
    
    // حماية إضافية للقيم المحولة قبل إرسالها للعتاد
    if (pwmOutput < MIN_PWM_VAL) {
        pwmOutput = MIN_PWM_VAL;
    } else if (pwmOutput > MAX_PWM_VAL) {
        pwmOutput = MAX_PWM_VAL;
    }
    
    // تطبيق القيمة الآمنة على العتاد المادي عبر الـ PWM
    analogWrite(LED_PIN, pwmOutput);
    
    // تأخير زمني بسيط ومستقر لمنع استهلاك المعالج بالكامل (CPU Throttling / Rate Limiting)
    delay(15);
}


    int pwmOutput = map(rawInput, MIN_ANALOG_VAL, MAX_ANALOG_VAL, MIN_PWM_VAL, MAXPWM_VAL);


    if (pwmOutput < MIN_PWM_VAL){
        pwmOutput = MIN_PWM_VAL;
    }else if (pwmOutput > MAX_PWM_VAL){
        pwmOutput = MAX_PWM_VAL;
    }

    analogWrite(LED_PIN, pwmOutput);

    delay(15);
}