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

#triangles
for i in range(3):
    points = []
    x1 = random.randint(0,size-1)
    y1 = random.randint(0,size-1)
    points.append((x1,y1))

    x2 = random.randint(0,size-1)
    y2 = random.randint(0,size-1)
    while x1 == x2 or y1 == y2 or abs(x1-x2)*abs(y1-y2) < size*2 or abs(x1-x2)*abs(y1-y2) > size*(size-1)*2:
        x2 = random.randint(0,size-1)
        y2 = random.randint(0,size-1)
    points.append((x2,y2))

    if random.random() > 0.5:
        points.append((x1,y2))
    else:
        points.append((x2,y1))
    triangles.append(points)

for tri in triangles:
    print(tri)