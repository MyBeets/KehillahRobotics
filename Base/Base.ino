#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>
#include <SoftwareSerial.h>

RF24 radio(7, 8); // CE, CSN
#define VRY_PIN  A0 // Arduino pin connected to VRX pin
#define VRX_PIN  A1 // Arduino pin connected to VRY pin
const uint64_t pipes[2] = {0x63726C665FLL, 0x54617572E9}; //Send, Receive
// We have 32 byte package payload, arduino is an 8 bit architecutre, int is 2 bytes, long, float and double both 4 bytes, char is 1
typedef struct{
  byte type; // message type, plan: 0->e, 1->s, 2->pr, 3 is set
  long base[2];//reference point for the remainder of the coordinates
  word disp[3][2];
  char rtcm[10];
  bool rtk;
} emitPak; //size is 32

typedef struct{
  long pos[2];//reference point for the remainder of the coordinates
  int w_dir;
  int b_dir;
  byte mode;
} receivePak; //size is 8+2+2+1

typedef struct{//cords, wdir, bdir,mode
  long longitude;
  long latitude;
  long rudder;
  int wind;
  int rot;
  byte mode;
}Serialer;
typedef struct{//cords, wdir, bdir,mode
  byte mode;
  long co1;long co2;long co3;long co4;long co5;long co6;long co7;long co8;
}Serialy;
// SoftwareSerial rtcm = SoftwareSerial(2, 3);
void setup() {
  radio.begin();
  radio.openWritingPipe(pipes[0]);
  radio.openReadingPipe(1,pipes[1]);
  radio.setPALevel(RF24_PA_MAX);
  radio.setDataRate(RF24_250KBPS);
  // radio.setDataRate(RF24_1MBPS);
  radio.stopListening();
  Serial.begin(9600);
  // rtcm.begin(38400);
}
long rudder =0;
long sail = 0;
byte mode = 10;
void loop() {
  radio.stopListening();
  emitPak instr;
  instr.type = 10;//set
  // if (rtcm.available() > 0) {
    
  // //   int len = Serial.readString().toInt();
  //   char cor[10];// = (char)rtcm.read(); //= Serial.readString();
  //   for(int i=0; i<10; i++){
  //       cor[i] = rtcm.read();
  //   }
    
  //   // instr.rtcm = cor;
  //   strcpy(instr.rtcm,cor);
  //   instr.rtk = true;
  // //   instr.pos = len;
  // }else{
  //   instr.rtk = false;
  // }
  // rudder = (long)(((double)analogRead(VRX_PIN))/1023*40-20);
  // sail = (long)((double)(1023-analogRead(VRY_PIN))/1023*180-90);
  if (Serial.available() > 0) {
    Serialy input;
    Serial.readBytes((char*)&input, sizeof(input));
    mode = 10;//input.mode;
    instr.base[0] = input.co1;
    instr.base[1] = input.co2;
    // Serial.println(input.co2);
    if (instr.type == 10){//instr.type == 10
      long rd = (long)(((double)analogRead(VRX_PIN))/1023*40-20);
      long sd = (long)((double)(1023-analogRead(VRY_PIN))/1023*180-90);
      int num =5;
      if (rd>0){
        rudder +=num;
      }
      if (rd<0){
        rudder -=num;
      }
      if (sd<0){
        sail -=2;
      }
      if (sd>0){
        sail += 2;
      }
      // instr.base[0] = sail; //sail
      // instr.base[1] = rudder; //rudder
      // Serial.print("RUDDER");
      // Serial.println(rudder);
    }
    instr.disp[0][0] = (word)(input.co1-input.co3);
    instr.disp[0][1] = (word)(input.co2-input.co4);
    instr.disp[1][0] = (word)(input.co1-input.co5);
    instr.disp[1][1] = (word)(input.co2-input.co6);
    instr.disp[2][0] = (word)(input.co1-input.co7);
    instr.disp[2][1] = (word)(input.co2-input.co8);
  }
  instr.base[0] = sail; //sail
  instr.base[1] = rudder; //rudder
  instr.type = mode;
  radio.write(&instr, sizeof(instr));
  radio.startListening();
  // while (radio.available() == 0){};
  while(!radio.available());  
  receivePak data;
  radio.read(&data, sizeof(data));
  Serialer update;
  update.longitude = data.pos[0];
  update.latitude = data.pos[1];
  update.rudder = instr.base[1];
  update.wind = instr.base[0];//data.w_dir;
  update.rot = data.b_dir;
  update.mode = data.mode;
  Serial.write((char*)&update, sizeof(update));
  Serial.println();
  // radio.stopListening();
  delay(10);
}