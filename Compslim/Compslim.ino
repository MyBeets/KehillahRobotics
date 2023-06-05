// This is the code running on the computational arduino MEGA
// Comp gets radio, gyro and wind, gps
// Comp plans navs and executes them by relaying instructions to moter ardunio UNO
#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>
#include <Wire.h> //Needed for I2C to GNSS
// #include <SparkFun_u-blox_GNSS_Arduino_Library.h>
#include <math.h>
#include <REG.h>
// #include <wit_c_sdk.h>
// #define MAG_UPDATE		0x08
// #define READ_UPDATE		0x80
// static volatile char s_cDataUpdate = 0;

// static void SensorUartSend(uint8_t *p_data, uint32_t uiSize);
// static void SensorDataUpdata(uint32_t uiReg, uint32_t uiRegNum);
// static void Delayms(uint16_t ucMs);

const uint64_t pipes[2] = {0x54617572E9, 0x63726C665FLL}; //Send, Receive


// We have 32 byte package payload, arduino is an 8 bit architecutre, int and word is 2 bytes, long, float and double both 4 bytes, char is 1
//https://learn.sparkfun.com/tutorials/data-types-in-arduino/all
typedef struct{
  byte type; // message type, plan: 0->e, 1->s, 2->pr, 3 is set
  long base[2];//reference point for the remainder of the coordinates
  word disp[3][2];
  char rtcm[10];
  bool rtk;

} receivePak; //size is 1+8+12=21

typedef struct{
  long pos[2];//reference point for the remainder of the coordinates
  int w_dir;
  int b_dir;
  byte mode;
} emitPak; //size is 8+2+2

RF24 radio(7, 8); // CE, CSN
// SFE_UBLOX_GNSS GPS;
byte mode = 0;// modes: Standby:0, RC:1, Endurance:2, Station Keeping:3, Precision:4, Payload:5
long course[4*2][2];
byte index = 0; //course index 
byte course_size = 0;
double BVMG[2] = {63,150};
long latitude = 0;
long longitude = 0;
long gpsInterval = 0;
void setup() {
  Serial.begin(9600); // Pins 0,1 

  // Serial2.begin(38400); // Pins 17, 16 serves as GPS rtk data
  Serial3.begin(9600); //Pins 15(RX), 14(TX), communication with motor arduino
  // setGPS();
  setRadio();
}

void leg(long start[2], long stop[2], int w_dir, int b_dir){//leg adds start middle stop to course
    //w_dir is obviously the direction from which the true wind is coming
    course[course_size][0]= start[0];
    course[course_size++][1]= start[1];    
    int apparentAngle = abs(w_dir-w_dir)%180;
    if (apparentAngle < BVMG[0]){ // upwind
      // We want to get to stop only using the upwind BVMG
      //Cramer's rule
      double v1x = cos((w_dir+BVMG[0])*PI/180);
      double v1y = sin((w_dir+BVMG[0])*PI/180);
      double v2x = cos((w_dir-BVMG[0])*PI/180);
      double v2y = sin((w_dir-BVMG[0])*PI/180);
      double dx = stop[0]-start[0];
      double dy = stop[1]-start[1];
      double A = ((dx*v2y)-(dy*v2x))/((v1x*v2y)-(v1y*v2x));
      // course[course_size++] = {start[0]+v1x*A,start[1]+v1y*A};
      course[course_size][0]= start[0]+v1x*A;
      course[course_size++][1]= start[1]+v1y*A;
    }else if (apparentAngle > BVMG[1]){ //downwind
      double v1x = cos((w_dir+BVMG[1])*PI/180);
      double v1y = sin((w_dir+BVMG[1])*PI/180);
      double v2x = cos((w_dir-BVMG[1])*PI/180);
      double v2y = sin((w_dir-BVMG[1])*PI/180);
      double dx = stop[0]-start[0];
      double dy = stop[1]-start[1];
      double A = ((dx*v2y)-(dy*v2x))/((v1x*v2y)-(v1y*v2x));
      course[course_size][0]= start[0]+v1x*A;
      course[course_size++][1]= start[1]+v1y*A;
    }
    course[course_size][0]= stop[0];
    course[course_size++][1]= stop[1];
}
typedef struct{//cords, wdir, bdir,mode
  int sail;
  int rudder;
}data;
long baseSave[2];
word dispSave[3][2];
long stationTime;
void loop() {
  int b_dir = 90;//-boatDir();
  int w_dir = 0;
  int rot_v =0;
  int rudder;
  int sail;
  radio.startListening();
  delay(20);
  // Serial.println(radio.available());
  if (radio.available()) {
    receivePak instr;
    radio.read(&instr, sizeof(instr));
    status(instr, w_dir,b_dir);
    if (mode == 0){//manuel
      sail = instr.base[0];
      rudder = instr.base[1];
    }
  }
  radio.stopListening();
  // if (mode != 0){
  //   nextP(longitude, latitude);
  //   if (index == course_size){
  //     mode = 0;
  //   }else{
  //     if (index == course_size-1 && mode == 2){
  //       //endurance reset
  //       index = 0;
  //       course_size = 0;
  //       planEndurance(baseSave,dispSave, w_dir, b_dir);
  //     }
  //     rudder = rudderRot(2,1,longitude,latitude,b_dir,rot_v);
  //     sail = sailRot(w_dir, b_dir);

  //     //Station keeping and leaving
  //     if (mode == 3){
  //       if ((millis()-stationTime)/1000 > 300){//5m=300s
  //         mode = 0;
  //         rudder = 0;// this needs to be tested
  //       }else{
  //         if (index == course_size-1){
  //           planStation(baseSave,dispSave, w_dir, b_dir);
  //         }
  //       }
  //     }

  //   }
  // }
  // Serial3.print('<');
  // Serial3.print(sail);
  // Serial3.print(',');
  // Serial3.print(rudder);
  // Serial3.println('>');
  // Serial.println(GPS.getHeading());
  // Serial.println("PASS");
  Serial.println(rudder);
  data inp;
  inp.sail=sail;
  inp.rudder=rudder;
  Serial3.write((char*)&inp, sizeof(inp));
  emitPak resp;
  resp.pos[0] = longitude;
  resp.pos[1] = latitude;
  resp.w_dir = w_dir;
  resp.b_dir = b_dir;
  resp.mode = mode;
  radio.write(&resp, sizeof(resp));
  // Serial.println(radio.write(&resp, sizeof(resp)));
  // delay(10);
}

