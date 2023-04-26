const int time = 500;

class Stepper{
  public:
    const int stepPin,dirPin,enPin;
    double length; // length in centimeters
    Stepper(int step, int dir, int en, double len){
      stepPin = step;
      pinMode(stepPin,OUTPUT); 
      dirPin = dir;
      pinMode(dirPin,OUTPUT);
      enPin = en;
      pinMode(enPin,OUTPUT);
      length = len;
    }
    void lengthInit(){
      setLen(length-3);
    }
    void setLen(int len){
      for (int i =0; i < abs(length-len); i++){
          digitalWrite(dirPin,(length-len) >= 0);
          step();
      }
    }
    void lock(){
      digitalWrite(enPin,HIGH); 
      delayMicroseconds(time); 
      digitalWrite(enPin,LOW); 
    }
  private:
    void step(){
      digitalWrite(stepPin,HIGH); 
      delayMicroseconds(time); 
      digitalWrite(stepPin,LOW);
      delayMicroseconds(time);
    }
};
void setup() {
  Stepper star(5,2,8,0); //starboard winch
  Serial.begin(9600);
  star.lengthInit()

  // lengthInit();
}
void loop() {
  if (Serial.available()){
    int pos = Serial.readString().toInt();
    Serial.print(dir);
    star.setLen(dir);
  }else{
    star.lock()
  }
}


  // if (dir == 2){
  //   digitalWrite(enPin,HIGH); 
  //   delayMicroseconds(time); 
  //   digitalWrite(enPin,LOW); 
  // }else{
  //   if (dir ==1){
  //     digitalWrite(dirPin,HIGH);
  //   }else{
  //     digitalWrite(dirPin,LOW);
  //   }
  //   digitalWrite(stepPin,HIGH); 
  //   delayMicroseconds(time); 
  //   digitalWrite(stepPin,LOW);
  //   delayMicroseconds(time);
  // }
  // delay(1000); 

