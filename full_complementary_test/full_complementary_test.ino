#include <stdio.h>
#include "quat.h"
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
#include <utility/imumaths.h>


/* Set the delay between fresh samples */
#define BNO055_SAMPLERATE_DELAY_MS (100)

// Check I2C device address and correct line below (by default address is 0x29 or 0x28)
//                                   id, address
Adafruit_BNO055 bno = Adafruit_BNO055(-1, 0x28);


struct quat {
  float r;
  float i;
  float j;
  float k;
};

struct return_data {
  float return_value_x;
  float return_value_y;
};

struct prev_data {
  float prev_ux1; // make this name more explicit
  float prev_ux2; 
  float prev_yx; // change this name
  float prev_uy1;
  float prev_uy2;
  float prev_yy;
};

struct args{
  float T=0.2;
  float omega = 2.0; // make it const float or #define (a little better/cooler this way)
  float a = 1.0/(2.0+T*omega); // make all the constants variables defined at the top
  float b = (T*omega - 2.0);
  float ux;
  float uy;
}; 

struct accel_angles{
  float alpha = 0.0; // might not wanna set a default value for these
  float beta = 0.0;
};

struct gyro_vals{
  float gyrox;
  float gyroy;
};

struct gyro_prev{
  float prev_gyrox;
  float prev_gyroy;
  float prev_angx;
  float prev_angy;
};

struct gyro_angles{
  float gyro_xang;
  float gyro_yang;
};

struct return_data ret; // put this in the loop method scope
struct prev_data prev; // this is ok to have in the global scope
struct args arg;

struct accel_angles accel_angle; // also put in loop

struct gyro_vals gyros; // also put in loop
struct gyro_prev gprev; // this is fine
struct gyro_angles g_angs; // also put in loop

struct quat q; //quaternian

// variable state controls the 
int state = 0;
// state = 0 - test has not begun yet. arduino will look for input from serial to begin executing
// state = 1 - arduino will read the value of the pushbutton for a period of time specfied in the input to start

float tmax = 0;

long previousMillis = 0;
long currentMillis = 0;

String tmax_str;

