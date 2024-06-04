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

  digitalWrite(1, LOW);
  HCSR04.begin(triggerPin, echoPins, echoCount);
  selector_servo.attach(9); // Selector Servo


#if !defined(__MIPSEL__)
  // while (!Serial); // Wait for serial port to connect - used on Leonardo, Teensy and other boards with built-in USB CDC serial connection
#endif
  // Serial.println("Start");

  if (Usb.Init() == -1)
      // Serial.println("OSCOKIRQ failed to assert");

  delay( 200 );
}
int counter = 0;

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


        //  Serial.println("Serial: " + data);
         /* sending to the LEGO */
        const char* sendData = data.c_str(); // Convert to C-string
        rcode = Acm.SndData(strlen(sendData), (uint8_t*)sendData); // Send the entire string

        // Serial.println("Data sent to LEGO");
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
                 
              if(buffer == "<<D>>") {
                  // Serial.println("Data received: D");
                  selector_servo.write(100);
              } else if (buffer == "<<I>>") {
                  // Serial.println("Data received: I");
                  selector_servo.write(160);
              }

              insideMarkers = false;
              buffer = "";
            }
        }
          //Serial.println();
        }
  }
  
}
