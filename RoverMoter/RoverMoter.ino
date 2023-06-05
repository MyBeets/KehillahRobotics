#include <Servo.h>
#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>

const int time = 150;

class Stepper{
  public:
    int stepPin,dirPin,enPin;
    bool direction = true;
    double length; // length in centimeters
    int ppr = 3200;//pulse per revolution
    int radius = 2;// 2cm
    bool side;
    double circ = 2*3.1415*radius;
    Stepper(int step, int dir, int en, double len, bool flip){
      stepPin = step;
      pinMode(stepPin,OUTPUT); 
      dirPin = dir;
      pinMode(dirPin,OUTPUT);
      enPin = en;
      pinMode(enPin,OUTPUT);
      length = len;
      side = flip;
    }
    void lock(){
      digitalWrite(enPin,HIGH); 
      delayMicroseconds(time); 
      digitalWrite(enPin,LOW); 
    }
    void step(){
      digitalWrite(stepPin,HIGH); 
      delayMicroseconds(time); 
      digitalWrite(stepPin,LOW);
      delayMicroseconds(time);
      if (direction){
        length -= circ/ppr;
      }else{
        length += circ/ppr;
      }
    }
    void setDir(bool dir){
      direction = dir;
      if (side) dir = !dir;
      if (dir){ //I know
        digitalWrite(dirPin,HIGH);
      }else{
        digitalWrite(dirPin,LOW);
      }
    }
};

double distance(double x1, double y1, double x2, double y2){
  return sqrt(sq(x1-x2)+sq(y1-y2));
}

class Controller{
  public:
    Stepper babord;
    Stepper tribord;
    Controller(const Stepper& _babord, const Stepper& _tribord);
    Stepper _babord() const;
    Stepper _tribord() const;
    double length=100;
    void setAngle(double angle){
      //for this we assume x direction is torwards the front of the boat
      angle = abs(angle);
      angle += 180;//flip it
      int dist2mast = 107; //cm
      int boom = 150;
      double sx = dist2mast + cos(angle*PI/180)*boom;
      double sy = sin(angle*PI/180)*boom;
      double w1x = 0;
      double w1y = 100;
      double w2x = 0;
      double w2y = -100;
      double dist = max(distance(sx,sy,w1x,w1y),distance(sx,sy,w2x,w2y));
      length = dist;
      // setLen(dist);
    }
    void update(){
      int stepn = round(abs(babord.length-length)*babord.ppr/babord.circ);
      for (int i =0; i < floor(stepn/5); i++){
        babord.setDir((length-babord.length) < 0);
        tribord.setDir((length-tribord.length) < 0);
        babord.step();
        tribord.step();
      }
    }
    // void setLen(double len){
    //   int stepn = round(abs(babord.length-len)*babord.ppr/babord.circ);
    //   for (int i =0; i < stepn; i++){
    //     babord.setDir((len-babord.length) < 0);
    //     tribord.setDir((len-tribord.length) < 0);
    //     babord.step();
    //     tribord.step();
    
    //   }
    // }
};

// Controller::Controller(const Stepper& _babord, const Stepper& _tribord){
//   babord(_babord);
//   tribord(_tribord);
// }

Controller::Controller(const Stepper& _babord, const Stepper& _tribord) 
    : babord(_babord), tribord(_tribord)  
{
}

typedef struct{//cords, wdir, bdir,mode
  int sail;
  int rudder;
}data;

Stepper babord(4,3,2,100,0); //babord winch
Stepper tribord(12,11,10,100,1); //tribord step dir enable
Controller cont(babord,tribord);
int servoPin = 8;
Servo rudder;
void setup() {
  Serial.begin(38400);
  rudder.attach(servoPin);
  rudder.write(25);
}

void loop(){
  data inp;
  if (Serial.available()>0){
    Serial.readBytes((char*)&inp, sizeof(inp));
    cont.setAngle(inp.sail);
    rudder.write(inp.rudder+25);
    Serial.print("Sail:");
    Serial.println(inp.sail);
    Serial.print("Rudder:");
    Serial.println(inp.rudder);
  }
  cont.update();
}
  // if (radio.available()) {
  //   receivePak instr;
  //   radio.read(&instr, sizeof(instr));

  //   if (instr.type == 0){ //set
  //     // star.setLen(instr.pos);
  //     cont.setAngle(instr.pos);
  //   }
  //   if (instr.type == 1){ //release
  //     rudder.write(instr.pos); 
  //   }
  // }
