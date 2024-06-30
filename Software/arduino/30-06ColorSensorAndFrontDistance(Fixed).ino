#include <cdcacm.h>
#include <usbhub.h>
#include "pgmstrings.h"
#ifdef dobogusinclude
#include <spi4teensy3.h>
#endif
#include <SPI.h>
#include <HCSR04.h>
#include <Servo.h>

// UTF-8 support
#include <avr/pgmspace.h>
#include <stdlib.h>

#include "Adafruit_APDS9960.h"

Adafruit_APDS9960 apds;
uint16_t r, g ,b ,c;

class ACMAsyncOper : public CDCAsyncOper
{
public:
    uint8_t OnInit(ACM *pacm);
};

uint8_t ACMAsyncOper::OnInit(ACM *pacm)
{
    uint8_t rcode;
    // Set DTR = 1 RTS=1
    rcode = pacm->SetControlLineState(3);

    if (rcode)
    {
        ErrorMessage<uint8_t>(PSTR("SetControlLineState"), rcode);
        return rcode;
    }

    LINE_CODING lc;
    lc.dwDTERate = 115200;
    lc.bCharFormat = 0;
    lc.bParityType = 0;
    lc.bDataBits = 8;

    rcode = pacm->SetLineCoding(&lc);

    if (rcode)
        ErrorMessage<uint8_t>(PSTR("SetLineCoding"), rcode);

    return rcode;
}

USB Usb;
ACMAsyncOper AsyncOper;
ACM Acm(&Usb, &AsyncOper);
bool data_send = false;
String buffer = "";
bool insideMarkers = false;
bool outsideMarkers = false;


const int switchPin = 17; // Pin connected to the switch
bool lastSwitchState = HIGH; // Previous state of the switch
bool currentSwitchState;

unsigned long previousMillis = 0; // will store last time the task was done
const long interval = 300; // interval at which to perform the task (milliseconds)
long tlighthigh = 100 ;
long tlightlow = 1000;
long previosMillislight;
bool  currentlightON = false;

signed pinLifts = 3;
signed PinSelector = 9;
signed PinDeposit = 6;
signed PinRight = 5;
signed PinLeft = 10;

Servo lift_servo;
Servo deposit_servo;
Servo right_claw;
Servo left_claw;
Servo selector_servo;

//Servo Values
int LIFT_SERVO_NORMAL = 44;
int LIFT_SERVO_READBALL = 45;
int LIFT_SERVO_LINE = 60;
int LIFT_SERVO_RAMP = 70;
int LIFT_SERVO_UPPER = 145;

int RIGHT_CLOSE = 38; // Si baja cierra más.
int LEFT_CLOSE = 164; // Si aumenta cierra más.
int RIGHT_OPEN = 100; // Si se sube ...
int LEFT_OPEN = 109; // Si se sube cierra más.

int LEFT_MORE_OPEN = 80;
int RIGHT_MORE_OPEN = 130;

int LEFT_LESS_OPEN = 135;
int RIGHT_LESS_OPEN = 70;

int SELECTOR_LEFT = 30;
int SELECTOR_RIGHT = 130;
int SELECTOR_SPECIAL_RIGHT = 80;
int SELECTOR_SPECIAL_LEFT = 80;

int DEPOSIT_DEFAULT = 150;
int DEPOSIT_LEFT = 130;
int DEPOSIT_RIGHT = 170;

byte triggerPin = 16;
byte echoCount = 3;
byte* echoPins = new byte[echoCount] { 15, 8, 7 };
byte lightpin = 1; // esto hay que reemplazar por el pin de encendido de luz

void setup() {
    Serial.begin(115200);
    HCSR04.begin(triggerPin, echoPins, echoCount);

    if (Usb.Init() == -1) {
        //Serial.println("OSCOKIRQ failed to assert");
    }

    if (!apds.begin()) {
        // Serial.println("Failed to init device! check wiring.");
    } else {
        // Serial.println("Device init!");
        apds.enableColor(true);
    }

    lift_servo.attach(pinLifts);
    selector_servo.attach(PinSelector);
    deposit_servo.attach(PinDeposit);
    right_claw.attach(PinRight);
    left_claw.attach(PinLeft);

    LMessage();
    deposit_servo.write(DEPOSIT_DEFAULT);

    pinMode(switchPin, INPUT_PULLUP);
    pinMode(lightpin, OUTPUT);
    digitalWrite(lightpin, LOW);  //switch light off

    while (digitalRead(switchPin) == LOW) {
        Tilight();
    }
    
    delay(200);
}

void delay_switch(int espera) {
    int current_time = millis();

    while (millis() - current_time < espera && currentSwitchState == HIGH && currentSwitchState == lastSwitchState) {
        currentSwitchState = digitalRead(switchPin);
    }
}

