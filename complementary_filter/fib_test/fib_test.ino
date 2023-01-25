
//unsigned int sleep(unsigned int seconds);

struct return_data {
    int return_value;
};

struct prev_data {
    int fib1;
    int fib2;
};

struct args{
    int step_value;
};

struct return_data ret;
struct prev_data prev;
struct args arg;
//ret.return_value = 0;
//prev.fib1 = 0;
//prev.fib2 = 1;


void setup(){
    Serial.begin(9600);
    ret.return_value = 0;
    prev.fib1 = 0;
    prev.fib2 = 1;
}


void loop() {
  // put your main code here, to run repeatedly:
  //struct args arg;
  //struct prev_data prev;
  //struct return_data ret;
  run_step(&arg, &prev, &ret);
  Serial.println(ret.return_value);
  //sleep(1);
  delay(1000);
}

int run_step(struct args *arg, struct prev_data *prev, struct return_data *return_val){
    return_val->return_value = prev->fib1 + prev->fib2;
    prev->fib1 = prev->fib2;
    prev->fib2 = return_val->return_value;
    return 0;
}