double distancedegree2meter(double lon1, double lat1, double lon2, double lat2){
  //haversine formula from http://www.movable-type.co.uk/scripts/latlong.html
  int R = 6371; // km
  double dLat = (lat2-lat1)*PI/180;
  double dLon = (lon2-lon1)*PI/180; 
  double a = sin(dLat/2) * sin(dLat/2) +
          cos(lat1*PI/180) * cos(lat2*PI/180) * 
          sin(dLon/2) * sin(dLon/2); 
  double c = 2 * atan2(sqrt(a), sqrt(1-a)); 
  return R * c;
}


void nextP(long lon, long lat){
  int r = 5;//5meter radius to play it safe
  if (distancedegree2meter((double)(lon)/10000000,(double)(lat)/10000000,(double)(course[index][0])/10000000,(double)(course[index][1])/10000000) < r) index++;
}

int rudderRot(int rNoise, int stability, long lon, long lat, int b_dir, int rot_v){
  long dy = (lat - course[index][1]);
  long dx = (lon - course[index][0]);
  double target_angle = atan2(dy,dx)*180/PI;

  double dtheta = target_angle - b_dir;
  rot_v *= 180/PI *0.03;

  dtheta = fmodf(dtheta,360);
  if (dtheta > 180) dtheta = -180 + dtheta-180;
  double coeff = 2/PI * atan((dtheta)/40 - rot_v/stability);
  return -10*coeff*rNoise;
}


int sailRot(int w_dir, int b_dir){
    w_dir = w_dir - b_dir;
    if (w_dir > 180) w_dir = -180 + w_dir-180;
    return 44/90*w_dir;
}

void planEndurance(long base[2],word disp[3][2], int w_dir, int b_dir){
  leg(new long[2]{longitude,latitude},new long[2]{base[0],base[1]}, w_dir, b_dir);
  course_size--;
  leg(new long[2]{base[0],base[1]},new long[2]{base[0]+disp[0][0],base[1]+disp[0][1]}, w_dir, b_dir);
  course_size--;
  leg(new long[2]{base[0]+disp[0][0],base[1]+disp[0][1]},new long[2]{base[0]+disp[1][0],base[1]+disp[1][1]}, w_dir, b_dir);
  course_size--;
  leg(new long[2]{base[0]+disp[1][0],base[1]+disp[1][1]},new long[2]{base[0]+disp[2][0],base[1]+disp[2][1]}, w_dir, b_dir);
  course_size--;
  long middle[2] = {(base[0]+disp[2][0]+longitude)/2,(latitude+base[1]+disp[2][1])/2};
  leg(new long[2]{base[0]+disp[2][0],base[1]+disp[2][1]},middle, w_dir, b_dir);
}
void planPrecision(long base[2],word disp[3][2], int w_dir, int b_dir){
  leg(new long[2]{longitude,latitude},new long[2]{base[0]+disp[0][0],base[1]+disp[0][1]}, w_dir, b_dir);
  course_size--;
  leg(new long[2]{base[0]+disp[0][0],base[1]+disp[0][1]},new long[2]{base[0]+disp[1][0],base[1]+disp[1][1]}, w_dir, b_dir);
  course_size--;
  long middle[2] = {(2*base[0]+disp[2][0])/2,(2*base[1]+disp[2][1])/2};
  leg(new long[2]{base[0]+disp[1][0],base[1]+disp[1][1]},middle, w_dir, b_dir);
}
void planStation(long base[2],word disp[3][2], int w_dir, int b_dir){
  long last[2] = {longitude,latitude};
  long waypoints[4][2] = {{base[0],base[1]},{base[0]+disp[0][0],base[1]+disp[0][1]},{base[0]+disp[1][0],base[1]+disp[1][1]},{base[0]+disp[2][0],base[1]+disp[2][1]}};
  for (uint8_t i = -1; i < 3; i++){
    long avg[2] = {(waypoints[i%4][0]+waypoints[(i+1)%4][0])/2,(waypoints[i%4][1]+waypoints[(i+1)%4][1])/2};
    long angle = atan2((waypoints[i%4][1]-waypoints[(i+1)%4][1]),(waypoints[i%4][0]-waypoints[(i+1)%4][0]))+PI/2;
    long l = sqrt(sq(waypoints[(i+1)%4][1]-waypoints[(i+2)%4][1])+sq(waypoints[(i+1)%4][0]-waypoints[(i+2)%4][0]))/8;
    avg[0] -= cos(angle)*l;
    avg[1] -= sin(angle)*l;
    leg(last, avg, w_dir, b_dir);
    course_size--;
    last[0] = avg[0];
    last[1] = avg[1];
  }
}

