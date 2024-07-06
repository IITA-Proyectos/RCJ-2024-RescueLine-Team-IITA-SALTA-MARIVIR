#include <cdcacm.h>
#include <usbhub.h>
#include "pgmstrings.h"
#include <SPI.h>
#include "Adafruit_APDS9960.h"
#include <HCSR04.h>

byte triggerPin = 16;
byte echoCount = 3;
byte* echoPins = new byte[echoCount] { 15, 8, 7 };
const int switchPin = 17;

//int lightpin = 50 ; // despues hay que volver a 1 esto es para que ande puerto serie
int lightpin = 1;

#include <Servo.h>

// UTF-8 support
#include <avr/pgmspace.h>
#include <stdlib.h>

Adafruit_APDS9960 apds;
uint16_t r, g, b, c;

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
bool usb_initialized = false;
String buffer = "";
bool insideMarkers = false;
bool outsideMarkers = false;

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
int LIFT_SERVO_NORMAL = 49; // 44
int LIFT_SERVO_READBALL = 55;// 45
int LIFT_SERVO_LINE = 60;
int LIFT_SERVO_RAMP = 70;
int LIFT_SERVO_UPPER = 145; // 145

int RIGHT_CLOSE = 54; // 38 Si baja cierra más.
int LEFT_CLOSE = 151; // 164 Si aumenta cierra más.
int RIGHT_OPEN = 100; // 100 Si se sube abre ...
int LEFT_OPEN = 109; //  109 Si se baja abre más.

int RIGHT_MORE_OPEN = 85; //80
int LEFT_MORE_OPEN = 125;  //130

int RIGHT_LESS_OPEN = 75;  //70 es la posicion donde tiene que caer pelota arriba
int LEFT_LESS_OPEN = 130;    //135

int SELECTOR_LEFT = 30;
int SELECTOR_RIGHT = 130; 
int SELECTOR_SPECIAL_RIGHT = 80; 
int SELECTOR_SPECIAL_LEFT = 80;

int DEPOSIT_DEFAULT = 150;
int DEPOSIT_LEFT = 130; 
int DEPOSIT_RIGHT = 170;

void servos_default() {
  lift_servo.write(LIFT_SERVO_NORMAL);
  right_claw.write(RIGHT_OPEN);
  left_claw.write(LEFT_OPEN);
  deposit_servo.write(DEPOSIT_DEFAULT);
  selector_servo.write(SELECTOR_LEFT);
}

void setup()
{
    pinMode(switchPin, INPUT_PULLUP);
    pinMode(lightpin, OUTPUT);
    // digitalWrite(lightpin, LOW);  //switch light off
    //delay(3000);

    //Serial.begin(115200);
    HCSR04.begin(triggerPin, echoPins, echoCount);
    
    if (Usb.Init() == -1) {

    } else {
        // Serial.println("OSCOK IRQ failed to assert");
        usb_initialized = true;
      //  Serial.println("Device initialized! conexion spike");
    delay(200);
    }

    if (!apds.begin())
    {
        // Serial.println("failed to initialize device! Please check your wiring.");
    }
    else
    {
        //Serial.println("conexion color sensor ok");
        apds.enableColor(true);
    }

    
    lift_servo.attach(pinLifts);
    selector_servo.attach(PinSelector);
    deposit_servo.attach(PinDeposit);
    right_claw.attach(PinRight);
    left_claw.attach(PinLeft);


    servos_default();
    /*
    delay(100000);
    LMessage();  /// linea
    delay(10000);
    RMessage();  /// rescate
    delay(10000);
    AMessage();  /// agarrar y dejar nivel luz
    delay(10000);
    
    DMessage(); // sube derecha
    delay(100000);
    */
}

// global long int current_time1 = millis();


// void delay_switch(int espera) {
//   global long int current_time1;
//   current_time1 = millis(); 
//   while (millis() - current_time1 < espera && currentSwitchState == HIGH && currentSwitchState == lastSwitchState)
//   {
//      currentSwitchState = digitalRead(switchPin);
     
//   }
// }



void read_data_color()
{
    while (!apds.colorDataReady())
    {
        delay(5);
    }
    apds.getColorData(&r, &g, &b, &c);
}

uint8_t getRawValueColor(uint16_t color) {
    // Map the r value to the range 0-240
    int mapped_value = map(color, 0, 1024, 0, 240);

    // Constrain the value to be between 0 and 240
    mapped_value = constrain(mapped_value, 0, 240);

    // Prepare the byte to send
    byte byte_to_send = (byte)mapped_value;

    // Return the rawValue
    uint8_t rawValue = byte_to_send;
    return rawValue;
}

