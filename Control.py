# I'll start out with a simple test that aims to maintain a certain direction
import math
from Variables import *

def printA(x):
    x %= 360
    if x > 180:
        x = -180 + x-180
    return x
#sailData = {'-90': 0, '-89': 0, '-88': 1, '-87': 2, '-86': 3, '-85': 4, '-84': 5, '-83': 6, '-82': 7, '-81': 8, '-80': 9, '-79': 10, '-78': 11, '-77': 12, '-76': 13, '-75': 14, '-74': 15, '-73': 16, '-72': 17, '-71': 18, '-70': 19, '-69': 20, '-68': 21, '-67': 22, '-66': 23, '-65': 24, '-64': 25, '-63': 26, '-62': 27, '-61': 28, '-60': 29, '-59': 29, '-58': 28, '-57': 27, '-56': 26, '-55': 25, '-54': 24, '-53': 23, '-52': 22, '-51': 21, '-50': 20, '-49': 19, '-48': 18, '-47': 17, '-46': 16, '-45': 15, '-44': 14, '-43': 13, '-42': 12, '-41': 11, '-40': 10, '-39': 9, '-38': 8, '-37': 7, '-36': 6, '-35': 5, '-34': 4, '-33': 3, '-32': 2, '-31': 1, '-30': 0, '-29': 59, '-28': 58, '-27': 57, '-26': 56, '-25': 55, '-24': 65, '-23': 66, '-22': 67, '-21': 68, '-20': 69, '-19': 70, '-18': 71, '-17': 72, '-16': 73, '-15': 74, '-14': 75, '-13': 76, '-12': 77, '-11': 78, '-10': 79, '-9': 80, '-8': 81, '-7': 82, '-6': 82, '-5': 81, '-4': 80, '-3': 79, '-2': 78, '-1': 77, '0': 76, '1': 75, '2': 74, '3': 73, '4': 72, '5': 71, 
#'6': 70, '7': 69, '8': 68, '9': 67, '10': 66, '11': 65, '12': 64, '13': 63, '14': 62, '15': 61, '16': 60, '17': 59, '18': 58, '19': 57, '20': 56, '21': 55, '22': 54, '23': 53, '24': 52, '25': 51, '26': 50, '27': 49, '28': 48, '29': 47, '30': 46, '31': 45, '32': 44, '33': 43, '34': 42, '35': 41, '36': 40, '37': 39, '38': 38, '39': 37, '40': 36, '41': 35, '42': 34, '43': 33, '44': 32, '45': 31, '46': 30, '47': 29, '48': 28, '49': 27, '50': 26, '51': 25, '52': 24, '53': 23, '54': 22, '55': 21, '56': 20, '57': 19, '58': 18, '59': 17, '60': 16, '61': 15, '62': 14, '63': 13, '64': 12, '65': 11, '66': 10, '67': 9, '68': 8, '69': 7, '70': 6, '71': 5, '72': 4, '73': 3, '74': 2, '75': 1, '76': 0, '77': 0, '78': 0, '79': 0, '80': 0, '81': 0, '82': 0, '83': 0, '84': 0, '85': 0, '86': 0, '87': 0, '88': 1, '89': 0}
sailData = {'-90': 60, '-89': 59, '-88': 58, '-87': 57, '-86': 56, '-85': 55, '-84': 54, '-83': 53, '-82': 52, '-81': 51, '-80': 50, '-79': 49, '-78': 48, '-77': 47, '-76': 46, '-75': 45, '-74': 44, '-73': 43, '-72': 42, '-71': 41, '-70': 40, '-69': 39, '-68': 38, '-67': 37, '-66': 36, '-65': 35, '-64': 34, '-63': 33, '-62': 32, '-61': 31, '-60': 30, '-59': 29, '-58': 28, '-57': 27, '-56': 26, '-55': 25, '-54': 24, '-53': 23, '-52': 22, '-51': 21, '-50': 20, '-49': 19, '-48': 18, '-47': 17, '-46': 16, '-45': 15, '-44': 14, '-43': 13, '-42': 12, '-41': 11, '-40': 10, '-39': 9, '-38': 8, '-37': 7, '-36': 6, '-35': 5, '-34': 4, '-33': 3, '-32': 2, '-31': 1, '-30': 0, '-29': 0, '-28': 0, '-27': 0, '-26': 0, '-25': 0, '-24': 0, '-23': 0, '-22': 0, '-21': 0, '-20': 0, '-19': 0, '-18': 0, '-17': 0, '-16': 46, '-15': 45, '-14': 44, '-13': 43, '-12': 42, '-11': 41, '-10': 40, '-9': 39, '-8': 38, '-7': 37, '-6': 36, '-5': 35, '-4': 49, '-3': 48, '-2': 47, '-1': 46, '0': 45, '1': 44, '2': 43, '3': 42, '4': 41, '5': 40, '6': 39, '7': 38, '8': 37, '9': 36, '10': 35, '11': 34, '12': 33, '13': 35, '14': 36, '15': 37, '16': 38, '17': 39, '18': 40, '19': 40, '20': 40, '21': 39, '22': 38, '23': 37, '24': 36, '25': 35, '26': 34, '27': 33, '28': 32, '29': 31, '30': 30, '31': 29, '32': 28, '33': 27, '34': 26, '35': 
25, '36': 24, '37': 23, '38': 22, '39': 22, '40': 23, '41': 23, '42': 23, '43': 24, '44': 24, '45': 24, '46': 25, '47': 25, '48': 25, '49': 25, '50': 26, '51': 25, '52': 24, '53': 23, '54': 22, '55': 21, '56': 20, '57': 19, '58': 18, '59': 17, '60': 16, '61': 15, '62': 14, '63': 13, '64': 
12, '65': 11, '66': 10, '67': 9, '68': 8, '69': 7, '70': 6, '71': 5, '72': 4, '73': 3, '74': 2, '75': 1, '76': 0, '77': 0, '78': 0, '79': 0, '80': 0, '81': 0, '82': 0, '83': 0, '84': 0, '85': 0, '86': 0, '87': 0, '88': 1, '89': 0}
class Controler():
    def __init__(self,Boat, waypoint):
        self.boat = Boat
        self.waypoint = waypoint
        self.target_angle = Angle(1,0)
    def plan(self,plantype,waypoints):
        #type can either E(ndurance), S(tation Keeping), Pr(ecision Navigation), P(ayload),
        plantype = plantype.lower()
        if plantype == "e":
            # Format of waypoints is as such
            # 4 Buoy in order of navigation
            pass
        elif plantype == "s":
            #4 Buoy in any order
            pass
        elif plantype == "Pr":
            # 4 Buoy in order of navigation
            pass
    def setTarget(self,angle):
        self.target_angle = angle

    def update(self,dt,rNoise= 2,stability=1): # less noise = faster rotation, stability tries to limit angular momentum
        self.updateRudder(rNoise,stability)
        self.updateSails()
    def updateRudder(self,rNoise,stability):
        # dx = self.waypoint[0]-self.boat.position.xcomp()
        # dy = self.waypoint[1]-self.boat.position.ycomp()
        # target_angle = Angle(1,math.atan2(dy,dx)*180/math.pi)
        # target_angle = angle
        current_angle = self.boat.linearVelocity.angle
        dtheta = (self.target_angle - current_angle).calc()
        rotV = self.boat.rotationalVelocity*180/math.pi *0.03
        # coeff = 1-(1/(dtheta.calc()*(1/rotV)+1))
        dtheta = printA(dtheta)
        coeff = 2/math.pi * math.atan((dtheta)/40 - rotV/stability)
        self.boat.hulls[-1].angle = Angle(1,-10*coeff)*rNoise
        #print(dtheta,self.target_angle,coeff,-10*coeff,self.boat.hulls[-1].angle)
        # print(Angle.norm(self.boat.globalAparentWind().angle+Angle(1,180)))
    
    def updateSails(self):
        #print(Angle.norm(self.boat.globalAparentWind().angle+Angle(1,180)))
        # self.boat.sails[0].angle = (self.boat.globalAparentWind().angle+Angle(1,180)-Angle(1,38))
        print(str(printA(round(Angle.norm(self.boat.angle).calc()))))
        
        self.boat.sails[0].setSailRotation(Angle(1,sailData[str(printA(round(Angle.norm(self.boat.angle).calc())))]))
        # self.boat.sails[0].setSailRotation(self.boat.globalAparentWind().angle+Angle(1,180)-Angle(1,38))
        # self.boat.sails[0].setSailRotation(self.boat.globalAparentWind().angle+Angle(1,180)-Angle(1,38))
