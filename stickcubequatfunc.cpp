#include "quat.h"

struct angles {
  float theta_x;
  float theta_y;
};
struct quat {
  float r;
  float i;
  float j;
  float k;
};
void setup() {
  Serial.begin(9600);
  // put your setup code here, to run once:

}

void loop() {
  // put your main code here, to run repeatedly:

}

int anglesToQuat(struct angles *ang, struct quat *q) {

  float tanx  = (180.0/PI)* tan(ang->theta_x); //taking tangents of values
  float tany = (180.0/PI)*tan(ang->theta_y);
  
  float a_x = tanx*sqrt(pow(tany,2) + pow(tanx,2));
  float a_y = tany*sqrt(pow(tany,2) + pow(tanx,2));
  float a_z = 0.0;
  
  float phi = acos(1/(sqrt(pow(tany,2) + pow(tanx,2)+1)));
  float sin_phi = sin(phi/2);

  float eta = 1/(2*(sqrt(pow(tany,2) + pow(tanx,2)+1)));
  
  q->r = eta;
  q->i = sin_phi*a_x;
  q->j = sin_phi*a_y;
  q->k = 0;
  
  
  
  

  
  
  
 
  
}