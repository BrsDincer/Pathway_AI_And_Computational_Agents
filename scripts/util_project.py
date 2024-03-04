import random,math
from util_class import ClassInitial

# The argmax method returns the index of an element that has the maximum value

def ArgMaxAll(generator:ClassInitial)->list:
  """
  returns a list of all of the elements with maximal value
  """
  maxValues = []
  maxValue = -math.inf
  for (element,value) in generator:
    if value > maxValue:
      maxValues,maxValue = [element],value
    elif value == maxValue:
      maxValues.append(element)
  return maxValues

def ArgMaxRandom(generator:ClassInitial)->int|float:
  """
  if there are multiple elements with the max value, one is returned at random
  """
  return random.choice(ArgMaxAll(generator))

def ArgMax(lst:list)->int|float:
  """
  returns maximum index in a list
  """
  return ArgMaxRandom(enumerate(lst))

def ArgMaxDictionary(dct:dict)->int|float:
  """
  returns the arg max of a dictionary dct
  """
  return ArgMaxRandom(dct.items())


# EXAMPLE
#exampleList = [1,4,5,12,78]
#exampleDictionary = {2:5,5:11,7:7}
#print(ArgMax(exampleDictionary))
#print(ArgMax(exampleList))

def FlipRandom(probability:float)->bool:
  """
  return true with probability prob
  """
  return random.random() < probability

# The probabilities should sum to 1 or more. If they sum to more than one, the excess is ignored.
def SelectFromDistribution(itemDistribution:dict)->int|float:
  randomReal = random.random()
  for (item,probability) in itemDistribution.items():
    if randomReal < probability:
      return item
    else:
      randomReal -= probability
  raise RuntimeError(f"[Not a probability distribution]::{itemDistribution}")




