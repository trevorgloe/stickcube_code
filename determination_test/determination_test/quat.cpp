#include "quat.h"

struct return_data {
  float return_value_x;
  float return_value_y;
};

struct quat {
  float r;
  float i;
  float j;
  float k;
};


int anglesToQuat(struct return_data *ang, struct quat *q) {

  // convert angles from degrees to radians
  float rad_angx = 3.14159/180.0 * ang->return_value_x;
  float rad_angy = 3.14159/180.0 * ang->return_value_y;
  
  float tanx  = tan(rad_angx); //taking tangents of values
  float tany = tan(rad_angy);
  
  float a_x = tanx*sqrt(pow(tany,2) + pow(tanx,2));
  float a_y = tany*sqrt(pow(tany,2) + pow(tanx,2));
  float a_z = 0.0;

  float a_mag = sqrt(pow(a_x,2) + pow(a_y,2) + pow(a_z,2));
  a_x = a_x / a_mag;
  a_y = a_y / a_mag;
  a_z = a_z / a_mag;
  
  float phi = acos(1.0/(sqrt(pow(tany,2) + pow(tanx,2)+1)));
  float sin_phi = sin(phi/2.0);

  float eta = cos(phi/2.0);
  
  q->r = eta;
  q->i = sin_phi*a_x;
  q->j = sin_phi*a_y;
  q->k = 0;
  
  
  
  

  
  
  
 
  
}
