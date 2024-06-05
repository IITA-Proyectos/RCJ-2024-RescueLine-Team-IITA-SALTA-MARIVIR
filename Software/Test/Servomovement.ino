/* 
  Diego M. Salinas Fernandez
  04/06/24 (ES) | 06/04/24 (EN) 
  This code has not yet been tested.

-------------------------------------------------------
+ U variables. 
+ This code is working with the white and black ball.
- It dont release the ball yet.
-------------------------------------------------------
*/


#include "Adafruit_APDS9960.h"
#include <Servo.h>

// Sensor and Servo objects
Adafruit_APDS9960 apds;
Servo left_claw;  // Left claw servo
Servo right_claw; // Right claw servo
Servo selector_servo; // Selector Servo
Servo deposit_servo; // Deposit Servo
Servo lift_servo; // Lift Servo

// Servo positions
int pos = 0;
int pos2 = 0;

// Ball detection flag
int ball_white = 0;
int ball_black = 0;

// Ball Types (1 is White | 2 is Black)
int type = 0;

// Servo Values
const int RIGHT_CLOSE = 100;
const int RIGHT_OPEN = 160;
const int LEFT_OPEN = 100;
const int LEFT_CLOSE = 160;
const int LIFT_DOWN = 50;
const int LIFT_UP = 150;
const int SELECTOR_LEFT = 100;
const int SELECTOR_RIGHT = 160;
const int DEPOSIT_POSITION = 160;
const int CLAW_CLOSE_LEFT = 120;
const int CLAW_OPEN_LEFT = 160;
const int CLAW_CLOSE_RIGHT = 140;
const int CLAW_OPEN_RIGHT = 95;

// RGB values for white and black balls
const int RED_WHITEBALL = 600;
const int GREEN_WHITEBALL = 600;
const int BLUE_WHITEBALL = 600;

const int RED_BLACKBALL_MIN = 85;
const int RED_BLACKBALL_MAX = 200;
const int GREEN_BLACKBALL_MIN = 100;
const int GREEN_BLACKBALL_MAX = 200;
const int BLUE_BLACKBALL_MIN = 100;
const int BLUE_BLACKBALL_MAX = 200;

// System condition
bool condition = false;

void setup() {
  pinMode(1, OUTPUT);
  Serial.begin(115200);
  lift_servo.attach(3); // Lift Servo
  selector_servo.attach(9); // Selector Servo
  deposit_servo.attach(6);  // Deposit Servo  
  right_claw.attach(5);  // Right claw servo
  left_claw.attach(10);  // Left claw servo

  right_claw.write(RIGHT_OPEN);
  lift_servo.write(LIFT_DOWN);
  
  if(!apds.begin()){
    Serial.println("Failed to initialize device! Please check your wiring.");
  } else {
    Serial.println("Device initialized!");
    apds.enableColor(true); // Enable color sensing mode
  }
}

void loop() {
  if (!condition) {      
    uint16_t r, g, b, c; // Variables to store the color data in
    
    while(!apds.colorDataReady()){
        delay(5);
    }

    apds.getColorData(&r, &g, &b, &c); // Get the color data
    Serial.print("Red: ");
    Serial.print(r);
    Serial.print(" Green: ");
    Serial.print(g);
    Serial.print(" Blue: ");
    Serial.print(b);
    Serial.print(" Clear: ");
    Serial.println(c);
    Serial.println();

    digitalWrite(1, HIGH);   // LED Front Turn ON

    grab_ball(r, g, b); // Grab the ball based on color
    delay(2000);
  }  
}

void grab_ball(uint16_t r, uint16_t g, uint16_t b) {
    if (r >= RED_WHITEBALL && g >= GREEN_WHITEBALL && b >= BLUE_WHITEBALL) {
        Serial.println("[System] Detected white ball.");
        type = 1;
    } else if (r >= RED_BLACKBALL_MIN && r <= RED_BLACKBALL_MAX && 
               g >= GREEN_BLACKBALL_MIN && g <= GREEN_BLACKBALL_MAX && 
               b >= BLUE_BLACKBALL_MIN && b <= BLUE_BLACKBALL_MAX) {
        Serial.println("[System] Detected black ball.");
        type = 2;
    }

    if (type != 0) {
        claws(); // Close the claws
        deposit_up_selector(r, g, b); // Deposit the ball based on its type
    }
}

void claws() {
    delay(2000);
    left_claw.write(LEFT_CLOSE);
    right_claw.write(RIGHT_OPEN);

    delay(2000);
}

void release_ball_onzone() {
    // Arrived to correct zone.


    // Moved the correct side for release the balls.
}

void deposit_up_selector(uint16_t r, uint16_t g, uint16_t b) {
    if (type == 1) {
        // Verif of WHITEBALL
        if (r <= RED_WHITEBALL && g <= GREEN_WHITEBALL && b <= BLUE_WHITEBALL) {
            loop();
            return;
        } else {
            digitalWrite(1, LOW);   
            // Select the side for the ball.
            selector_servo.write(SELECTOR_LEFT);
            
            // Up Lift
            lift_servo.write(LIFT_UP);
            
            // release the ball.
            delay(2000);
            
            right_claw.write(CLAW_CLOSE_RIGHT);
            left_claw.write(CLAW_CLOSE_LEFT);

            // Lift go to position normal.
            delay(1000);
            lift_servo.write(LIFT_DOWN);

            // open claws.
            delay(1000);
            right_claw.write(RIGHT_OPEN);
            left_claw.write(LEFT_OPEN);
        }
    } else if (type == 2) {
        // Select the side for the ball.
        selector_servo.write(SELECTOR_RIGHT);

        //Up lift
        lift_servo.write(LIFT_UP);

        // release the ball.
        delay(2000);

        right_claw.write(CLAW_CLOSE_RIGHT);
        left_claw.write(CLAW_CLOSE_LEFT);

        // Lift go to position normal.
        delay(1000);
        lift_servo.write(LIFT_DOWN);


        // open claws.
        delay(1000);
        right_claw.write(RIGHT_OPEN);
        left_claw.write(LEFT_OPEN);
    }
    
    // Reset the type after depositing the ball
    type = 0;
}

