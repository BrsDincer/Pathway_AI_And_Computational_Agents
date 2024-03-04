"""
In this project, we simulate a scenario where a transportation company needs to manage its fuel inventory.
Fuel prices change over time due to market dynamics and other factors.
The agent's goal is to buy fuel at optimal prices to ensure the company's vehicles are always operational without overspending on fuel costs.
"""

import random,os
import matplotlib.pyplot as plt
from agent_configuration import Agent,Environment
from util_class import ClassInitial,NullInitial

class FuelEnvironment(Environment):
  priceDelta = [
        0, 5, -3, 10, -4, 8, -7, 2, 0, -5, 3, -8, 6, -1, 4,
        -2, 5, -3, 7, -6, 4, 0, -4, 6, -2, 8, -5, 3, -7, 1
  ]
  standardDeviation = 3
  def __init__(self)->ClassInitial:
    self.time = 0
    self.fuelStock = 1000 # in liters
    self.stockHistory = []
    self.priceHistory = []
    self.price = 100 # initial price per liter
  def InitialPerception(self):
    self.stockHistory.append(self.fuelStock)
    self.priceHistory.append(self.price)
    return {
      "price":self.price,
      "fuelStock":self.fuelStock
    }
  def Do(self,action):
    fuelUsed = random.randint(50,150) # Simulate fuel consumption
    bought = action["buy"]
    self.fuelStock = max(self.fuelStock+bought-fuelUsed,0)
    self.stockHistory.append(self.fuelStock)
    self.time += 1
    priceChange = self.priceDelta[self.time%len(self.priceDelta)]+self.standardDeviation*random.gauss(0,1)
    self.price = max(50,self.price+priceChange) # Prevent price from going below a minimum
    self.priceHistory.append(self.price)
    return {
      "price":self.price,
      "fuelStock":self.fuelStock
    }

class FuelAgent(Agent):
  def __init__(self)->ClassInitial:
    self.spent = 0
    self.ave = self.lastPrice = environment.InitialPerception()["price"] # Average Price
    self.fuelStock = environment.InitialPerception()["fuelStock"]
    self.buyHistory = []
  def SelectAction(self,perception):
    self.lastPrice = perception["price"]
    self.fuelStock = perception["fuelStock"]
    self.ave = self.ave+(self.lastPrice-self.ave)
    if self.lastPrice < 0.9*self.ave and self.fuelStock < 800:
      toBuy = 200
    elif self.fuelStock < 500:
      toBuy = 100
    else:
      toBuy = 0
    self.spent += toBuy*self.lastPrice
    self.buyHistory.append(self.spent)
    return {"buy":toBuy}
  
class FuelSimulation(object):
  def __init__(self,agent:ClassInitial,environment:ClassInitial)->ClassInitial:
    self.agent = agent
    self.environment = environment
  def Run(self,steps:int)->None|NullInitial:
    for idx in range(steps):
      currentPerception = self.environment.Do(self.agent.SelectAction(self.environment.InitialPerception()))
      print(f"Step: {idx} [::] Price: {currentPerception['price']} [::] Stock: {currentPerception['fuelStock']}")
  def VisualizeResults(self)->None:
    plt.figure(figsize=(14,8))
    plt.subplot(1,2,1)
    plt.plot(self.environment.stockHistory,label="Fuel Stock")
    plt.plot(self.environment.priceHistory,label="Price per Liter",linestyle="--")
    plt.title("Fuel Stock & Price")
    plt.xlabel("Time")
    plt.ylabel("Value")
    plt.legend()
    plt.subplot(1,2,2)
    plt.bar(range(len(self.agent.buyHistory)),self.agent.buyHistory,label="Fuel Purchased")
    plt.title("Fuel Purchase History")
    plt.xlabel("Time")
    plt.ylabel("Liters")
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(os.getcwd(),"fuel_simulation.png"))
    plt.show()

# UNIT TEST
#environment = FuelEnvironment()
#agent = FuelAgent()
#simulation = FuelSimulation(agent,environment)
#simulation.Run(100)
#simulation.VisualizeResults()

    