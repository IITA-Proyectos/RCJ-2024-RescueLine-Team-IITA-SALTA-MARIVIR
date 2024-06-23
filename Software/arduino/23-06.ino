#include <Servo.h>
#include <HCSR04.h>
#include "Adafruit_APDS9960.h"
Adafruit_APDS9960 apds;

byte triggerPin = 16;
byte echoCount = 3;
byte *echoPins = new byte[echoCount]{15, 8, 7};

Servo lift_servo;
Servo deposit_servo;
Servo right_claw;
Servo left_claw;
Servo selector_servo;

//debug
bool debug = true;
bool servos_debug = false;
bool apds_debug = true;
bool ultrasonic_debug = false;

// Universal Values
// Pins
signed PinLed = 1;
signed pinLifts = 3;
signed PinSelector = 9;
signed PinDeposit = 6;
signed PinRight = 5;
signed PinLeft = 10;

// Mode
String Mode = "RESCUE"; // LINE | RESCUE
String SubMode = "RAMP"; // LINE: PALA NORMAL | RAMP: PALA CERRADA Y ARRIBA 
//Servos Values
int LIFT_SERVO_NORMAL = 44;
int LIFT_SERVO_READBALL = 45;
int LIFT_SERVO_LINE = 70;
int LIFT_SERVO_RAMP = 70;
int RIGHT_CLOSE = 38; // Si baja cierra más.
int LEFT_CLOSE = 162; // Si aumenta cierra más.
int RIGHT_OPEN = 100; // Si se sube ...
int LEFT_OPEN = 109; // Si se sube cierra más.

void setup() {
    pinMode(PinLed, OUTPUT);
    HCSR04.begin(triggerPin, echoPins, echoCount);
    lift_servo.attach(pinLifts);
    selector_servo.attach(PinSelector);
    deposit_servo.attach(PinDeposit);
    right_claw.attach(PinRight);
    left_claw.attach(PinLeft);

    ServoSetup();
    APDS9960Setup();


    if (debug == true) {
      Serial.begin(115200);
      while (!Serial);
    }  
}

void debugPrint(String message) {
  if (debug == true) {

    Serial.print(message);
  }
}

void debugPrintln(String message) {
  if (debug == true) {
    Serial.println(message);
  }
}

void APDS9960Setup() {
  if(!apds.begin()) {
    debugPrintln("[ERROR] Failed to initialize APDS9960.");
  } else debugPrintln("Device initialized!");

  apds.enableColor(true);
}

void APPDS9960() {
  uint16_t r, g, b, c;

  while(!apds.colorDataReady()) {
    delay(5);
  }

  apds.getColorData(&r, &g, &b, &c);

  if (apds_debug == true) {
    Serial.print("red: ");
    Serial.println(r);

    Serial.print("green: ");
    Serial.println(g);

    Serial.print("blue: ");
    Serial.println(b);

    Serial.println("---");

    delay(500);
  }
  
}

void ServoSetup() {
  if (Mode == "LINE") {    
    lift_servo.write(LIFT_SERVO_LINE);
    right_claw.write(RIGHT_OPEN);
    left_claw.write(LEFT_OPEN);

  } else if (Mode == "RESCUE") {
    lift_servo.write(LIFT_SERVO_NORMAL);
    right_claw.write(RIGHT_OPEN);
    left_claw.write(LEFT_OPEN);
  }
}

void ServosDebug() {
  if (servos_debug == true) {
    lift_servo.write(LIFT_SERVO_LINE);
    right_claw.write(RIGHT_OPEN);
    left_claw.write(LEFT_OPEN);

  }
}


void HCSR04Setup() {
  double* distances = HCSR04.measureDistanceCm();
  if (Mode == "LINE") {
    int front_sensor = distances[0];

    if (ultrasonic_debug == true) {
      debugPrintln("Front: " + String(front_sensor) + "cm");

      debugPrintln("---");
    }

    delay(2000);
  }
  if (Mode == "RESCUE") {
    int front_sensor = distances[0];
    int right_sensor = distances[1];
    int left_sensor = distances[2];

    if (ultrasonic_debug == true) {      
      debugPrintln("Front: " + String(front_sensor) + "cm");
      debugPrintln("Right: " + String(right_sensor) + "cm");
      debugPrintln("Left: " + String(left_sensor) + "cm");

      debugPrintln("---");
    }
    delay(2000);
  }
}
void LedSetup() {
    if (Mode == "LINE") {
        digitalWrite(PinLed, LOW);
    } else if (Mode == "RESCUE") {
        digitalWrite(PinLed, HIGH);
    }   
}

void loop() {
    LedSetup();
    //HCSR04Setup();
    //ServosDebug();
    APPDS9960();

    delay(3000); 
    AMessage();
}

// Communication Uses

void OMessage() {
  //Recibe mensaje O
  Mode = "LINE";
  if (Mode == "LINE") {
    lift_servo.write(LIFT_SERVO_LINE);
    right_claw.write(0);
    left_claw.write(0);
  }
}
void RMessage() {
  Mode = "RESCUE";

  if (Mode == "RESCUE") {
    lift_servo.write(LIFT_SERVO_NORMAL);
    right_claw.write(RIGHT_OPEN);
    left_claw.write(LEFT_OPEN);
  }
}

void LMessage() {
  SubMode = "LINE";
  if (Mode && SubMode == "LINE") {
    lift_servo.write(LIFT_SERVO_LINE);
  } 
}

void MMessage() {
  SubMode = "RAMP";
  if (Mode == "LINE" && SubMode == "RAMP") {
    lift_servo.write(LIFT_SERVO_RAMP);
    right_claw.write(RIGHT_CLOSE);
    left_claw.write(LEFT_CLOSE);
  }
}

void AMessage() {
  if (Mode == "RESCUE") {
    lift_servo.write(LIFT_SERVO_READBALL);
    right_claw.write(RIGHT_CLOSE);
    left_claw.write(LEFT_CLOSE);
  }
}
