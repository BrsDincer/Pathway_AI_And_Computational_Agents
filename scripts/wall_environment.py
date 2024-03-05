import math,os
from util_class import *
from util_display import Displayable
from agent_configuration import Environment
import matplotlib.pyplot as plt

"""
It determines if two line segments intersect based on their geometric properties.
This is done by comparing the slopes and intercepts of the lines to see if there's a point where they cross within the segments' bounds.
If such a point exists, it means a collision is detected.
"""
def LineSegmentInterception(lineA:tuple,lineB:tuple)->bool:
  """
  returns true if the line segments, line-A and line-B intersect
  a line segment is represented as a pair of points
  a point is represented as a (x,y) pair
  """
  ((Ax0,Ay0),(Ax1,Ay1)) = lineA
  ((Bx0,By0),(Bx1,By1)) = lineB
  dA,dB = Ax1-Ax0,Bx1-Bx0
  eA,eB = Ay1-Ay0,By1-By0
  angleSeg = dB*eA-eB*dA
  if angleSeg == 0:
    # line segments are parallel
    return False
  cB = (dA*(By0-Ay0)-eA*(Bx0-Ax0))/angleSeg # position along line B
  if cB < 0 or cB > 1:
    return False
  cA = (dB*(By0-Ay0)-eB*(Bx0-Ax0))/angleSeg # position along line A
  return 0 <= cA <= 1

#UNIT TEST
#print(LineSegmentInterception(((0,0),(1,1)),((1,0),(0,1))))

"""
# Wall Environment
- Initializes an environment with predefined walls.
- Walls are represented as line segments defined by tuples of points (each point being an (x, y) pair).
"""
class WallEnvironment(Environment):
  def __init__(self,walls:dict={})->ClassInitial:
    self.walls = walls

"""
# Body Environment
- Represents a robotic agent within the wall environment.
- Initializes the agent with a starting position and orientation.
- Implements a "whisker" sensor simulation to detect collisions with walls.
- The Whisker method simulates this sensor by extending a line segment (the whisker) from the agent in the direction it's facing minus the whisker angle. It then checks for intersections with any wall using the LineSegmentInterception function.
- The Do method updates the agent's position based on steering actions ('left', 'right', 'straight') and checks for collisions.
"""
class BodyEnvironment(Environment):
  def __init__(self,environment:ClassInitial,initPosition:tuple=(0,0,90))->ClassInitial:
    self.environment = environment
    self.xPos,self.yPos,self.direction = initPosition
    self.turningAngle = 18 # degrees that a left makes
    self.whiskerLength = 6 # length of the whisker
    self.whiskerAngle = 30 # angle of whisker relative to robot
    self.crashed = False
    self.plotting = True # whether the trace is being plotted
    self.sleepTime = 0.05 # time between actions (for real-time plotting)
    self.history = [(self.xPos,self.yPos)] # history of (x,y) positions
    self.wallHistory = []
  def Whisker(self)->bool:
    """
    returns true whenever the whisker sensor intersects with a wall
    Red dots correspond to the whisker sensor being on; the green dot to the whisker sensor being off
    """
    # angle in radians in world coordinates
    angleWorld = (self.direction-self.whiskerAngle)*math.pi/180 
    Wx = self.xPos + self.whiskerLength*math.cos(angleWorld)
    Wy = self.yPos + self.whiskerLength*math.sin(angleWorld)
    lineWhisker = ((self.xPos,self.yPos),(Wx,Wy))
    hit = any(LineSegmentInterception(lineWhisker,wall) for wall in self.environment.walls)
    if hit:
      self.wallHistory.append((self.xPos,self.yPos))
      if self.plotting:
        plt.plot([self.xPos],[self.yPos],"ro")
        plt.draw()
  def Perception(self)->dict:
    return {
      "xPos":self.xPos,
      "yPos":self.yPos,
      "direction":self.direction,
      "whisker":self.Whisker(),
      "crashed":self.crashed
    }
  InitialPerception = Perception # use percept function for initial percept too
  def Do(self,action)->ClassInitial:
    """
    action is {'steer':direction}
    """
    if self.crashed:
      return self.Perception()
    # direction is 'left', 'right' or 'straight'
    directionSteer = action["steer"]
    compassDerivation = {"left":1,"straight":0,"right":-1}[directionSteer]*self.turningAngle
    self.direction = (self.direction+compassDerivation+360)%360 # making in range [0,360)
    xPosNew = self.xPos+math.cos(self.direction*math.pi/180)
    yPosNew = self.yPos+math.sin(self.direction*math.pi/180)
    path = ((self.xPos,self.yPos),(xPosNew,yPosNew))
    if any(LineSegmentInterception(path,wall) for wall in self.environment.walls):
      self.crashed = True
      if self.plotting:
        plt.plot([self.xPos],[self.yPos],"r*",markersize=15.0)
        plt.draw()
    self.xPos,self.yPos = xPosNew,yPosNew
    self.history.append((self.xPos,self.yPos))
    if self.plotting and not self.crashed:
      plt.plot([self.xPos],[self.yPos],"go")
      plt.draw()
      plt.pause(self.sleepTime)
    return self.Perception()
  

