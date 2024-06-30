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
bool  currentlightON=false;




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
byte lightpin = 1 ; // esto hay que reemplazar por el pin de encendido de luz

void setup() {
  Serial.begin(9600);
  Serial.println("Setup.");
  HCSR04.begin(triggerPin, echoPins, echoCount);
  
  
  if (Usb.Init() == -1) {
    //Serial.println("OSCOKIRQ failed to assert");
  }

  // if (!apds.begin()) {
  //   // Serial.println("Failed to init device! check wiring.");
  // } else {
  //   // Serial.println("Device init!");
  //   apds.enableColor(true);
  // }

  lift_servo.attach(pinLifts);
  selector_servo.attach(PinSelector);
  deposit_servo.attach(PinDeposit);
  right_claw.attach(PinRight);
  left_claw.attach(PinLeft);

  //lift_servo.write(44); // Punto Medio

  //Default Positions
  LMessage();
  deposit_servo.write(DEPOSIT_DEFAULT);

  pinMode(switchPin, INPUT_PULLUP);
  pinMode(lightpin, OUTPUT);
  digitalWrite(lightpin, LOW);  //switch light off

  //   // Check about the Switch status.
  //   bool TReceived = false;
  //   while (TReceived == false) {
  //     Usb.Task();
  //     currentSwitchState = digitalRead(switchPin);
    
  //   // Break while true if switch is ON
    
  //   //Led function for waiting spike response. /Delay comun no


    
  //     if (Acm.isReady()) 
  //       {
  //         uint8_t buf[1024];
  //         uint16_t rcvd = 1024;
  //         uint8_t rcode = Acm.RcvData(&rcvd, buf);
  //         if (rcode && rcode != hrNAK)
  //             ErrorMessage<uint8_t>(PSTR("Ret"), rcode);
  //         if (rcvd) {
  //             for (uint16_t i = 0; i < rcvd; i++) {
  //                 char data = (char)buf[i];
  //                 char datanext = (char)buf[i];
  //                 if (data == '<' && datanext == '<') {
  //                     buffer = "<<";
  //                     insideMarkers = true;
  //                 }
  //                 if (insideMarkers && data != '>' && data != '<') {
  //                     buffer += data;
  //                 }
  //                 if (data == '>' && datanext == '>' && insideMarkers) {
  //                     buffer += ">>";
  //                     if (buffer == "<<T>>") {
  //                         TReceived = true;
  //                         Serial.println("T recibida");
  //                         ButtonSwitchServos();
  //                         break;
  //                         //sendConfirmation();
  //                     }
  //                     insideMarkers = false;
  //                     buffer = "";
  //                 }
  //             }
  //       }
  //     }
  //     while (digitalRead(switchPin) == LOW && TReceived == false) {
  //       wait_for_spike();
  //       if (TReceived == true && digitalRead(switchPin) == HIGH) {
  //         break;
  //       }
  //     }
  // }  
  // Execute tilight if Switch is ON 
  // 255 = LOW = ON = STOP
  // 254 = HIGH = OFF = RUN
  while (digitalRead(switchPin) == LOW) {
    Tilight();
  }
     
   
  delay(200); 
  Serial.println("jjjj   nnnn   Setup.");
}


// ----------- General ----------
void delay_switch(int espera) {
  int current_time;

  current_time = millis(); 

  while (millis() - current_time < espera && currentSwitchState == HIGH && currentSwitchState == lastSwitchState)
  {
     currentSwitchState = digitalRead(switchPin);
  }
}


void wait_for_spike() {
    //Serial.println("wait_for_spike");
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
    Serial.println("tilight");
    unsigned long current_Millis = millis(); // time on live
    if (currentlight_ON && (current_Millis - previosMillis_light > tlight_high)) {
        digitalWrite(lightpin, LOW);
        currentlight_ON = false;
        previosMillis_light = current_Millis;
    } else if (!currentlight_ON && (current_Millis - previosMillis_light > tlight_low)) {
        digitalWrite(lightpin, HIGH);
        currentlight_ON = true;
        previosMillis_light = current_Millis;
    }
}


