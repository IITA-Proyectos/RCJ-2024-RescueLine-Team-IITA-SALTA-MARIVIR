#include <cdcacm.h>
#include <usbhub.h>

#include <Servo.h>
#include <HCSR04.h>

byte triggerPin = 16;
byte echoCount = 3;
byte * echoPins = new byte[echoCount] { 15, 8, 7};

#include "pgmstrings.h"

// Satisfy the IDE, which needs to see the include statment in the ino too.
#ifdef dobogusinclude
#include <spi4teensy3.h>
#endif
#include <SPI.h>

Servo lift_servo;
Servo deposit_servo;
Servo right_claw;
Servo left_claw;
Servo selector_servo;

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

    LINE_CODING	lc;
    lc.dwDTERate	= 115200;
    lc.bCharFormat	= 0;
    lc.bParityType	= 0;
    lc.bDataBits	= 8;

    rcode = pacm->SetLineCoding(&lc);

    if (rcode)
        ErrorMessage<uint8_t>(PSTR("SetLineCoding"), rcode);

    return rcode;
}

USB     Usb;
//USBHub     Hub(&Usb);
ACMAsyncOper  AsyncOper;
ACM           Acm(&Usb, &AsyncOper);
String buffer = "";
bool insideMarkers = false;
bool outsideMarkers = false;

void setup()
{
  pinMode(1, OUTPUT);
  Serial.begin(115200);
  digitalWrite(1, LOW);
  HCSR04.begin(triggerPin, echoPins, echoCount);

  lift_servo.attach(3); // Selector Servo
  selector_servo.attach(9);
  deposit_servo.attach(6);
  right_claw.attach(5);
  left_claw.attach(10);

  lift_servo.write(44); //Punto Medio

  //Pruebas de valores de los servos.
  // delay(2000);
  // lift_servo.write(60); //Punto Bajo
  // delay(2000);
  // lift_servo.write(40); // Piso

  // lift_servo.write(20); //Up
  // deposit_servo.write(100); // Normal
  
  // selector_servo.write(120);
  // delay(2000);
  // selector_servo.write(150);

  // delay(2000);

  // left_claw.write(100); // Open 
  // delay(1000);
  // left_claw.write(160); // Close


  // right_claw.write(100); //Open
  // delay(1000);
  // right_claw.write(40); //Close

#if !defined(__MIPSEL__)
  // while (!Serial); // Wait for serial port to connect - used on Leonardo, Teensy and other boards with built-in USB CDC serial connection
#endif
  // Serial.println("Start");

  if (Usb.Init() == -1)
      // Serial.println("OSCOKIRQ failed to assert");

  delay( 200 );
}
int counter = 0;

void found_ball() {
  delay(2000);
  left_claw.write(160);
  right_claw.write(40);
  deposit_up_selector();
}

void claws_closed() {
  delay(2000);
  left_claw.write(160);
  right_claw.write(40);
}

void claws_open() {
  delay(2000);
  left_claw.write(100);
  right_claw.write(40);
}

void deposit_up_selector() {
  delay(1000);

  lift_servo.write(150); // Up
  delay(1000);

  claws_open();

  delay(1000);
  lift_servo.write(20); // Down
  claws_closed();
}




void loop()
{
    Usb.Task();

    if( Acm.isReady()) {
       uint8_t rcode;

       double* distances = HCSR04.measureDistanceCm();

       int front_sensor = distances[0];

       /* This part send a message to LEGO , the message can be like "a", "A", "{20,15}" or like you estructure */

        //  String data = Serial.readStringUntil('\n'); // Read a string until newline character
            String data = String(front_sensor); 


         Serial.println(data);
        //  /* sending to the LEGO */
        const char* sendData = data.c_str(); // Convert to C-string
        // rcode = Acm.SndData(strlen(sendData), (uint8_t*)sendData); // Send the entire string

        Serial.println("Data sent to LEGO");
        if (rcode)
          ErrorMessage<uint8_t>(PSTR("SndData"), rcode);
        

        /* Reading to Lego need a meesage like <<a>> and use the "<<>>" to identify the message*/
        /* buffer size must be greater or equal to max.packet size */
        /* it it set to 64 (largest possible max.packet size) here, can be tuned down
        for particular endpoint */
        uint8_t  buf[1024];
        uint16_t rcvd = 1024;
        rcode = Acm.RcvData(&rcvd, buf);
         if (rcode && rcode != hrNAK){
            ErrorMessage<uint8_t>(PSTR("Ret"), rcode);
         }
        if( rcvd ) { //more than zero bytes received
        for (uint16_t i = 0; i < rcvd; i++) {
            char data = (char)buf[i];
            char datanext = (char)buf[i];
            //Serial.println(data);
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
              Serial.println("Buffer: " + buffer);
                 
              if(buffer == "<<R>>") {
                  // Serial.println("Data received: D");
                  lift_servo.write(44); //UP
              } else if (buffer == "<<L>>") {
                  // Serial.println("Data received: I");
                  lift_servo.write(50); //DOWN
              } else if (buffer == "<<C>>") {
                  found_ball();
                //Todavia no testeado
              }

              insideMarkers = false;
              buffer = "";
            }
        }
          //Serial.println();
        }
  }
  
}
