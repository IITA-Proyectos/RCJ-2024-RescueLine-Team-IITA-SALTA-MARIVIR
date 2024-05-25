/* Sweep
 by BARRAGAN <http://barraganstudio.com>
 This example code is in the public domain.

 modified 8 Nov 2013
 by Scott Fitzgerald
 https://www.arduino.cc/en/Tutorial/LibraryExamples/Sweep
*/

#include <Servo.h>

Servo myservo;  // create servo object to control a servo
// twelve servo objects can be created on most boards

int pos = 0;    // variable to store the servo position

void setup() {
  // myservo.attach(9);  // Pin 9 used to servo selector range (120-150) aprox
  myservo.attach(6);  // Pin 6 used to servo deposit range (100-160) aprox
  // myservo.attach(3);  // Pin 3 used to servo lift range (100-180) aprox --> 180:upper // 100:lower
  // myservo.attach(5);  // Pin 5 used to rihgt-claw servo range (100-165) --> 100:close // 160: open
  // myservo.attach(10);  // Pin 10 used to left-claw servo range (160-95) --> 160:close // 95: open
}

void loop() {
  
  for (pos = 100; pos <= 160; pos += 1) { // goes from 0 degrees to 180 degrees
    // in steps of 1 degree
    myservo.write(pos);              // tell servo to go to position in variable 'pos'
    delay(15);                       // waits 15 ms for the servo to reach the position
  }
  for (pos = 160; pos >= 100; pos -= 1) { // goes from 180 degrees to 0 degrees
    myservo.write(pos);              // tell servo to go to position in variable 'pos'
    delay(15);                       // waits 15 ms for the servo to reach the position
  }
}