void save(long baseS[2], word dispS[3][2]){
  baseSave[0] = baseS[0];
  baseSave[1] = baseS[1];
  for (int x = 0; x< 3;x++){
    for (int y = 0; y< 2;y++){
      dispSave[x][y] = dispS[x][y];
    }
  }
}


void status(receivePak instr,int w_dir, int b_dir){
  // message type, plan: 0->e, 1->s, 2->pr, 3-> payload, 10 is set
  if (instr.type == 0){ //endurance
    mode = 2;
    planEndurance(instr.base,instr.disp, w_dir, b_dir);
    save(instr.base, instr.disp);
  }else if (instr.type == 1){ //station
    mode = 3;
    planStation(instr.base,instr.disp, w_dir, b_dir);
    save(instr.base, instr.disp);
    stationTime = millis();
  }else if (instr.type == 2){ //precision
    mode = 4;
    planPrecision(instr.base,instr.disp, w_dir, b_dir);
    save(instr.base, instr.disp);
  }else if (instr.type == 3){ //payload
    mode = 5;
    save(instr.base, instr.disp);
  }else if (instr.type == 10){//set
    //set
    mode = 0;
  }
}
// void setGPS(){
//   Wire.begin();
//   if (GPS.begin() == false){
//     Serial.println(F("u-blox GNSS not detected at default I2C address. Please check wiring. Freezing."));
//     while (1);
//   }
//   GPS.setI2COutput(COM_TYPE_UBX); //Set the I2C port to output UBX only (turn off NMEA noise)
//   GPS.saveConfigSelective(VAL_CFG_SUBSEC_IOPORT); //Save (only) the communications port settings to flash and BBR
//   GPS.setPortInput(COM_PORT_I2C, COM_TYPE_UBX | COM_TYPE_NMEA | COM_TYPE_RTCM3); //Be sure RTCM3 input is enabled. UBX + RTCM3 is not a valid state.
//   GPS.setNavigationFrequency(1); //Set output in Hz.
// }
void setRadio(){
  // radio.setAutoAck(true);
  radio.begin();
  radio.openWritingPipe(pipes[0]);
  radio.openReadingPipe(1,pipes[1]);
  radio.setPALevel(RF24_PA_MAX);
  radio.setDataRate(RF24_250KBPS);
  // radio.setDataRate(RF24_1MBPS);
  radio.stopListening();
}

// static void SensorUartSend(uint8_t *p_data, uint32_t uiSize)
// {
//   Serial1.write(p_data, uiSize);
//   Serial1.flush();
// }
// static void Delayms(uint16_t ucMs)
// {
//   delay(ucMs);
// }
// static void SensorDataUpdata(uint32_t uiReg, uint32_t uiRegNum)
// {
// 	int i;
//     for(i = 0; i < uiRegNum; i++)
//     {
//         switch(uiReg)
//         {

//             case HZ:
// 				s_cDataUpdate |= MAG_UPDATE;
//             break;
//             default:
// 				s_cDataUpdate |= READ_UPDATE;
// 			break;
//         }
// 		uiReg++;
//     }
// }
// // star.setLen(instr.pos);
// //  cont.setAngle(instr.pos);

// //GPS methods
// // long speed = myGNSS.getGroundSpeed();
// // Serial.print(F(" Speed: "));
// // Serial.print(speed);
// // Serial.print(F(" (mm/s)"));

// // long heading = myGNSS.getHeading();
// // Serial.print(F(" Heading: "));
// // Serial.print(heading);
// // Serial.print(F(" (degrees * 10^-5)"));
// // long latitude = myGNSS.getLatitude();//do remember to not poll GPS much more than 1hz
// // long longitude = myGNSS.getLongitude();
// // int32_t latitude = myGNSS.getHighResLatitude();
// // int32_t longitude = myGNSS.getHighResLongitude();
