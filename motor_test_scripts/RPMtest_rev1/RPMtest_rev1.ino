#include "DualTB9051FTGMotorShield.h"

DualTB9051FTGMotorShield md;

// Motor encoder output pulse per rotation (change as required)
#define ENC_COUNT_REV 48
 
// Encoder output to Arduino Interrupt pin
#define ENC_IN 3 
 
// MD10C PWM connected to pin 10
//#define PWM 10 
// MD10C DIR connected to pin 12
//#define DIR 12 

// Pulse count from encoder
volatile long encoderValue = 0;

// period of time for each measurement
int interval = 50;
float interval_float = (float)interval;

float ENC_COUNT_float = (float)ENC_COUNT_REV;

// Counters for milliseconds during interval
long previousMillis = 0;
long currentMillis = 0;

// Variable for RPM measuerment
float rpm = 0;
float tickpersec = 0;

// Variable for PWM motor speed output
int motorPwm = 0;

float encoderValFloat = 0;

void updateEncoder()
{
  // Increment value for each pulse from encoder
  encoderValue++;
}

void stopIfFault()
{
  if (md.getM1Fault())
  {
    Serial.println("M1 fault");
    //while (1);
  }
  if (md.getM2Fault())
  {
    Serial.println("M2 fault");
    //while (1);
  }
}

void setup() {
  // Setup Serial Monitor
  Serial.begin(115200); 
  
  // Set encoder as input with internal pullup  
  pinMode(ENC_IN, INPUT_PULLUP); 
 
  // Set PWM and DIR connections as outputs
  //pinMode(PWM, OUTPUT);
  //pinMode(DIR, OUTPUT);
  
  // Attach interrupt 
  attachInterrupt(digitalPinToInterrupt(ENC_IN), updateEncoder, RISING);
  
  // Setup initial values for timer
  previousMillis = millis();

  md.init();

}

void loop() {
  md.enableDrivers();
  delay(1);
  Serial.println("THis is test");
  for (int i = 0; i <= 400; i++)
  {
    md.setM1Speed(i);
    //Serial.println(md.getM1CurrentMilliamps());
    //Serial.println(i);
    stopIfFault();
    //if (abs(i)%200 == 100)
    //{
    //  Serial.print("M1 current: ");
    //  Serial.println(md.getM1CurrentMilliamps());
    //}
    // Update RPM value every interval
    currentMillis = millis();
    //Serial.println(currentMillis);
    
    if (currentMillis - previousMillis > interval) {
      
      //previousMillis = currentMillis;
 
 
      // Calculate RPM
      //interval_float = (float)interval
      encoderValFloat = (float)encoderValue;
      tickpersec = (encoderValFloat*1000.0/interval_float);
      Serial.println(tickpersec);
      rpm = ((tickpersec*60.0)/ENC_COUNT_float);
      //rpm = (float)(encoderValue * 60 * (1 / (interval / 1000)) / ENC_COUNT_REV);
      //Serial.println(rpm);
      // Only update display when there is a reading
      
      Serial.print("PWM VALUE (0 to 400): ");
      Serial.print(i);
      Serial.print('\t');
      Serial.print(" PULSES: ");
      Serial.print(encoderValue);
      Serial.print('\t');
      Serial.print(" SPEED: ");
      Serial.print(rpm);
      Serial.println(" RPM");
      encoderValue = 0;
      
    }
    
    delay(100);
  }

}
