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
int ball = 0;


// Ball Types (1 is White | 2 is Black)
int type = 0;

// Servo Values
int right_close = 100;
int right_open = 160;
int left_open = 100;
int left_close = 160;

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

  right_claw.write(160);
  lift_servo.write(50);
  
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
    if (r >= 600 && g >= 600 && b >= 600) {
        Serial.println("[System] Detected white ball.");
        type = 1;
    } else if (r >= 85 && r <= 200 && b >= 100 && b <= 200 && g >= 100 && g <= 200) {
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
    left_claw.write(160);
    right_claw.write(95);

    delay(2000);
}

void deposit_up_selector(uint16_t r, uint16_t g, uint16_t b) {
    // Add your code here to deposit the ball based on its type
    if (type == 1) {
        //Verificación si hay una pelota Blanca Medir Color
        if(r <= 600 && g <= 600 && b >= 600) {
            loop();
            return;
        } else {
            digitalWrite(1, LOW);   
            // Elegir al lado que deberia ir
            selector_servo.write(100);
            
            // deposit_servo.write(160);

            
            delay(1000);
            // Moviento para subir
            lift_servo.write(150);
            
            //Soltar a la pelota
            delay(2000);
            
            right_claw.write(140);
            left_claw.write(120);

            // selector_servo.write(160); // a low pushment for the ball.

            // Movimiento para bajar a su posición normal   
            delay(1000);
            lift_servo.write(50);

            // Abrir garras
            delay(1000);
            right_claw.write(160);
            left_claw.write(100);
            // selector_servo.write(100);

        }
    } 
    
    // Reset the type after depositing the ball
    type = 0;
}