uint8_t getRawValueUltrasound(int ultrasound) {
  // Map the r value to the range 0-240
  int mapped_value = map(ultrasound, 0,250 , 0, 240); // Supose max read from sensor is 400cm

  // Constrain the value to be between 0 and 240
  mapped_value = constrain(mapped_value, 0, 240);

  if (mapped_value == 0)
        mapped_value = 240;

  // Prepare the byte to send
  byte byte_to_send = (byte)mapped_value;

  // Return the rawValue
  uint8_t rawValue = byte_to_send;
  return rawValue;
 }

/////////////////////////////// inicio servos
// ---------- SERVOS ----------

void DMessage() { //Go up to left way.
  lift_servo.write(LIFT_SERVO_UPPER);

  delay(2000);

  right_claw.write(RIGHT_LESS_OPEN);
  left_claw.write(LEFT_LESS_OPEN);
  
   selector_servo.write(SELECTOR_LEFT);
  
   delay(2000);

   selector_servo.write(SELECTOR_SPECIAL_LEFT); 

   lift_servo.write(LIFT_SERVO_NORMAL);
   right_claw.write(RIGHT_OPEN);
   left_claw.write(LEFT_OPEN);
 
}


void EMessage() { // Gop up to right way.
  
  lift_servo.write(LIFT_SERVO_UPPER);
  
  delay(2000);

  right_claw.write(RIGHT_LESS_OPEN);
  left_claw.write(LEFT_LESS_OPEN);
  selector_servo.write(SELECTOR_RIGHT);

//  delay_switch(2000);
  
//  selector_servo.write(SELECTOR_SPECIAL_RIGHT);
}


void FMessage() { // Left deposit
//  delay_switch(1000);

  deposit_servo.write(DEPOSIT_LEFT);
//  delay_switch(6000);

}

void GMessage() { // Right deposit
//  delay_switch(1000);

  deposit_servo.write(DEPOSIT_RIGHT);
//  delay_switch(6000);

}

void MMessage() { // Ramp Mode 
  lift_servo.write(LIFT_SERVO_RAMP);
  right_claw.write(RIGHT_CLOSE);
  left_claw.write(LEFT_CLOSE);
}

void RMessage() {
  // digitalWrite(lightpin, HIGH);
  lift_servo.write(LIFT_SERVO_NORMAL);
  right_claw.write(RIGHT_OPEN);
  left_claw.write(LEFT_OPEN);
}

void LMessage() {
  // // digitalWrite(lightpin, LOW);
  // lift_servo.write(LIFT_SERVO_LINE);
  // right_claw.write(RIGHT_MORE_OPEN);
  // left_claw.write(LEFT_MORE_OPEN);
  lift_servo.write(LIFT_SERVO_UPPER);
  
  right_claw.write(RIGHT_LESS_OPEN);
  left_claw.write(LEFT_LESS_OPEN);
}




