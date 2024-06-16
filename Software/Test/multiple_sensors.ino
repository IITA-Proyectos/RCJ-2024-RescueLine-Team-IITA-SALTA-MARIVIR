#include <cdcacm.h>
#include <usbhub.h>


#include "pgmstrings.h"

// Satisfy the IDE, which needs to see the include statement in the ino too.
#ifdef dobogusinclude
#include <spi4teensy3.h>
#endif
#include <SPI.h>

#include <HCSR04.h>
byte triggerPin = 16;
byte echoCount = 3;
byte* echoPins = new byte[echoCount] { 15, 8, 7 };
int front_sensor, right_sensor, left_sensor;

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
ACMAsyncOper  AsyncOper;
ACM           Acm(&Usb, &AsyncOper);
String buffer = "";
bool insideMarkers = false;

unsigned long previousMillis = 0;
const long interval = 500;

void setup()
{
  pinMode(1, OUTPUT);
  digitalWrite(1, LOW);

  Serial.begin( 115200 );
  Serial.print("Iniciado...");



  if (Usb.Init() == -1)
      // Serial.println("OSCOKIRQ failed to assert");

  delay( 200 );

  HCSR04.begin(triggerPin, echoPins, echoCount);
}

void loop()
{
    Usb.Task();

    if (Acm.isReady()) {
       uint8_t rcode;

      // Get current time
      unsigned long currentMillis = millis();

      // Check if it's time to send data
      if (currentMillis - previousMillis >= interval) {
        double* distances = HCSR04.measureDistanceCm();
        front_sensor = distances[0];
        right_sensor = distances[1];
        left_sensor = distances[2];

        // Prepare data to send
        
        String data =  String(front_sensor) + "," + String(right_sensor) + "," + String(left_sensor);
        
        
        Serial.println("Serial: " + data);

        // Sending data to the LEGO
        const char* sendData = data.c_str(); // Convert to C-string
        rcode = Acm.SndData(strlen(sendData), (uint8_t*)sendData); // Send the entire string

        Serial.println("Data sent to LEGO");
        if (rcode){
          ErrorMessage<uint8_t>(PSTR("SndData"), rcode);
        }

        // Save the last time data was sent
        previousMillis = currentMillis;
      }

      // Reading data from LEGO
      uint8_t  buf[1024];
      uint16_t rcvd = 1024;
      rcode = Acm.RcvData(&rcvd, buf);
      if (rcode && rcode != hrNAK){
        ErrorMessage<uint8_t>(PSTR("Ret"), rcode);
      }

      if (rcvd) { //more than zero bytes received
        for (uint16_t i = 0; i < rcvd; i++) {
            char data = (char)buf[i];
            char datanext = (char)buf[i];
            if (data == '<' && datanext == '<'){
              buffer = "<<";
              insideMarkers = true;
            }
            if (insideMarkers && data !='>' && data !='<'){
              buffer += data;
            }
            if (data == '>' && datanext == '>' && insideMarkers){ 
              buffer += ">>";
              Serial.println("Buffer: " + buffer);
              if (buffer == "<<A>>"){
                // Serial.println("Llego la A");
              }
              if (buffer == "<<B>>"){
                // Serial.println("Llego la B");
              }
              insideMarkers = false;
              buffer = "";
            }
        }
      }
  }
}
