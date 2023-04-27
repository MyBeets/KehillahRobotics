# I'll start out with a simple test that aims to maintain a certain direction
import math
class Controler():
    def __init__(self,Boat, waypoint):
        self.boat = Boat
        self.waypoint = waypoint
    def update(self,dt):
        dx = self.waypoint[0]-self.boat.position.xcomp()
        dy = self.waypoint[1]-self.boat.position.ycomp()
        target_angle = math.atan2(dy,dx)*180/math.pi
        current_angle = self.linearVelocity.angle.calc()
        
