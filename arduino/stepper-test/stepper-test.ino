#include <Stepper.h>
Stepper stepper(64*32, 2, 4, 3, 5);

void setup() {
    stepper.setSpeed(10);
}

void loop() {
  // put your main code here, to run repeatedly:
      stepper.step(1000);
      stepper.step(-1000);
}