void setup() {

  // can get rid of all the ones that arent previous values
  ret.return_value_x = 0.0;
  ret.return_value_y = 0.0;
  prev.prev_ux1 = 0.0;
  prev.prev_ux2 = 0.0;
  prev.prev_uy1 = 0.0;
  prev.prev_uy2 = 0.0;
  prev.prev_yx = 0.0;
  prev.prev_yy = 0.0;
  arg.ux=0.0;
  arg.uy=0.0;

  gyros.gyrox = 0.0;
  gyros.gyroy = 0.0;
  gprev.prev_gyrox = 0.0;
  gprev.prev_gyroy = 0.0;
  gprev.prev_angx = 0.0;
  gprev.prev_angy = 0.0;
  g_angs.gyro_xang = 0.0;
  g_angs.gyro_yang = 0.0;

  
  Serial.begin(115200);
  // Serial.println("Orientation Sensor Raw Data Test"); Serial.println("");

  /* Initialise the sensor */
  if(!bno.begin())
  {
    /* There was a problem detecting the BNO055 ... check your connections */
    Serial.print("Ooops, no BNO055 detected ... Check your wiring or I2C ADDR!");
    while(1);
  }

  delay(1000);
  

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

        // put your main code here, to run repeatedly:
        // call IMU function to return data get accel and gyro
        imu::Vector<3> gyro = bno.getVector(Adafruit_BNO055::VECTOR_GYROSCOPE);
        imu::Vector<3> accel = bno.getVector(Adafruit_BNO055::VECTOR_ACCELEROMETER);

        //Serial.print(gyro.x());
        //Serial.print(" ");
        //Serial.print(gyro.y());
        //Serial.print(" ");
        //Serial.println(gyro.z());
        //Serial.print(accel.x());
        //Serial.print(" ");
        //Serial.print(accel.y());
        //Serial.print(" ");
        //Serial.println(accel.z());
        inverse_trig(accel.x(), accel.y(), accel.z(), &accel_angle);
        float alpha = accel_angle.alpha;
        float beta = accel_angle.beta;

        gyros.gyrox = gyro.x(); // dont really need a structure here, 
        gyros.gyroy = gyro.y();

        integrate_gyro(&gyros, &gprev, &g_angs, &arg);

        //Serial.print("integrated gyro x: ");
        //Serial.println(g_angs.gyro_xang);
        //Serial.print("accelerometer angle: ");
        //Serial.println(alpha);
  
        float ux = arg.omega*alpha + gyro.x();
        arg.ux = ux;
        float uy = arg.omega*beta + gyro.y();
        arg.uy = uy; // just wanna pass ux and uy directly into run_step

        run_step(&arg, &prev, &ret);

        //Serial.print("filtered x angle: ");
        //Serial.println(ret.return_value_x);
        //Serial.print("filtered y angle: ");
        //Serial.println(ret.return_value_y);

        anglesToQuat(&ret,&q);
        
        // print out the state of the button:
        String output1 = "Time: " + String(t);
        String output2 = "x: " + String(ret.return_value_x);
        String output3 = "y: " + String(ret.return_value_y);
        String output_full = output1 + "\t" + output2 + "\t" + output3;
        Serial.print(output_full + "\n");
         
        //print quaternians
        String q1 = "Q1: " + String(q.r);
        String q2 = "Q2: " + String(q.i);
        String q3 = "Q3: " + String(q.j);
        String q4 = "Q4 : " + String(q.k);
        String quat_full = q1 + "\t" + q2 + "\t" + q3 + "\t" + q4 + "\t";
        Serial.print(quat_full + "\n");

        float test = pow(q.r,2) + pow(q.i,2) + pow(q.j,2) + pow(q.k,2);
        Serial.print(String(test) + "\n");
        
        delay(arg.T*1000.0);
        
        break;
      } else {
        state = 0;
        break;
      }
  
  }

}

int run_step(struct args *arg, struct prev_data *prev, struct return_data *return_val){
    return_val->return_value_x = arg->a*(arg->T*prev->prev_ux1 + arg->T*prev->prev_ux2 - arg->b*prev->prev_yx);
    prev->prev_ux1 = arg->ux;
    prev->prev_ux2 = prev->prev_ux1;
    prev->prev_yx = return_val->return_value_x;
    return_val->return_value_y = arg->a*(arg->T*prev->prev_uy1 + arg->T*prev->prev_uy2 - arg->b*prev->prev_yy);
    prev->prev_uy1 = arg->uy;
    prev->prev_uy2 = prev->prev_uy1;
    prev->prev_yy = return_val->return_value_y;
    return 0;
}

int inverse_trig(float accelx, float accely, float accelz, struct accel_angles *accel_angle){
  // takes the accelerometer vector and produces the angles
  float tempx = 90 - 180.0*atan2(accelz,accely)/3.141593;
  float tempy = 90 - 180.0*atan2(accelz,accelx)/3.141593;

  accel_angle->alpha = tempx;
  accel_angle->beta = tempy;
  
  return 0;
}

int integrate_gyro(struct gyro_vals *gyros, struct gyro_prev *gprev, struct gyro_angles *angs, struct args *arg){
  angs->gyro_xang = arg->T/2.0*(gyros->gyrox + gprev->prev_gyrox) + gprev->prev_angx;
  angs->gyro_yang = arg->T/2.0*(gyros->gyroy + gprev->prev_gyroy) + gprev->prev_angy;
  gprev->prev_angx = angs->gyro_xang;
  gprev->prev_angy = angs->gyro_yang;
  gprev->prev_gyrox = gyros->gyrox;
  gprev->prev_gyroy = gyros->gyroy;
  
  return 0;
}
