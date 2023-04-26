int t_dir = -1;
int pin_dir = 3;
int pin_speed = 2;
int speed = -1; //radians per second
int direction = 0; //radians
#define PI 3.1415926535897932384626433832795
void setup() {
  Serial.begin(9600);
  pinMode(pin_speed, INPUT);
  pinMode(pin_dir, INPUT);
}

void loop() {
  if (digitalRead(pin_speed)){// if we've compleated a roation around the direction thing
    int delta_speed = t_speed;
    if (t_speed == -1){
      delta_speed= micros();
    }else{
      delta_speed = micros() - delta_speed;
    }
    t_speed = micros();
    speed = (2*PI)/delta_dir;
  }
  if (digitalRead(pin_dir) && speed != -1){ // if we've compleated a roation
    int delta_dir = micros() - t_speed;
    direction = delta_dir*speed;
    Serial.print(speed*PI/180);
    Serial.print(",");
    Serial.println(direction*PI/180);
  }
}
