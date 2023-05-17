//time Variables and switches
bool dir_switch = false;
double t_speed = 0;
bool speed_switch = false;

//Pins
int pin_dir = 2; //orange
int pin_speed = 3; //yellow

// Interesting variables
double speed = 0; //radians per second
double direction = 0; //radians
const double radius = 9.52;

#define PI 3.1415926535897932384626433832795
void setup() {
  Serial.begin(9600);
  pinMode(pin_speed, INPUT);
  pinMode(pin_dir, INPUT);
  t_speed = micros();
}

void loop() {
  //Serial.println(digitalRead(pin_speed));
  if (digitalRead(pin_speed)){ // if we've compleated a rotation
    if (!speed_switch){
      double delta_speed = (micros() - t_speed)/1000000.0;
      speed = radius*(2*PI)/delta_speed;
      speed_switch = true;
      t_speed = micros();
    }
  }else{
    speed_switch = false;
  }

  if (digitalRead(pin_dir)){ // if we've compleated a rotation
    if (!dir_switch){
      double delta_dir = (micros() - t_speed)/1000000.0;
      direction = (delta_dir * speed)/(radius*(2*PI))
      dir_switch = true;
    }
  }else{
    dir_switch = false;
  }
  
  if ((micros() - t_speed)/1000000.0 > radius*(2*PI)*speed){
    // if we've slowed down and not hit the rotation point yet
    Serial.print("Speed: ");
    Serial.println(radius*(2*PI)/((micros() - t_speed)/1000000.0));
  }else{
    Serial.print("Speed: ");
    Serial.println(speed);
  }
  Serial.print("Direction: ");
  Serial.println(direction*360);
  delay(10);
}
