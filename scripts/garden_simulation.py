import matplotlib.pyplot as plt
import math,random,os

"""
# Project Overview
- Environment: A garden represented by a rectangular grid with obstacles (trees).
- Robot: An autonomous lawn mower with simple controls: move forward and turn.
- Objective: Cover the entire garden area without colliding with obstacles.
"""

class Garden:
  def __init__(self,width:int,height:int,obstacles=None)->None:
    if obstacles is None:
      obstacles = []
    self.width = width
    self.height = height
    self.obstacles = obstacles

class LawnMower:
  """
  Simulates the autonomous lawn mower. It can move forward and turn.
  It avoids moving outside the garden bounds or into obstacles.
  The lawn mower's path is visualized, with obstacles marked distinctly.
  """
  def __init__(self,garden,x:int=0,y:int=0,direction:int=90):
    self.garden = garden
    self.x = x
    self.y = y
    self.direction = direction
    self.figure,self.axs = plt.subplots()
    self.axs.set_xlim(0,garden.width)
    self.axs.set_ylim(0,garden.height)
    self.axs.set_aspect("equal","box")
    self.PlotObstacles()
  def PlotObstacles(self):
    for obst in self.garden.obstacles:
      self.axs.plot(obst[0],obst[1],"bs",markersize=10) # Plot obstacles as blue squares
  def MoveForward(self):
    radian = math.radians(self.direction)
    nextX = self.x+math.cos(radian)
    nextY = self.y+math.sin(radian)
    if 0 <= nextX <= self.garden.width and 0 <= nextY <= self.garden.height and (nextX,nextY) not in self.garden.obstacles:
      self.x = nextX
      self.y = nextY
      self.axs.plot(self.x,self.y,"go") # Mowed grass as green dots
      plt.draw()
      plt.pause(0.2)
  def Turn(self,angle):
    self.direction = (self.direction+angle)%360
  def StartMoving(self,steps=100):
    for idx in range(steps):
      self.MoveForward()
      if random.random() < 0.3: # Randomly decide to turn to simulate navigation
        self.Turn(random.choice([-90,90]))

#UNIT TEST
# width,height = 20,20
# obstacles = [(5,5),(5,6),(5,7),(10,10),(10,11)]
# garden = Garden(width,height,obstacles)
# lawnMower = LawnMower(garden,x=0,y=0,direction=90)
# lawnMower.StartMoving(100)
# plt.savefig(os.path.join(os.getcwd(),"garden_simulation.png"))
# plt.show()