"""
# Middle Layer
- The middle layer acts like both a controller (for the environment layer) and an environment for the upper layer.
- It has to tell the environment how to steer.
- Acts as a controller for the BodyEnvironment and as an environment for navigation tasks.
- It calculates steering directions to navigate towards a target position without colliding with walls.
- Utilizes the Whisker sensor information to avoid obstacles.
- The Steer method decides on the steering action based on the target location and whisker detection.
"""
class MiddleEnvironment(Environment):
  def __init__(self,environment)->ClassInitial:
    self.environment = environment
    self.perception = environment.InitialPerception()
    self.straightAngle = 11 # angle that is close enough to straight ahead
    self.closeThreshold = 2 # distance that is close enough to arrived
    self.closeThresholdSquared = self.closeThreshold**2 # just compute it once
  def InitialPerception(self)->dict:
    return {}
  def IsCloseEnough(self,targetPosition)->bool:
    Gx,Gy = targetPosition
    Rx,Ry = self.perception["xPos"],self.perception["yPos"]
    return (Gx-Rx)**2+(Gy-Ry)**2 <= self.closeThresholdSquared
  def HeadTowards(self,targetPosition):
    """
    given a target position, return the action that heads towards that position
    """
    Gx,Gy = targetPosition
    Rx,Ry = self.perception["xPos"],self.perception["yPos"]
    goal = math.acos(
      (Gx-Rx)/math.sqrt((Gx-Rx)*(Gx-Rx)+(Gy-Ry)*(Gy-Ry))
    )*180/math.pi
    if Ry>Gy:
      goal = -goal
    goalFrom = (goal-self.perception["direction"]+540)%360-180
    assert -180 < goalFrom <= 180
    if goalFrom > self.straightAngle:
      return "left"
    elif goalFrom < -self.straightAngle:
      return "right"
    else:
      return "straight"
  def Steer(self,targetPosition)->str:
    if self.perception["whisker"]:
      self.display(3,"whisker on",self.perception)
      return "left"
    else:
      return self.HeadTowards(targetPosition)
  def Do(self,action):
    """
    action is {'go_to':target_pos,'timeout':timeout}
    targetPosition is (x,y) pair
    timeout is the number of steps to try

        returns {'arrived':True} when arrived is true
                {'arrived':False} if it reached the timeout
    """
    if "timeout" in action:
      remaining = action["timeout"]
    else:
      remaining = -1 # will never reach 0
    targetPosition = action["go_to"]
    arrived = self.IsCloseEnough(targetPosition)
    while not arrived and remaining != 0:
      self.perception = self.environment.Do({"steer":self.Steer(targetPosition)})
      remaining -= 1
      arrived = self.IsCloseEnough(targetPosition)
    return {"arrived":arrived}

"""
# Top Layer
- The top layer treats the middle layer as its environment. Note that the top layer is an environment for us to tell it what to visit.
- Defines higher-level navigation tasks, such as visiting specific locations within the environment.
- It interacts with the MiddleEnvironment to execute these tasks by steering the agent towards the designated positions.
"""
class TopEnvironment(Environment):
  def __init__(self,middle:ClassInitial,timeout:int=200,locations:dict={
    "mail":(-5,10),
    "o103":(50,100),
    "o109":(100,10),
    "storage":(101,51)
  }):
    self.middle = middle
    self.timeout = timeout
    self.locations = locations
  def Do(self,plan):
    toDo = plan["visit"]
    for loc in toDo:
      position = self.locations[loc]
      arrived = self.middle.Do({"go_to":position,"timeout":self.timeout})
      self.display(1,"Arrived at",loc,arrived)

