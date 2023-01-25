
// variable state controls the 
int state = 0;
// state = 0 - test has not begun yet. arduino will look for input from serial to begin executing
// state = 1 - arduino will read the value of the pushbutton for a period of time specfied in the input to start

float tmax = 0;

long previousMillis = 0;
long currentMillis = 0;

String tmax_str;

// the setup routine runs once when you press reset:
void setup() {
  // initialize serial communication at 9600 bits per second:
  Serial.begin(115200);
  // make the pushbutton's pin an input:
  pinMode(pushButton, INPUT);
}

void loop() {
  switch (state) {
    case 0:
      // the non-active state
      // will stay in this state until a value is given through serial
      tmax_str = Serial.readString();
      if (tmax_str != "") {
        tmax = tmax_str.toFloat();
        state = 1;
        previousMillis = millis();
        Serial.print("Changed!\n");
        Serial.println(tmax);
        delay(1);
        break;
      } else {
        Serial.print("waiting\n");
        break;
      }
    case 1:
      // the active state
      // will constant read data from the pushButton pork for the amount of time, tmax
      //Serial.println(previousMillis);
      currentMillis = millis();
      //Serial.println(currentMillis);
      if ((currentMillis - previousMillis)/1000 < tmax) {
        // read the input pin:
        int t = currentMillis - previousMillis;
        // print out the state of the button:
        String output1 = "Time: " + String(t);
        String output2 = "Button: " + String(buttonState);
        String output_full = output1 + "\t" + output2;
        Serial.print(output_full + "\n");
        delay(1);        // delay in between reads for stability
        break;
      } else {
        state = 0;
        break;
      }
  }

}