// ---------- COLOR_SENSOR ---------
void read_data_color() {
  // while (!apds.colorDataReady()) {
  //   delay_switch(5);
  // }
  apds.getColorData(&r, &g, &b, &c);
  Serial.println("read_data_color()");
  Serial.println("R: " + String(r) + " G: " + String(g) + " B: " + String(b));
}

uint8_t getRawValueColor(uint16_t color) {
    // Map the r value to the range 0-240
    int mapped_value = map(color, 0, 400, 0, 240);

    // Constrain the value to be between 0 and 240
    mapped_value = constrain(mapped_value, 0, 240);

    // Prepare the byte to send
    byte byte_to_send = (byte)mapped_value;

    // Return the rawValue
    uint8_t rawValue = byte_to_send;
    return rawValue;
}

// ---------- SERVOS ----------

void DMessage() { //Go up to left way.
  lift_servo.write(LIFT_SERVO_UPPER);

  delay_switch(2000);

  right_claw.write(RIGHT_LESS_OPEN);
  left_claw.write(LEFT_LESS_OPEN);
  
  selector_servo.write(SELECTOR_LEFT);
  
  delay_switch(2000);

  selector_servo.write(SELECTOR_SPECIAL_LEFT); 
}


void EMessage() { // Gop up to right way.
  
  lift_servo.write(LIFT_SERVO_UPPER);
  
  delay_switch(2000);

  right_claw.write(RIGHT_LESS_OPEN);
  left_claw.write(LEFT_LESS_OPEN);
  selector_servo.write(SELECTOR_RIGHT);

  delay_switch(2000);
  
  selector_servo.write(SELECTOR_SPECIAL_RIGHT);
}


void FMessage() { // Left deposit
  delay_switch(1000);

  deposit_servo.write(DEPOSIT_LEFT);
  delay_switch(6000);

}

void GMessage() { // Right deposit
  delay_switch(1000);

  deposit_servo.write(DEPOSIT_RIGHT);
  delay_switch(6000);

}