void wait_for_spike() {
    static bool current_light_ON = false;
    static unsigned long previos_Millis_light = 0;
    const unsigned long t_light_high = 200;
    const unsigned long t_light_low = 200;

    unsigned long current_Millis = millis();

    if (current_light_ON && (current_Millis - previos_Millis_light > t_light_high)) {
        digitalWrite(lightpin, LOW);
        current_light_ON = false;
        previos_Millis_light = current_Millis;
    } else if (!current_light_ON && (current_Millis - previos_Millis_light > t_light_low)) {
        digitalWrite(lightpin, HIGH);
        current_light_ON = true;
        previos_Millis_light = current_Millis;
    }
}

bool currentlight_ON = false;
unsigned long previosMillis_light = 0; // save the previous ms value
const unsigned long tlight_high = 1000; // 100 ms on
const unsigned long tlight_low = 1000;  // 100 ms off
void Tilight() {
    unsigned long current_Millis = millis();
    if (currentlight_ON && (current_Millis - previosMillislight > tlighthigh)) {
        digitalWrite(lightpin, LOW);
        currentlight_ON = false;
        previosMillislight = current_Millis;
    } else if (!currentlight_ON && (current_Millis - previosMillislight > tlightlow)) {
        digitalWrite(lightpin, HIGH);
        currentlight_ON = true;
        previosMillislight = current_Millis;
    }
}

void read_data_color() {
    while (!apds.colorDataReady()) {
        delay_switch(5);
    }
    apds.getColorData(&r, &g, &b, &c);
    Serial.println("R: " + String(r) + " G: " + String(g) + " B: " + String(b));
}

uint8_t getRawValueColor(uint16_t color) {
    int mapped_value = map(color, 0, 400, 0, 240);
    mapped_value = constrain(mapped_value, 0, 240);
    return (uint8_t)mapped_value;
}

// ---------- SERVOS ----------
void DMessage() {
    lift_servo.write(LIFT_SERVO_UPPER);
    delay_switch(2000);
    right_claw.write(RIGHT_LESS_OPEN);
    left_claw.write(LEFT_LESS_OPEN);
    selector_servo.write(SELECTOR_LEFT);
    delay_switch(2000);
    selector_servo.write(SELECTOR_SPECIAL_LEFT);
}

void EMessage() {
    lift_servo.write(LIFT_SERVO_UPPER);
    delay_switch(2000);
    right_claw.write(RIGHT_LESS_OPEN);
    left_claw.write(LEFT_LESS_OPEN);
    selector_servo.write(SELECTOR_RIGHT);
    delay_switch(2000);
    selector_servo.write(SELECTOR_SPECIAL_RIGHT);
}

void FMessage() {
    delay_switch(1000);
    deposit_servo.write(DEPOSIT_LEFT);
    delay_switch(6000);
}

void GMessage() {
    delay_switch(1000);
    deposit_servo.write(DEPOSIT_RIGHT);
    delay_switch(6000);
}

void MMessage() {
    lift_servo.write(LIFT_SERVO_RAMP);
    right_claw.write(RIGHT_CLOSE);
    left_claw.write(LEFT_CLOSE);
}

void RMessage() {
    lift_servo.write(LIFT_SERVO_NORMAL);
    right_claw.write(RIGHT_OPEN);
    left_claw.write(LEFT_OPEN);
}

void LMessage() {
    lift_servo.write(LIFT_SERVO_LINE);
    right_claw.write(RIGHT_MORE_OPEN);
    left_claw.write(LEFT_MORE_OPEN);
}

void AMessage() {
    lift_servo.write(LIFT_SERVO_READBALL);
    right_claw.write(RIGHT_CLOSE);
    left_claw.write(LEFT_CLOSE);
    delay_switch(2000);
}

void PMessage() {
    lift_servo.write(LIFT_SERVO_NORMAL);
    right_claw.write(RIGHT_CLOSE);
    left_claw.write(LEFT_CLOSE);
}

void LyOMessage() {
    lift_servo.write(LIFT_SERVO_LINE);
    right_claw.write(RIGHT_MORE_OPEN);
    left_claw.write(LEFT_MORE_OPEN);
}

void ButtonSwitchServos() {
    lift_servo.write(LIFT_SERVO_NORMAL);
    right_claw.write(RIGHT_OPEN);
    left_claw.write(LEFT_OPEN);
}

String mode = "line";

