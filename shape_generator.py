import random
import math

rectangles = []
circles = []
triangles = []

size = 10

#rectangles
for i in range(3):
    points = []
    x1 = random.randint(0,size-1)
    y1 = random.randint(0,size-1)
    points.append((x1,y1))

    x2 = random.randint(0,size-1)
    y2 = random.randint(0,size-1)
    while x1 == x2 or y1 == y2 or abs(x1-x2)*abs(y1-y2) < size or abs(x1-x2)*abs(y1-y2) > size*(size-1):
        x2 = random.randint(0,size-1)
        y2 = random.randint(0,size-1)
    points.append((x2,y2))
    rectangles.append(points)

for rec in rectangles:
    print(rec)

for i in range(3):
    points = []
    x = random.randint(0,size-1)
    y = random.randint(0,size-1)
    # r = random.randint(2,4)
    r = i+2
    while x+r > size or x-r < 0 or y+r > size or y-r < 0:
        x = random.randint(0,size-1)
        y = random.randint(0,size-1)
        # r = random.randint(2,4)
    points.append((x,y,r))
    circles.append(points)
    
for circ in circles:
    print(circ[0])


def shoelace(pts):
    left, right = 0, 0
    for i in range(len(pts)):
        left += pts[i][0] * pts[(i+1) % len(pts)][1]
        right += pts[i][1] * pts[(i+1) % len(pts)][0]
    return abs(left-right)/2

# triangles
for i in range(3):
    points = []
    x1 = random.randint(0,size-1)
    y1 = random.randint(0,size-1)
    points.append((x1,y1))

    x2 = random.randint(0,size-1)
    y2 = random.randint(0,size-1)
    while x1 == x2 or y1 == y2:
        x2 = random.randint(0,size-1)
        y2 = random.randint(0,size-1)
    points.append((x2,y2))
    
    x3 = random.randint(0,size-1)
    y3 = random.randint(0,size-1)
    points.append((x3,y3))
    while x3 in [x1, x2] or y3 in [y1, y2] or shoelace(points) < size or shoelace(points) > size*(size-1):
        points.pop()
        x3 = random.randint(0,size-1)
        y3 = random.randint(0,size-1)
        points.append((x3,y3))
    print(shoelace(points))
    print(points)
    triangles.append(points)
