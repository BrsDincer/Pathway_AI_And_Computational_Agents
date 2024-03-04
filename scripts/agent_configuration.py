from util_display import Displayable
from util_class import ClassInitial,ErrorInitial,NullInitial

class Agent(Displayable):
  def SelectAction(self,perception)->ErrorInitial:
    raise NotImplementedError("Go") # abstract method
  def InitialAction(self,perception)->ErrorInitial:
    return self.SelectAction(perception) # abstract method
  
class Environment(Displayable):
  def InitialPerception(self)->ErrorInitial:
    """
    returns the initial perception
    """
    raise NotImplementedError("InitialPerception") # abstract method
  def Do(self,action)->ErrorInitial:
    """
    returns the next perception
    """
    raise NotImplementedError("Environment.Do") # abstract method

# The simulator lets the agent and the environment take turns in updating their states and returning the action and the percept.
class Simulate(Displayable):
  """
  simulate the interaction between the agent and the environment
  returns a pair of the agent state and the environment state
  """
  def __init__(self,agent:ClassInitial,environment:ClassInitial)->ClassInitial:
    self.agent = agent
    self.environment = environment
    self.perception = self.environment.InitialPerception()
    self.perceptionHistory = [self.perception]
    self.actionHistory = []
  def Go(self,n:int)->None|NullInitial:
    for idx in range(n):
      action = self.agent.SelectAction(self.perception)
      self.display(2,f"Count: {idx} [::] Action: {action}")
      self.perception = self.environment.Do(action)
      self.display(2,f"\t Perception: {self.perception}")
  