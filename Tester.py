
from Foil import foil
from Variables import *
from Boat import Boat
import os
import re

data_dir = os.path.dirname(__file__) #abs dir

def color(fail):
    if fail==0:
        return '.  \x1b[6;30;42m' + 'Success!' + '\033[0m'
    else:
        return '.  \x1b[7;31;40m' + 'Failure!' + '\033[0m'

def rm_ansi(line):
    ansi_escape =re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]')
    return ansi_escape.sub('', line)

def VariableTest():
    pas = 0;fail = 0
    #Basic Variable Class:
    basicVar = Variable(1,10)#calc
    pas+= basicVar.data() == 10;fail+= basicVar.data() != 10
    pas+= basicVar.calc() == 10;fail+= basicVar.calc() != 10
    pas+= basicVar.display() == 10;fail+= basicVar.display() != 10
    pas+= basicVar.type == 1;fail+= basicVar.type != 1
    pas+= rm_ansi(str(basicVar)) == "Calc: 10.0";fail+= rm_ansi(str(basicVar)) != "Calc: 10.0"
    basicVar.changeType(2)
    pas+= basicVar.data() == 10;fail+= basicVar.data() != 10
    pas+= basicVar.calc() == 10;fail+= basicVar.calc() != 10
    pas+= basicVar.display() == 10;fail+= basicVar.display() != 10  
    pas+= basicVar.type == 2;fail+= basicVar.type != 2
    print("Variable, passed: " + str(pas) + ", failed: " + str(fail)+ ", of: " +str(pas+fail) + color(fail))
    pas = 0;fail = 0

    #Basic Angle Class:
    calcAngle = Angle(1, 40) # calc
    pas+= rm_ansi(str(calcAngle)) == "Angle: Calc: 40.0";fail+= rm_ansi(str(calcAngle)) != "Angle: Calc: 40.0"
    pas+= calcAngle.calc2display() == 140;fail+= calcAngle.calc2display() != 140
    pas+= calcAngle.display() == 140;fail+= calcAngle.display() != 140
    pas+= calcAngle.calc2data() == 50;fail+= calcAngle.calc2data() != 50
    pas+= calcAngle.data() == 50;fail+= calcAngle.data() != 50
    pas+= calcAngle.calc() == 40;fail+= calcAngle.calc() != 40
    pas+= calcAngle.type == 1;fail+= calcAngle.type != 1
    basicVar.changeType(2)
    pas+= calcAngle.display() == 140;fail+= calcAngle.display() != 140
    pas+= calcAngle.data() == 50;fail+= calcAngle.data() != 50
    pas+= calcAngle.calc() == 40;fail+= calcAngle.calc() != 40
    pas+= basicVar.type == 2;fail+= basicVar.type != 2
    print("Calc Angle, passed: " + str(pas) + ", failed: " + str(fail)+ ", of: " +str(pas+fail) + color(fail))
    pas = 0;fail = 0

    dataAngle = Angle(0, 90)#data
    pas+= dataAngle.data2calc() == 0;fail+= dataAngle.data2calc() != 0
    pas+= dataAngle.calc() == 0;fail+= dataAngle.calc() != 0
    pas+= dataAngle.data2display() == 180;fail+= dataAngle.data2display() != 180
    pas+= dataAngle.display() == 180;fail+= dataAngle.display() != 180
    pas+= dataAngle.data() == 90;fail+= dataAngle.data() != 90
    pas+= dataAngle.type == 0;fail+= dataAngle.type != 0
    dataAngle.changeType(2)
    pas+= dataAngle.calc() == 0;fail+= dataAngle.calc() != 0
    pas+= dataAngle.display() == 180;fail+= dataAngle.display() != 180
    pas+= dataAngle.data() == 90;fail+= dataAngle.data() != 90
    pas+= dataAngle.type == 2;fail+= dataAngle.type != 2
    print("Data Angle, passed: " + str(pas) + ", failed: " + str(fail)+ ", of: " +str(pas+fail) + color(fail))
    pas = 0;fail = 0

    displayAngle = Angle(2, 0)#display
    pas+= displayAngle.display2calc() == 180;fail+= displayAngle.display2calc() != 180
    pas+= displayAngle.calc() == 180;fail+= displayAngle.calc() != 180
    pas+= displayAngle.display2data() == -90;fail+= displayAngle.display2data() != -90
    pas+= displayAngle.data() == -90;fail+= displayAngle.data() != -90
    pas+= displayAngle.display() == 0;fail+= displayAngle.display() != 0
    pas+= dataAngle.type == 2;fail+= dataAngle.type != 2
    dataAngle.changeType(0)
    pas+= displayAngle.calc() == 180;fail+= displayAngle.calc() != 180
    pas+= displayAngle.data() == -90;fail+= displayAngle.data() != -90
    pas+= displayAngle.display() == 0;fail+= displayAngle.display() != 0
    pas+= dataAngle.type == 0;fail+= dataAngle.type != 0
    print("Display Angle, passed: " + str(pas) + ", failed: " + str(fail)+ ", of: " +str(pas+fail) + color(fail))
    pas = 0;fail = 0

    #Simple Vector
    v1 = Vector(Angle(1,10),10)
    v2 = Vector(Angle(1,10),10)
    v3 = v1+v2
    v4 = v1-v2
    v5 = v3+v4
    pas+= v3.angle.calc() == 10.0;fail+= v3.angle.calc() !=10.0
    pas+= v3.speed() == 20;fail+= v3.speed() != 20
    pas+= round(v4.angle.calc()) == 0;fail+= round(v4.angle.calc()) !=0
    pas+= v4.speed() == 0;fail+= v4.speed() != 0
    pas+= v5.angle.calc() == 10.0;fail+= v5.angle.calc() !=10.0
    pas+= v5.speed() == 20;fail+= v5.speed() != 20
    #Harder Vector calculations
    v6 = Vector(Angle(1,10),10)
    v7 = Vector(Angle(1,-20),-5.5) # 160 with norm 5.5
    v8 = v6+v7
    pas+= v8.angle.calc() == 37.705;fail+= v8.angle.calc() !=37.705
    pas+= v8.speed() == 5.915;fail+= v8.speed() != 5.915
    print("Vector, passed: " + str(pas) + ", failed: " + str(fail)+ ", of: " +str(pas+fail) + color(fail))
    pas = 0;fail = 0

