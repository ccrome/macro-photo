#include <Servo.h>  
Servo servo;
void setup() 
{ 
  servo.attach(8);  // attaches the servo on pin 9 to the servo object 
} 
 
void loop() 
{ 
  servo.write(30);
  delay(1000);
  servo.write(130);
  delay(1000);
} 

