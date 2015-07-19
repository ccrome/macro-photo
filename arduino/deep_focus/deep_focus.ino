#include <Stepper.h>
#include <Servo.h>
#define  SERVO_GOTO 1
#define  STEPPER_STEP 2
#define  INVALID 3

  int cmd;
  int value;

Servo servo;
Stepper stepper(64*32, 2, 4, 3, 5);
const int steps_per_photo = 32;
const int degrees_per_photo = 5.625;
const int start_angle = 30;
const int end_angle = 130;
const int dly = 100;
int current_angle;

int servo_last_value;

void setup() {
  // put your setup code here, to run once:
  servo.attach(8);
  servo_last_value = 30;
  servo.write(servo_last_value);
  current_angle = start_angle;
  stepper.setSpeed(10);
  Serial.begin(9600);
  Serial.print("Deep Photo");
}

void get_command() {
  int command_found = 0;
  while (!command_found) {
    char c = Serial.read();
    switch (c) {
      case 'v':
      case 'V':
          // servo command
          value = Serial.parseInt();
          cmd = SERVO_GOTO;
          command_found = 1;
      break;
      case 's':
      case 'S':
          value = Serial.parseInt();
          cmd = STEPPER_STEP;
          command_found = 1;
      break;
    }
  }
}

void servo_goto(int value)
{
  int dir = 1;
  if (value < servo_last_value)
    dir = -1;
  int current = servo_last_value;
  int i;
  for (i = 0; i < (abs(servo_last_value-value)); i++) {
    current += dir;
    servo.write(current);
    delay(50);
  }
  servo.write(value);
  servo_last_value = value;
}

void loop() {
  // put your main code here, to run repeatedly:
  get_command();  
  switch (cmd) {
    case SERVO_GOTO:
      servo_goto(value);
      Serial.write("servo moved to ");
      Serial.print(value);
      Serial.write("\n");
      delay(100);
      break;
    case STEPPER_STEP:
      stepper.step(-value);
      Serial.write("stepped ");
      Serial.print(value);
      Serial.write(" steps\n");
      break;
    case INVALID:
    default:
      Serial.write("Invalid command\n");
      break;
  }
  return;
  servo.write(start_angle);
  stepper.step(steps_per_photo);
  delay(500);
  for (current_angle = start_angle; current_angle < end_angle; current_angle++) {
    servo.write(current_angle);
    delay(dly);
  }  
}