void AMessage() {  
  lift_servo.write(LIFT_SERVO_READBALL);
  right_claw.write(RIGHT_CLOSE);
  left_claw.write(LEFT_CLOSE);

//  delay_switch(2000);
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


////////////////////////fin servos
String modo = "line";
//String modo = "rescue";
unsigned long previousMillis = 0; // will store last time the task was done
const long interval = 800;

void loop()
{
    Usb.Task();
       // Serial.println("USB TASK");
  
    if (Acm.isReady())
    {
        //Serial.println("acn is ready USB TASK");
        unsigned long currentMillis = millis();
        uint8_t rcode;

        if (modo == "rescue" && (currentMillis - previousMillis) >= interval)
        {
            previousMillis = currentMillis;
            uint8_t rawValue;
            double* distances = HCSR04.measureDistanceCm();
            int front_sensor = distances[0];
            int right_sensor = distances[1];
            int left_sensor = distances[2];
            uint8_t rawFrontUltraValue = getRawValueUltrasound(front_sensor);
            uint8_t rawRightUltraValue = getRawValueUltrasound(right_sensor);
            uint8_t rawLeftUltraValue = getRawValueUltrasound(left_sensor);

            read_data_color();
            uint8_t rawRedValue = getRawValueColor(r); // Color R_value
            uint8_t rawGreenValue = getRawValueColor(g); // Color G_value
            uint8_t rawBlueValue = getRawValueColor(b);
            
            // Send reference data for R value
            rawValue = 253; // Reference data color R_value
            rcode = Acm.SndData(1, &rawValue);
            rcode = Acm.SndData(1, &rawRedValue);
            //  Serial.print("R: " + String(rawRedValue));
            
            // Send reference data for G value
            rawValue = 252; // Reference data color G_value
            rcode = Acm.SndData(1, &rawValue);
            rcode = Acm.SndData(1, &rawGreenValue);
            //Serial.print(" G:" + String(rawGreenValue));

            // Send reference data for B value
            rawValue = 251; // Reference data color B_value
            rcode = Acm.SndData(1, &rawValue);
            rcode = Acm.SndData(1, &rawBlueValue);
            // Serial.println(" B:" + String(rawBlueValue));

            rawValue = 248; // 248 Mean next value to send is a front_sensor_color
            rcode = Acm.SndData(1, &rawValue);;
            rcode = Acm.SndData(1, &rawFrontUltraValue);
            // Serial.print("UF:" + String(rawFrontUltraValue));
          
            rawValue = 249; // 249 Mean next value to send is a right_sensor_color
            rcode = Acm.SndData(1, &rawValue);
            rcode = Acm.SndData(1, &rawRightUltraValue);
            // Serial.print(" UD:" + String(rawRightUltraValue));
        
            rawValue = 250; // 250 Mean next value to send is a left_sensor_color
            rcode = Acm.SndData(1, &rawValue);
            rcode = Acm.SndData(1, &rawLeftUltraValue);
            // Serial.println(" UI:" + String(rawLeftUltraValue));

            // Serial.println("-- Data sent to LEGO --");
        } 
           
        if (modo == "line" && (currentMillis - previousMillis) >= interval)
        {
            previousMillis = currentMillis;
            uint8_t rawValue;
            double* distances = HCSR04.measureDistanceCm();
            int front_sensor = distances[0];
            //int right_sensor = distances[1];
            //int left_sensor = distances[2];
            uint8_t rawFrontUltraValue = getRawValueUltrasound(front_sensor);                                                       
            rcode = Acm.SndData(1, &rawFrontUltraValue);

        //     Serial.println("-- Data sent to LEGO --");
            
        //    Serial.println(" UI:" + String(rawFrontUltraValue));

        //    Serial.println("-- Data sent to LEGO --");
        } 
        
        uint8_t buf[512];
        uint16_t rcvd = 512;
        rcode = Acm.RcvData(&rcvd, buf);
        if (rcode && rcode != hrNAK)
            ErrorMessage<uint8_t>(PSTR("Ret"), rcode);
        if (rcvd) { // More than zero bytes received
          for (uint16_t i = 0; i < rcvd; i++) {
            char data = (char)buf[i];
            char datanext = (char)buf[i];
            //Serial.print(data);
            if (data == '<' && datanext == '<'){
              // Serial.println("Encontre <");
              buffer = "<<";
              insideMarkers = true;
            }
            if (insideMarkers && data !='>' && data !='<'){
              buffer += data;
            }
            if (data == '>' && datanext == '>' && insideMarkers){ 
              buffer += ">>";
              // Serial.println("Buffer: " + buffer);
                 
              if(buffer == "<<R>>") {  // Receive data: put mode --> rescue
                  // Serial.println("Data received: R");
                  RMessage();
                  modo = "rescue";
                  digitalWrite(1, HIGH);
              }
              if (buffer == "<<O>>") { // Receive data: put mode --> line
                  // Serial.println("Data received: O");

                  //DO HERE PUT CLAW IN NORMAL MODE
                  LyOMessage();
                  modo = "line";
              }
              if(buffer == "<<S>>"){ // Receive data: lego confirm STOP MODE
                // Serial.println("Data received: S");
                //bool confirm_stop = true;
              }
              if(buffer == "<<L>>"){ // Receive data: put claw --> NORMAL MODE
                // Serial.println("Data received: L");

                //DO HERE PUT CLAW IN NORMAL MODE 
                LMessage(); 
              }
              if(buffer == "<<M>>"){ // Receive data: put claw --> CLAW MODE
                // Serial.println("Data received: M");
                //DO HERE PUT CLAW IN RAMP MODE
                MMessage();
              }

              if(buffer == "<<P>>") { // 
              // DO HERE GRAB CLAW IN RESCUE ZONE
                PMessage();
              }

              if(buffer == "<<A>>"){ // Receive data: put claw --> Agarrar and put front light
                // Serial.println("Data received: A");
                //Agarrar and put front light
                //while (currentSwitchState == HIGH) {
                AMessage();  
                //}
              }

              if(buffer == "<<D>>"){ // Receive data: Subir izquierda
                // Serial.println("Data received: D");
                //DO HERE Subir izquierda
                DMessage();
                //delay(2000);
              }

              if(buffer == "<<E>>"){ // Receive data:  Subir derecha
                // Serial.println("Data received: E");
                //DO HERE Subir derecha
                EMessage();
              }

              if(buffer == "<<F>>"){ // Receive data: Depositar Izquierda
                // Serial.println("Data received: F");
                //DO HERE Depositar Izquierda
                FMessage();
              }

              if(buffer == "<<G>>"){ // Receive data: Depositar Derecha
                // Serial.println("Data received: G");
                //DO HERE Depositar Derecha
                GMessage();
              }
              insideMarkers = false;
              buffer = "";
            }
        }
      }
    }
}
