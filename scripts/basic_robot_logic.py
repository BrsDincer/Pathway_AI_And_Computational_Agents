import math,time,os
import matplotlib.pyplot as plt

"""
simple robotic navigation without obstacle detection
"""

class SimpleRobot:
  def __init__(self,x:int=0,y:int=0,direction:int=30):
    self.x = x
    self.y = y
    self.direction = direction
  def MoveForward(self,distance:int|float):
    """
    Move the robot forward in its current direction.
    """
    radian = math.radians(self.direction)
    self.x += distance*math.cos(radian)
    self.y += distance*math.sin(radian)
  def Turn(self,angle:int|float):
    self.direction = (self.direction+angle)%360
  def GetPosition(self):
    return self.x,self.y,self.direction

#UNIT TEST
# robot = SimpleRobot()
# robot.MoveForward(10)
# robot.Turn(-90)
# robot.MoveForward(5)
# print(robot.GetPosition())
  

class VisualRobot:
  def __init__(self,x:int=0,y:int=0,direction:int=90):
    self.x = x
    self.y = y
    self.direction = direction
    self.figure,self.axs = plt.subplots()
    self.axs.set_aspect("equal","box")
    self.axs.grid(True)
    self.axs.plot(self.x,self.y,"go") # Initial position
  def Turn(self,angle:int|float):
    """
    Turn the robot by a certain angle (degrees)
    """
    self.direction = (self.direction+angle)%360
  def UpdatePlot(self):
    """
    Update the plot with the robot's current position
    """
    self.axs.plot(self.x,self.y,"ro")
    plt.draw()
    plt.pause(0.4)
  def MoveForward(self,distance:int|float):
    radian = math.radians(self.direction)
    self.x += distance*math.cos(radian)
    self.y += distance*math.sin(radian)
    self.UpdatePlot()
  def GetPosition(self):
    return self.x,self.y,self.direction
  
robot = VisualRobot()
movements = [(10,0),(10,-10),(10,90),(5,90)]
for distance,angle in movements:
  robot.MoveForward(distance)
  robot.Turn(angle)
  time.sleep(0.7)
plt.savefig(os.path.join(os.getcwd(),"basic_robot_simulation.png"))
plt.show()