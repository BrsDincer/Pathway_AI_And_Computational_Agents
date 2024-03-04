"""
The environment state is given in terms of the time and the amount of paper in stock.
It also remembers the in-stock history and the price history.
The perception consists of the price and the amount of paper in stock.
The action of the agent is the number to buy.
"""

import random,os
import matplotlib.pyplot as plt
from agent_configuration import Agent,Environment,Simulate
from util_class import ClassInitial,NullInitial
from util_project import SelectFromDistribution

class PSEnvironment(Environment):
  priceDelta = [
    0, 0, 0, 21, 0, 20, 0, -64, 0, 0, 23, 0, 0, 0, -35,
    0, 76, 0, -41, 0, 0, 0, 21, 0, 5, 0, 5, 0, 0, 0, 5, 0, -15, 0, 5,
    0, 5, 0, -115, 0, 115, 0, 5, 0, -15, 0, 5, 0, 5, 0, 0, 0, 5, 0,
    -59, 0, 44, 0, 5, 0, 5, 0, 0, 0, 5, 0, -65, 50, 0, 5, 0, 5, 0, 0,
    0, 5, 0
  ]
  standardDeviation = 5
  def __init__(self)->ClassInitial:
    self.time = 0
    self.stock = 20
    self.stockHistory = [] # memory of the stock history
    self.priceHistory = [] # memory of the price history
  def InitialPerception(self):
    """
    initial perception
    """
    self.stockHistory.append(self.stock)
    self.price = round(234+self.standardDeviation*random.gauss(0,1))
    self.priceHistory.append(self.price)
    return {
      "price":self.price,
      "instock":self.stock
    }
  def Do(self,action)->dict:
    paperUsed = SelectFromDistribution(
      {
        6:0.1,
        5:0.1,
        4:0.1,
        3:0.3,
        2:0.2,
        1:0.2
      }
    )
    bought = action["buy"]
    self.stock = self.stock+bought-paperUsed
    self.stockHistory.append(self.stock)
    self.time += 1
    self.price = round(
      self.price
      +self.priceDelta[self.time%len(self.priceDelta)] # repeating pattern
      +self.standardDeviation*random.gauss(0,1) # randomness
    )
    self.priceHistory.append(self.price)
    return {
      "price":self.price,
      "instock":self.stock
    }

"""
The agent does not have access to the price model but can only observe the current price and the amount in stock.
It has to decide how much to buy.
The belief state of the agent is an estimate of the average price of the paper,and the total amount of money the agent has spent.

The agent decides how much paper to buy based on its belief state, which includes an estimate of the average price and its observations of stock levels and prices.
The agent prefers to buy more paper if the price is significantly lower than its estimated average price and if the stock is below a certain threshold.
"""
class PSAgent(Agent):
  def __init__(self):
    self.spent = 0
    perception = environment.InitialPerception()
    self.ave = self.lastPrice = perception["instock"]
    self.buyHistory = []
  def SelectAction(self, perception)->dict:
    self.lastPrice = perception["price"]
    self.ave = self.ave+(self.lastPrice-self.ave)*0.05
    self.instock = perception["instock"]
    if self.lastPrice < 0.9*self.ave and self.instock < 60:
      toBuy = 48
    elif self.instock < 12:
      toBuy = 12
    else:
      toBuy = 0
    self.spent += toBuy*self.lastPrice
    self.buyHistory.append(toBuy)
    return {"buy":toBuy}

#CHECK RESULTS
class PlotHistory(object):
  def __init__(self,agent:ClassInitial,environment:ClassInitial)->ClassInitial:
    self.agent = agent
    self.environment = environment
    plt.ion()
    plt.title("Environment-Agent Result")
    plt.xlabel("Time")
    plt.ylabel("Value")
  def PlotEnvironmentHistory(self)->None|NullInitial:
    """
    plot history of price and instock
    """
    number = len(environment.stockHistory)
    plt.plot(range(number),environment.priceHistory,label="Price")
    plt.plot(range(number),environment.stockHistory,label="In Stock")
    plt.legend()
    plt.savefig(os.path.join(os.getcwd(),"environment_history.png"))
    print("Environment Result Has Been Saved")
  def PlotAgentHistory(self)->None|NullInitial:
    """
    plot history of buying
    """
    number = len(agent.buyHistory)
    plt.bar(range(1,number+1),agent.buyHistory,label="Bought")
    plt.legend()
    plt.savefig(os.path.join(os.getcwd(),"agent_history.png"))
    print("Agent Result Has Been Saved")

# UNIT TEST
#environment = PSEnvironment()
#agent = PSAgent()
#simulation = Simulate(agent,environment)
#simulation.Go(100) # 100 steps
#plotEngine = PlotHistory(agent,environment)
#plotEngine.PlotEnvironmentHistory()
#plotEngine.PlotAgentHistory()





