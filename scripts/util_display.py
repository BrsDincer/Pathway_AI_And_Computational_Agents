from util_class import ClassInitial

class Displayable(object):
  maxDisplay:ClassInitial|int = 1
  def display(self,level:int,*args,**nargs)->None:
    """
    if level is less than or equal to the current maximum display level [maxDisplay]
    """
    if level <= self.maxDisplay:
      print(*args,**nargs)
