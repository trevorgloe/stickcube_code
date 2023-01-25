#include "DualTB9051FTGMotorShield.h"

DualTB9051FTGMotorShield md;

void setup()
{
  Serial.begin(115200);
  Serial.println("Dual TB9051FTG Motor Shield");
  md.init();

  // Uncomment to flip a motor's direction:
  //md.flipM1(true);
  //md.flipM2(true);
}

void loop() {
  md.enableDrivers();
  delay(1);
  md.setM1Speed(400);
  Serial.println(md.getM1CurrentMilliamps());
  if (md.getM1Fault())
  {
    Serial.println("M1 fault");
  }

}