void loop() {
    read_data_color();
    Usb.Task();

    currentSwitchState = digitalRead(switchPin);

    if (Acm.isReady()) {
        unsigned long currentMillis = millis();
        uint8_t rcode;

        if (mode == "rescue" && currentMillis - previousMillis >= interval && currentSwitchState == HIGH) {
            previousMillis = currentMillis;

            // Enviar datos de color
            uint8_t rawValue = 253;
            rcode = Acm.SndData(1, &rawValue);
            if (rcode) {
                ErrorMessage<uint8_t>(PSTR("SndData"), rcode);
            }
            rawValue = getRawValueColor(r);
            rcode = Acm.SndData(1, &rawValue);
            if (rcode) {
                ErrorMessage<uint8_t>(PSTR("SndData"), rcode);
            }

            rawValue = 252;
            rcode = Acm.SndData(1, &rawValue);
            if (rcode) {
                ErrorMessage<uint8_t>(PSTR("SndData"), rcode);
            }
            rawValue = getRawValueColor(g);
            rcode = Acm.SndData(1, &rawValue);
            if (rcode) {
                ErrorMessage<uint8_t>(PSTR("SndData"), rcode);
            }

            rawValue = 251;
            rcode = Acm.SndData(1, &rawValue);
            if (rcode) {
                ErrorMessage<uint8_t>(PSTR("SndData"), rcode);
            }
            rawValue = getRawValueColor(b);
            rcode = Acm.SndData(1, &rawValue);
            if (rcode) {
                ErrorMessage<uint8_t>(PSTR("SndData"), rcode);
            }
        }

        // Recibir datos de LEGO
        uint8_t buf[1024];
        uint16_t rcvd = 1024;
        rcode = Acm.RcvData(&rcvd, buf);
        if (rcode && rcode != hrNAK) {
            ErrorMessage<uint8_t>(PSTR("Ret"), rcode);
        }

        if (rcvd) {
            for (uint16_t i = 0; i < rcvd; i++) {
                char data = (char)buf[i];
                char datanext = (char)buf[i + 1];
                if (data == '<' && datanext == '<') {
                    buffer = "<<";
                    insideMarkers = true;
                } else if (insideMarkers && data != '>' && data != '<') {
                    buffer += data;
                } else if (data == '>' && datanext == '>' && insideMarkers) {
                    buffer += ">>";
                    if (buffer == "<<R>>") {
                        RMessage();
                        mode = "rescue";
                    }
                    if (buffer == "<<O>>") {
                        LyOMessage();
                        mode = "line";
                    }
                    if (buffer == "<<S>>") {
                        bool confirm_stop = true;
                    }
                    if (buffer == "<<L>>") {
                        LyOMessage();
                    }
                    if (buffer == "<<M>>") {
                        MMessage();
                    }
                    if (buffer == "<<P>>") {
                        PMessage();
                    }
                    if (buffer == "<<A>>") {
                        while (currentSwitchState == HIGH) {
                            AMessage();
                        }
                    }
                    if (buffer == "<<D>>") {
                        DMessage();
                        delay(2000);
                    }
                    if (buffer == "<<E>>") {
                        EMessage();
                    }
                    if (buffer == "<<F>>") {
                        FMessage();
                    }
                    if (buffer == "<<G>>") {
                        GMessage();
                    }
                    insideMarkers = false;
                    buffer = "";
                }
            }
        }

        // Detectar cambio de estado en el interruptor
        if (currentSwitchState != lastSwitchState) {
            currentSwitchState = digitalRead(switchPin);
            if (currentSwitchState != lastSwitchState) {
                lastSwitchState = currentSwitchState;
                if (currentSwitchState == LOW) {
                    uint8_t rawValue = 255;
                    rcode = Acm.SndData(1, &rawValue);
                    ButtonSwitchServos();
                    if (rcode) {
                        ErrorMessage<uint8_t>(PSTR("SndData"), rcode);
                    }
                    currentlightON = false;
                    delay(2000);
                } else {
                    uint8_t rawValue = 254;
                    rcode = Acm.SndData(1, &rawValue);
                    if (rcode) {
                        ErrorMessage<uint8_t>(PSTR("SndData"), rcode);
                    }
                    delay(2000);
                }
            }
        }

        // Gestionar el comportamiento de la luz frontal
        if (currentSwitchState == LOW) {
            if (currentlight_ON && (currentMillis - previosMillislight > tlighthigh)) {
                digitalWrite(lightpin, LOW);
                currentlight_ON = false;
                previosMillislight = currentMillis;
            } else if (!currentlight_ON && (currentMillis - previosMillislight > tlightlow)) {
                digitalWrite(lightpin, HIGH);
                currentlight_ON = true;
                previosMillislight = currentMillis;
            }
        } else {
            digitalWrite(lightpin, LOW);
        }

        // Modo línea solo envía datos del sensor ultrasónico frontal
        if (mode == "line" && currentMillis - previousMillis >= interval && currentSwitchState == HIGH) {
            previousMillis = currentMillis;
            double* distances = HCSR04.measureDistanceCm();
            int front_sensor = distances[0];

            if (front_sensor != -1) {
                int mapped_value = map(front_sensor, 0, 400, 0, 240);
                mapped_value = constrain(mapped_value, 0, 240);
                uint8_t rawValue = (uint8_t)mapped_value;
                rcode = Acm.SndData(1, &rawValue);
            }
        }
    }
}
