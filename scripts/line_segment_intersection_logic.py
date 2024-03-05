"""
Objective:
Write a function that determines if two line segments intersect.
The concept is detecting the intersection between two line segments, a key operation for collision detection in the environment.
"""

def CheckIntersection(lineA:tuple,lineB:tuple)->bool:
  """
    Determine if two line segments intersect.
    Each line segment is defined by a tuple of two points (x1, y1) and (x2, y2), where each point is represented as a (x, y) pair.
  """
  (Ax1,Ay1),(Ax2,Ay2) = lineA
  (Bx1,By1),(Bx2,By2) = lineB
  #differences
  dAx = Ax2-Ax1
  dAy = Ay2-Ay1
  dBx = Bx2-Bx1
  dBy = By2-By1
  # Calculate determinant
  determinant = dBx*dAy-dBy*dAx
  if determinant == 0:
    # Lines are parallel
    return False
  # Calculate the relative positions of the intersection point on the segments
  s = (dAx*(By1-Ay1)-dAy*(Bx1-Ax1))/determinant
  t = (dBx*(Ay1-By1)+dBy*(Bx1-Ax1))/determinant
  return 0 <= s <= 1 and 0 <= t <= 1

#UNIT TEST
# lineA = ((0,0),(1,1))
# lineB = ((1,0),(0,1))
# isIntersection = CheckIntersection(lineA,lineB)
# print(isIntersection)