void MMessage() { // Ramp Mode 
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

String mode = "rescue";


void loop() {
  //Serial.println(mode);

  read_data_color();
  Usb.Task();

  currentSwitchState = digitalRead(switchPin);

  if (Acm.isReady()) {
      unsigned long currentMillis = millis();
      // READING DATA FROM LEGO
      uint8_t  buf[1024];  // This size work rightly because the LEGO stream 
      uint16_t rcvd = 1024;
      uint8_t rcode = Acm.RcvData(&rcvd, buf);
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
                  mode = "rescue";
                  digitalWrite(lightpin, HIGH);
              }
              if (buffer == "<<O>>") { // Receive data: put mode --> line
                  // Serial.println("Data received: O");

                  //DO HERE PUT CLAW IN NORMAL MODE
                  LyOMessage();

                  mode = "line";
              }
              if(buffer == "<<S>>"){ // Receive data: lego confirm STOP MODE
                // Serial.println("Data received: S");
                bool confirm_stop = true;
              }
              if(buffer == "<<L>>"){ // Receive data: put claw --> NORMAL MODE
                // Serial.println("Data received: L");

                //DO HERE PUT CLAW IN NORMAL MODE 
                LyOMessage(); 
              }
              if(buffer == "<<M>>"){ // Receive data: put claw --> CLAW MODE
                // Serial.println("Data received: I");
                //DO HERE PUT CLAW IN RAMP MODE
                MMessage();
              }

              if(buffer == "<<P>>") { // 
              // DO HERE GRAB CLAW IN RESCUE ZONE
                PMessage();
              }

              if(buffer == "<<A>>"){ // Receive data: put claw --> Agarrar and put front light
                // Serial.println("Data received: I");
                //Agarrar and put front light
                while (currentSwitchState == HIGH) {
                  AMessage();  
                }
              }

              if(buffer == "<<D>>"){ // Receive data: Subir izquierda
                // Serial.println("Data received: I");
                //DO HERE Subir izquierda
                DMessage();
                delay(2000);
              }

              if(buffer == "<<E>>"){ // Receive data:  Subir derecha
                // Serial.println("Data received: I");
                //DO HERE Subir derecha
                EMessage();
              }

              if(buffer == "<<F>>"){ // Receive data: Depositar Izquierda
                // Serial.println("Data received: I");
                //DO HERE Depositar Izquierda
                FMessage();
              }

              if(buffer == "<<G>>"){ // Receive data: Depositar Derecha
                // Serial.println("Data received: I");
                //DO HERE Depositar Derecha
                GMessage();
              }
              insideMarkers = false;
              buffer = "";
            }
        }
      }

      // Detect change of state In SWITCH
      if (currentSwitchState != lastSwitchState) {
          //delay(50); // Debounce delay
          currentSwitchState = digitalRead(switchPin);
          if (currentSwitchState != lastSwitchState) {
              lastSwitchState = currentSwitchState;
              if (currentSwitchState == LOW) {
                  uint8_t rawValue = 255; //--> Switch is ON
                  rcode = Acm.SndData(1, &rawValue);
                  ButtonSwitchServos();
                  Serial.println("255");
                  if (rcode) {
                      ErrorMessage<uint8_t>(PSTR("SndData"), rcode);
                  }
                  // Serial.println("Sent: 255 --> SWITCH ON")
                  currentlightON = false;
                  delay(2000);
              } else {
                  uint8_t rawValue = 254; //--> Switch is OFF
                  rcode = Acm.SndData(1, &rawValue);
                  Serial.println("244");
                  if (rcode) {
                      ErrorMessage<uint8_t>(PSTR("SndData"), rcode);
                  }
                  delay(2000);
                  // Serial.println("Sent: 254 --> SWITCH OFF");
                  // HERE DO THE SETUP
              }
          }
       }

      // Manage the behavior of Front Light
      if (currentSwitchState == LOW){
        //digitalWrite(lightpin, HIGH);
        if(currentlightON and (currentMillis - previosMillislight)> tlighthigh)
        {
        digitalWrite(lightpin, LOW);  // switch light off
        currentlightON = false;
        previosMillislight = currentMillis;
        }
        else if( !currentlightON and (currentMillis - previosMillislight)> tlightlow )
        {             
        digitalWrite(lightpin, HIGH);  // switch light on
        currentlightON = true;
        previosMillislight = currentMillis;
        }  
      }
      else{
        digitalWrite(lightpin, LOW);
      }

      if (mode == "rescue" && currentMillis - previousMillis >= interval && currentSwitchState == HIGH) {
        previousMillis = currentMillis;
        digitalWrite(lightpin, HIGH);


        //--> Send data of color R_value
        uint8_t rawValue = 253; // --> Reference data color R_value
        rcode = Acm.SndData(1, &rawValue);
        if (rcode) {
            ErrorMessage<uint8_t>(PSTR("SndData"), rcode);
        }
        rawValue = getRawValueColor(r);
        rcode = Acm.SndData(1, &rawValue); // --> Color R_value
        Serial.print("R: " + String(rawValue));
        if (rcode)
        {
            ErrorMessage<uint8_t>(PSTR("SndData"), rcode);
        }
        
        // //--> Send data of color G_value
        // rawValue = 252; 
        // rcode = Acm.SndData(1, &rawValue); // --> Reference data color G_value
        // if (rcode) {
        //     ErrorMessage<uint8_t>(PSTR("SndData"), rcode);
        // }
        // rawValue = getRawValueColor(g); // --> Color G_value
        // rcode = Acm.SndData(1, &rawValue);
        // Serial.print(" G:" + String(rawValue));
        // if (rcode)
        // {
        //     ErrorMessage<uint8_t>(PSTR("SndData"), rcode);
        // }

        // //--> Send data of color B_value
        // rawValue = 251; // --> Reference data color B_value
        // rcode = Acm.SndData(1, &rawValue);
        // if (rcode) {
        //     ErrorMessage<uint8_t>(PSTR("SndData"), rcode);
        // }
        // rawValue = getRawValueColor(b);
        // rcode = Acm.SndData(1, &rawValue); // --> Color B_value
        // Serial.println(" B:"+ String(rawValue));
        // Serial.println("-- Data sent to LEGO --");
        // if (rcode)
        // {
        //     ErrorMessage<uint8_t>(PSTR("SndData"), rcode);
        // }

        // double * distances = HCSR04.measureDistanceCm();
        // int front_sensor = distances[0];
        // int right_sensor = distances[1];
        // int left_sensor = distances[2];

        // if (front_sensor != -1) {
        //   // Map the front sensor value to the range 0-240
        //   int mapped_value = map(front_sensor, 0, 400, 0, 240); // The max distance the sensor can read is 400 cm ? 

        //   // Constrain the value to be between 0 and 240
        //   mapped_value = constrain(mapped_value, 0, 240);

        //   // Prepare the byte to send
        //   byte byte_to_send = (byte)mapped_value;

        //   uint8_t rawValue = byte_to_send;
        //   uint8_t rcode = Acm.SndData(1, &rawValue);

        //   // Serial.println(String(byte_to_send));
        // } else {
        //   // Serial.println("Invalid sensor reading, skipping...");
        // }

        // if (right_sensor != -1) {
        //   // Map the front sensor value to the range 0-240
        //   int mapped_value = map(right_sensor, 0, 400, 0, 240); // The max distance the sensor can read is 400 cm ? 

        //   // Constrain the value to be between 0 and 240
        //   mapped_value = constrain(mapped_value, 0, 240);

        //   // Prepare the byte to send
        //   byte byte_to_send = (byte)mapped_value;

        //   uint8_t rawValue = byte_to_send;
        //   uint8_t rcode = Acm.SndData(1, &rawValue);

        //   // Serial.println(String(byte_to_send));
        // } else {
        //   // Serial.println("Invalid sensor reading, skipping...");
        // }

        // if (left_sensor != -1) {
        //   // Map the front sensor value to the range 0-240
        //   int mapped_value = map(left_sensor, 0, 400, 0, 240); // The max distance the sensor can read is 400 cm ? 

        //   // Constrain the value to be between 0 and 240
        //   mapped_value = constrain(mapped_value, 0, 240);

        //   // Prepare the byte to send
        //   byte byte_to_send = (byte)mapped_value;

        //   uint8_t rawValue = byte_to_send;
        //   uint8_t rcode = Acm.SndData(1, &rawValue);

        //   // Serial.println(String(byte_to_send));
        // } else {
        //   // Serial.println("Invalid sensor reading, skipping...");
        // }
      }


      // Line mode only send data of front_ultrasonic_sensor
      if (mode == "line" && currentMillis - previousMillis >= interval && currentSwitchState == HIGH) {
      previousMillis = currentMillis;

      double* distances = HCSR04.measureDistanceCm();
      int front_sensor = distances[0];

      if (front_sensor != -1) {
          // Map the front sensor value to the range 0-240
          int mapped_value = map(front_sensor, 0, 400, 0, 240); // The max distance the sensor can read is 400 cm ? 

          // Constrain the value to be between 0 and 240
          mapped_value = constrain(mapped_value, 0, 240);

          // Prepare the byte to send
          byte byte_to_send = (byte)mapped_value;

          uint8_t rawValue = byte_to_send;
          uint8_t rcode = Acm.SndData(1, &rawValue);

          // Serial.println(String(byte_to_send));
      } else {
          // Serial.println("Invalid sensor reading, skipping...");
      }
    }
  }
}

// void sendConfirmation() {
//   uint8_t rawValue = 72; // --> Send to Spike for confirmation. | 72: H 
//   rcode = Acm.SndData(1, &rawValue);

//   if (rcode) {
//     ErrorMessage<uint8_t>(PSTR("SndData"), rcode);
//   }        
// }

