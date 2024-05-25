/***************************************************************************
  This is a library for the APDS9960 digital proximity, ambient light, RGB, and gesture sensor

  This sketch puts the sensor in color mode and reads the RGB and clear values.

  Designed specifically to work with the Adafruit APDS9960 breakout
  ----> http://www.adafruit.com/products/3595

  These sensors use I2C to communicate. The device's I2C address is 0x39

  Adafruit invests time and resources providing this open source code,
  please support Adafruit andopen-source hardware by purchasing products
  from Adafruit!

  Written by Dean Miller for Adafruit Industries.
  BSD license, all text above must be included in any redistribution
 ***************************************************************************/

#include "Adafruit_APDS9960.h"
#include <Servo.h>
Adafruit_APDS9960 apds;


Servo myservo;  // create servo object to control a servo
Servo myservo2;
// twelve servo objects can be created on most boards

// Int Values
int pos = 0;    // variable to store the servo position
int pos2 = 0;
int ball = 0;

//Servos Values
 int right_close = 100;
 int right_open = 160;

 int left_open = 100;
 int left_close =  160

// Bool Values
bool condition = false;

void setup() {
  pinMode(1, OUTPUT);
  
  Serial.begin(115200);
  // myservo.attach(9);  // Pin 9 used to servo selector range (120-150) aprox
  //myservo.attach(6);  // Pin 6 used to servo deposit range (100-160) aprox
  // myservo.attach(3);  // Pin 3 used to servo lift range (100-180) aprox --> 180:upper // 100:lower
  myservo2.attach(5);  // Pin 5 used to rihgt-claw servo range (100-165) --> 100:close // 160: open
  myservo.attach(10);  // Pin 10 used to left-claw servo range (160-95) --> 160:close // 95: open


  if(!apds.begin()){
    Serial.println("failed to initialize device! Please check your wiring.");
  }
  else Serial.println("Device initialized!");

  //enable color sensign mode
  apds.enableColor(true);
}

void loop() {
  if (condition == true) {
    return;
  } else if (condition == false) {
    
  //create some variables to store the color data in
  uint16_t r, g, b, c;
  
  //wait for color data to be ready
  while(!apds.colorDataReady()){
    delay(5);
  }

  //get the data and print the different channels
  apds.getColorData(&r, &g, &b, &c);
  Serial.print("red: ");
  Serial.print(r);
  
  Serial.print(" green: ");
  Serial.print(g);
  
  Serial.print(" blue: ");
  Serial.print(b);
  
  Serial.print(" clear: ");
  Serial.println(c);
  Serial.println();

  digitalWrite(1, HIGH);   // LED Front Turn ON

  for (pos = 100, pos2 = 160; pos <= 160, pos2 >= 160; pos +=1, pos2 -= 1) {
    myservo.write(pos);
    myservo2.write(pos2);
    Serial.print("RIGHT:");
    Serial.println(pos2);
    Serial.print("LEFT:");
    Serial.println(pos);
    delay(2000);
  }


  for (pos = 160, pos2 = 100; pos >= 100, pos2 <= 100; pos -=1, pos2 +=1) {
    myservo.write(pos);
    myservo2.write(pos2);
    Serial.print("RIGHT 2:");
    Serial.println(pos2);
    Serial.print("LEFT 2:");
    
    Serial.println(pos);

    if (r >= 900, g >= 900, b >= 900) {
      Serial.print("Pelota Blanca");
      condition = true;
      break;
    } else if (r >= 85 and r <= 200, b >= 100 and b <= 200,  g >= 100 and g <= 200) {
      Serial.print("Pelota Negra");
      condition = true; 
    }
  }
  
  delay(2000);                       // wait for a second
  }
  
}