def FoilTest():
    pas = 0; fail = 0
    sail = foil(data_dir+"\\data\\mainSailCoeffs.cvs", 0.128, 1)
    #read method for mainsail lift coeffeciants
    pas+= sail.liftC[0][0].data() == 0;fail+=sail.liftC[0][0].data() != 0 
    pas+= sail.liftC[0][0].calc() == 90;fail+=sail.liftC[0][0].calc() != 90 
    pas+= sail.liftC[0][0].display() == 90;fail+=sail.liftC[0][0].display() != 90 
    pas+= sail.liftC[0][1] == 0 ;fail+=sail.liftC[0][1] != 0 
    pas+= sail.liftC[4][0].data() == 14 ;fail+=sail.liftC[4][0].data() != 14 #the data is halved that's why it's 14 not 28 
    pas+= sail.liftC[9][0].data() == 90 ;fail+=sail.liftC[9][0].data() != 90 
    pas+= sail.liftC[9][0].calc() == 0 ;fail+=sail.liftC[9][0].calc() != 0
    pas+= sail.liftC[9][0].display() == 180;fail+=sail.liftC[9][0].display() != 180 
    
    print("Data Read, passed: " + str(pas) + ", failed: " + str(fail)+ ", of: " +str(pas+fail) + color(fail))
    pas = 0;fail = 0

    #linear interpolation and reading
    pas+= float(sail.cd(Angle(0,45))) == 0.3825;fail+= float(sail.cd(Angle(0,45))) != 0.3825
    pas+= float(sail.cl(Angle(0,14))) == 1.42681;fail+= float(sail.cl(Angle(0,14))) != 1.42681
    pas+= float(sail.cl(Angle(0,100))) == 0.22126333333333334;fail+= float(sail.cl(Angle(0,100))) != 0.22126333333333334

    print("Reading and Linear Interpoltion, passed: " + str(pas) + ", failed: " + str(fail)+ ", of: " +str(pas+fail) + color(fail))
    pas = 0;fail = 0

    hull = foil(data_dir+"\\data\\xf-naca001034-il-1000000-Ex.csv", 1, 0.5)

    #read method for hull drag coeffeciants
    pas+= hull.dragC[0][0].data() == 0;fail+=hull.dragC[0][0].data() != 0
    pas+= hull.dragC[0][1] == 0.0067;fail+=hull.dragC[0][1] != 0.0067
    pas+= hull.dragC[10][1] == 0.0159;fail+=hull.dragC[10][1] != 0.0159
    pas+= hull.dragC[15][1] == 0.1170;fail+=hull.dragC[15][1] != 0.1170

    print("Coeffeciant Reading, passed: " + str(pas) + ", failed: " + str(fail)+ ", of: " +str(pas+fail) + color(fail))
    pas = 0;fail = 0

    # lift and drag methods
    pas+= hull.lift(Vector(Angle(1,45)-Angle(1,180),10)) == 27.125;fail+=hull.lift(Vector(Angle(1,45)-Angle(1,180),10)) != 27.125
    pas+= hull.lift(Vector(Angle(1,90)-Angle(1,180),10)) == 0;fail+=hull.lift(Vector(Angle(1,90)-Angle(1,180),10)) != 0
    pas+= hull.lift(Vector(Angle(1,270)-Angle(1,180),10)) == 0;fail+=hull.lift(Vector(Angle(1,270)-Angle(1,180),10)) != 0
    pas+= hull.drag(Vector(Angle(1,270)-Angle(1,180),10)) <= 1;fail+=hull.drag(Vector(Angle(1,270)-Angle(1,180),10)) > 1
    pas+= hull.drag(Vector(Angle(1,-10)-Angle(1,180),10)) >= 40;fail+=hull.drag(Vector(Angle(1,-10)-Angle(1,180),10)) < 40

    print("L/D methods, passed: " + str(pas) + ", failed: " + str(fail)+ ", of: " +str(pas+fail) + color(fail))
    pas = 0;fail = 0