class PlotSimulation(Displayable):
  def __init__(self,body:ClassInitial,top:ClassInitial)->ClassInitial:
    self.body = body
    self.top = top
    plt.ion()
    plt.axes().set_aspect("equal")
    self.ReDraw()
    plt.savefig(os.path.join(os.getcwd(),"wall_simulation.png"))
  def ReDraw(self):
    plt.clf()
    for wall in body.environment.walls:
      ((x0,y0),(x1,y1)) = wall
      plt.plot([x0,x1],[y0,y1],"-k",linewidth=3)
    for loc in top.locations:
      (x,y) = top.locations[loc]
      plt.plot([x],[y],"k<")
      plt.text(x+1.0,y+0.5,loc)
    plt.plot([body.xPos],[body.yPos],"go")
    plt.gca().figure.canvas.draw()
    if self.body.history or self.body.wallHistory:
      self.PlotRun()
  def PlotRun(self):
    if self.body.history:
      xS,yS = zip(*self.body.history)
      plt.plot(xS,yS,"go")
    if self.body.wallHistory:
      wxS,wyS = zip(*self.body.wallHistory)
      plt.plot(wxS,wyS,"ro")

#UNIT TEST -I
# environment = WallEnvironment(
#   {
#     ((20,0),(30,20)),
#     ((70,-5),(70,25))
#   }
# )
# body = BodyEnvironment(environment)
# middle = MiddleEnvironment(body)
# top = TopEnvironment(middle)
# pEngine = PlotSimulation(body,top)
# top.Do(
#   {
#     "visit":["o109","storage","o109","o103"]
#   }
# )
# middle.Do(
#   {
#     "go_to":(30,-10),
#     "timeout":200
#   }
# )

#UNIT TEST -II
# environment = WallEnvironment(
#   {
#     ((10,-11),(10,0)),
#     ((10,50),(10,31)),
#     ((30,-10),(30,0)),
#     ((30,10),(30,20))
#   }
# )
# body = BodyEnvironment(environment,initPosition=(0,0,90))
# middle = MiddleEnvironment(body)
# top = TopEnvironment(middle)
# pl=PlotSimulation(body,top)
# top.Do({'visit':["o109","storage","o109","o103","goal"]})


class PlotFollow(PlotSimulation):
  def __init__(self,body,top,epsilon=2.5):
    PlotSimulation.__init__(self,body,top)
    self.epsilon = epsilon
    self.canvas = plt.gca().figure.canvas
    self.canvas.mpl_connect("button_press_event",self.OnPress)
    self.canvas.mpl_connect("button_release_event",self.OnRelease)
    self.canvas.mpl_connect("motion_notify_event",self.OnMove)
    self.pressloc = None
    self.pressevent = None
    for loc in self.top.locations:
      self.display(2,f"Location: {loc} at {self.top.locations[loc]}")
  def OnPress(self,event):
    self.display(2,"v",end="")
    self.display(2,f"Press at ({event.xdata},{event.ydata})")
    for loc in self.top.locations:
      Lx,Ly = self.top.locations[loc]
      if abs(event.xdata-Lx) <= self.epsilon and abs(event.ydata-Ly) <= self.epsilon:
        self.pressloc = loc
        self.pressevent = event
        self.display(2,"moving",loc)
  def OnRelease(self,event):
    self.display(2,"^",end="")
    if self.pressloc is not None: #and event.inaxes == self.pressevent.inaxes:
      self.top.locations[self.pressloc] = (event.xdata,event.ydata)
      self.display(1,f"Place: {self.pressloc} at ({event.xdata,event.ydata})")
    self.pressloc = None
    self.pressevent = None
  def OnMove(self,event):
    if self.pressloc is not None: # and event.inaxes == self.pressevent.inaxes:
      self.display(2,"-",end="")
      self.top.locations[self.pressloc] = (event.xdata,event.ydata)
      self.ReDraw()
    else:
      self.display(2,".",end="")

#UNIT TEST
# environment = WallEnvironment(
#   {
#     ((10,-11),(10,0)),
#     ((10,50),(10,31)),
#     ((30,-10),(30,0)),
#     ((30,10),(30,20))
#   }
# )
# body = BodyEnvironment(environment,initPosition=(0,0,90))
# middle = MiddleEnvironment(body)
# top = TopEnvironment(middle)
# p1 = PlotFollow(body,top)
# top.Do(
#   {
#     "visit":['o109','storage','o109','o103']
#   }
# )