def BoatTest():
    data_dir = os.path.dirname(__file__) #abs dir
    hull = foil(data_dir+"\\data\\xf-naca001034-il-1000000-Ex.csv", 1, 0.5)
    sail = foil(data_dir+"\\data\\mainSailCoeffs.cvs", 0.128, 1)
    wind = Vector(Angle(1,270),10) # Going South wind, 10 m/s
    boat = Boat([hull],[sail],wind)
    pas = 0; fail = 0

    #Wind
    wind.angle += Angle(1,10) # now wind is going 280* calc south
    pas+= rm_ansi(str(boat.wind)) == "Vector, norm: 10, Angle: Calc: 280.0"; fail+=rm_ansi(str(boat.wind)) != "Vector, norm: 10, Angle: Calc: 280.0"
    pas+= boat.wind.angle.data() == 190; fail+=boat.wind.angle.data() != 190
    print("Wind, passed: " + str(pas) + ", failed: " + str(fail)+ ", of: " +str(pas+fail) + color(fail))
    pas = 0;fail = 0

    #Global Aparent Wind
    pas+= boat.globalAparentWind().angle.calc() == -80; fail+=boat.globalAparentWind().angle.calc() != -80
    pas+= boat.globalAparentWind().speed() == 10.0;fail+= boat.globalAparentWind().speed() != 10.0
    wind.angle -= Angle(1,10)
    boat.velocity.norm += 10
    pas+= boat.globalAparentWind().angle.calc() == -90;fail+= boat.globalAparentWind().angle.calc() != -90
    pas+= boat.globalAparentWind().speed() == 20.0; fail+= boat.globalAparentWind().speed() != 20.0
    boat.velocity.norm -= 20
    pas+= boat.globalAparentWind().angle.calc() == 0; fail+= boat.globalAparentWind().angle.calc() != 0
    pas+= boat.globalAparentWind().speed() == 0.0; fail+= boat.globalAparentWind().speed() != 0.0
    wind.angle += Angle(1,35)
    boat.velocity.norm = 10
    pas+= boat.globalAparentWind().angle.calc() == -72.5; fail+= boat.globalAparentWind().angle.calc() != -72.5
    pas+= boat.globalAparentWind().speed() == 19.0743; fail+= boat.globalAparentWind().speed() != 19.0743
    print("Global Aparent Wind, passed: " + str(pas) + ", failed: " + str(fail)+ ", of: " +str(pas+fail) + color(fail))
    pas = 0;fail = 0

    #Local Aparent Wind
    wind.angle = Angle(1,270)
    pas+= boat.sailAparentWind().angle.calc() == 360-90; fail+= boat.sailAparentWind().angle.calc() != 360-90
    pas+= boat.sailAparentWind().speed() == 20; fail+= boat.sailAparentWind().speed() != 20
    wind.angle = Angle(1,225)
    boat.velocity.norm = 0
    pas+= boat.sailAparentWind().angle.calc() == 360-135; fail+= boat.sailAparentWind().angle.calc() != 360-135
    pas+= boat.sailAparentWind().speed() == 10; fail+= boat.sailAparentWind().speed() != 10
    boat.velocity.norm = 5
    pas+= boat.sailAparentWind().angle.calc() == 360-120.3612; fail+= boat.sailAparentWind().angle.calc() != 360-120.3612
    pas+= boat.sailAparentWind().speed() == 13.9897; fail+= boat.sailAparentWind().speed() != 13.9897
    boat.velocity.norm = 10
    boat.velocity.angle += Angle(1,15)
    pas+= boat.sailAparentWind().angle.calc() == 360-105.0; fail+= boat.sailAparentWind().angle.calc() != 360-105.0
    pas+= boat.sailAparentWind().speed() == 17.3205; fail+= boat.sailAparentWind().speed() != 17.3205
    boat.velocity.angle -= Angle(1,15)
    boat.velocity.norm = 0
    boat.sails[0].angle += Angle(1,15)
    pas+= boat.sailAparentWind().angle.calc() == 360-150; fail+= boat.sailAparentWind().angle.calc() != 360-150
    pas+= boat.sailAparentWind().speed() == 10; fail+= boat.sailAparentWind().speed() != 10
    boat.velocity.norm = 0
    boat.sails[0].angle = Angle(1,10)
    wind.angle = Angle(1,225)
    pas+= boat.sailAparentWind().angle.calc() == 360-145.0; fail+= boat.sailAparentWind().angle.calc() != 360-145.0
    pas+= boat.sailAparentWind().speed() == 10; fail+= boat.sailAparentWind().speed() != 10
    print("Local Aparent Wind, passed: " + str(pas) + ", failed: " + str(fail)+ ", of: " +str(pas+fail) + color(fail))
    pas = 0;fail = 0

    boat.angle = Angle(1,75)
    boat.sails[0].angle = Angle(1,70)
    wind.angle = Angle(1,0)
    aparentForce = boat.sails[0].dragForce(boat.sailAparentWind(0))
    aparentForce.angle += boat.angle + boat.sails[0].angle - Angle(1,90)
    aparentForce.angle = Angle.norm(aparentForce.angle)
    pas+= aparentForce.angle.calc() == 0; fail+= aparentForce.angle.calc() != 0
    pas+= aparentForce.speed() == 1.2982186666666669; fail+= aparentForce.speed() != 1.2982186666666669
    pas+= boat.sailDragForce().angle.calc() == 0; fail+= boat.sailDragForce().angle.calc() != 0
    pas+= boat.sailDragForce().speed() == 1.2982186666666669; fail+= boat.sailDragForce().speed() != 1.2982186666666669

    boat.angle = Angle(1,155)
    boat.sails[0].angle = Angle(1,10)
    wind.angle = Angle(1,0)
    aparentForce = boat.sails[0].dragForce(boat.sailAparentWind(0))
    aparentForce.angle += boat.angle + boat.sails[0].angle - Angle(1,90)
    aparentForce.angle = Angle.norm(aparentForce.angle)
    pas+= aparentForce.angle.calc() == 0; fail+= aparentForce.angle.calc() != 0
    pas+= aparentForce.speed() == 0.20036800000000002; fail+= aparentForce.speed() != 0.20036800000000002
    pas+= boat.sailDragForce().angle.calc() == 0; fail+= boat.sailDragForce().angle.calc() != 0
    pas+= boat.sailDragForce().speed() == 0.20036800000000002; fail+= boat.sailDragForce().speed() != 0.20036800000000002

    boat.angle = Angle(1,155+90)
    boat.sails[0].angle = Angle(1,10)
    wind.angle = Angle(1,90)
    aparentForce = boat.sails[0].dragForce(boat.sailAparentWind(0))
    aparentForce.angle += boat.angle + boat.sails[0].angle - Angle(1,90)
    aparentForce.angle = Angle.norm(aparentForce.angle)
    pas+= aparentForce.angle.calc() == 90; fail+= aparentForce.angle.calc() != 90
    pas+= aparentForce.speed() == 0.20036800000000002; fail+= aparentForce.speed() != 0.20036800000000002
    pas+= boat.sailDragForce().angle.calc() == 90; fail+= boat.sailDragForce().angle.calc() != 90
    pas+= boat.sailDragForce().speed() == 0.20036800000000002; fail+= boat.sailDragForce().speed() != 0.20036800000000002

    print("HULL+BOAT \33[35mDrag\033[0m Forces, passed: " + str(pas) + ", failed: " + str(fail)+ ", of: " +str(pas+fail) + color(fail))
    pas = 0;fail = 0
    boat.angle = Angle(1,75)
    boat.sails[0].angle = Angle(1,70)
    wind.angle = Angle(1,0)
    pas+= boat.sailLiftForce().angle.calc() == 90; fail+= boat.sailLiftForce().angle.calc() != 90
    pas+= boat.sailLiftForce().speed() == 8.605056; fail+= boat.sailLiftForce().speed() != 8.605056

    boat.angle = Angle(1,15)
    boat.sails[0].angle = Angle(1,75)
    wind.angle = Angle(1,0)
    pas+= boat.sailLiftForce().angle.calc() == 90; fail+= boat.sailLiftForce().angle.calc() != 90
    pas+= boat.sailLiftForce().speed() == -0.717248; fail+= boat.sailLiftForce().speed() != -0.717248
    pas+= boat.sailDragForce().angle.calc() == 0; fail+= boat.sailDragForce().angle.calc() != 0
    pas+= boat.sailDragForce().speed() == 8.606912; fail+= boat.sailDragForce().speed() != 8.606912

    boat.angle = Angle(1,15)
    boat.sails[0].angle = Angle(1,-15)
    wind.angle = Angle(1,90)
    pas+= boat.sailLiftForce().angle.calc() == 0; fail+= boat.sailLiftForce().angle.calc() != 0
    pas+= boat.sailLiftForce().speed() ==-0.717248; fail+= boat.sailLiftForce().speed() != -0.717248

    #NOTE: TECHNICALLY THIS IS WRONG but the angle is correct, I don't have data for such extreme AOA but situation won't happen 
    boat.angle = Angle(1,15)
    boat.sails[0].angle = Angle(1,0)
    wind.angle = Angle(1,90)
    pas+= boat.sailLiftForce().angle.calc() == 180; fail+= boat.sailLiftForce().angle.calc() != 180
    pas+= boat.sailLiftForce().speed() ==9.114135999999998; fail+= boat.sailLiftForce().speed() != 9.114135999999998
    
    print("HULL+BOAT \033[94mLift\033[0m Forces, passed: " + str(pas) + ", failed: " + str(fail)+ ", of: " +str(pas+fail) + color(fail))

    #print("wind: ",boat.wind,'\n vel: ',boat.velocity, '\n res:',boat.sailAparentWind())


if __name__ == "__main__":
    # color guide https://stackoverflow.com/questions/287871/how-do-i-print-colored-text-to-the-terminal
    print("\033[1m\033[95m"+"Variable test"+"\033[0m")
    VariableTest()
    print("\033[1m\033[95m"+"Foil test"+"\033[0m")
    FoilTest()
    print("\033[1m\033[95m"+"Boat test"+"\033[0m")
    BoatTest()