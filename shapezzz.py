import abc
import logging
import math
import numpy as np
from dataclasses import dataclass
import matplotlib.patches 


@dataclass()
class Point:
    x: float
    y: float


class Shape(abc.ABC):
    points: list[Point]

    @abc.abstractmethod
    def is_point_in_shape(self, point: Point) -> bool:
        pass

    def is_point_on_shape_boundary(self, point: Point) -> bool:
        if not self.is_point_in_shape(point):
            return False
        dist = self.get_line_dists(point)
        cornercount = 0
        for dis in dist:
            if dis < 1:
                cornercount = cornercount + 1
        if cornercount == 2:
            return True
        return False

    def is_point_on_corner(self, point: Point) -> bool:
        if not self.is_point_in_shape(point):
            return False
        dists = self.get_line_dists(point)
        indist = False
        for dist in dists:
            if dist < 1:
                indist = True
        return indist

    @abc.abstractmethod
    def generateShape(self):
        pass

    @abc.abstractmethod
    def drawShape(self):
        pass

    @staticmethod
    def dist_line_to_point(l1: Point, l2: Point, p1: Point) -> float:
        m1 = (l2.x - l1.x) * (p1.y - l1.y)
        m2 = (p1.x - l1.x) * (l2.y - l1.y)
        nom = abs(m1 - m2)

        sq1 = (l2.x - l1.x) ** 2
        sq2 = (l2.y - l1.y) ** 2
        dom = math.sqrt(sq1 + sq2)
        ret = nom / dom
        return ret

    def get_line_dists(self, point: Point) -> list[float]:
        prevpoint = None
        outdists = []
        for sp in self.points:
            if prevpoint is None:
                prevpoint = sp
                continue
            outdists.append(self.dist_line_to_point(prevpoint, sp, point))
            prevpoint = sp
        outdists.append(self.dist_line_to_point(prevpoint, self.points[0], point))
        return outdists

    @staticmethod
    def dist_point_point(p1: Point, p2: Point):
        mul1 = (p2.x-p1.x)**2
        mul2 = (p2.y-p1.y)**2
        ret = math.sqrt(mul1+mul2)
        return ret

    @staticmethod
    def find_slope(point1: Point, point2: Point) -> float|None:
        if point1.x - point2.x == 0:
            return None
        slope = (point1.y - point2.y) / (point1.x - point2.x)
        return slope

    @staticmethod
    def test_colinear(p1: Point, p2: Point, p3: Point) -> bool:
        if p1==p2 or p1==p3 or p2==p3:
            return True
        s1 = Shape.find_slope(p1, p2)
        s2 = Shape.find_slope(p2, p3)
        if s1 is None and s2 is None:
            return True
        elif s1 is None or s2 is None:
            return False
        elif abs(s1) == abs(s2):
            return True
        else:
            return False

    @staticmethod
    def find_midpoint(p1: Point, p2: Point) -> Point:
        retx = (p1.x - p2.x)/2 + p2.x
        rety = (p1.y - p2.y)/2 + p2.y
        return Point(retx,rety)


class Rectangle(Shape):
    defpoints: tuple[Point, Point]

    def __init__(self, p1: Point, p2: Point):
        self.defpoints = (p1, p2)
        max_x = max(p1.x, p2.x)
        min_x = min(p1.x, p2.x)
        max_y = max(p1.y, p2.y)
        min_y = min(p1.y, p2.y)
        p1 = Point(min_x, min_y)
        p2 = Point(min_x, max_y)
        p3 = Point(max_x, max_y)
        p4 = Point(max_x, min_y)
        self.points = [p1, p2, p3, p4]


    def __new__(cls, p1: Point, p2: Point):
        if p1 == p2:
            return None
        if p1.x == p2.x or p1.y == p2.y:
            return None
        self = object.__new__(cls)
        return self


    def is_point_in_shape(self, point: Point) -> bool:
        lx = False
        hx = False
        ly = False
        hy = False
        if self.points[0].x <= point.x:
            lx = True
        if self.points[0].y <= point.y:
            hy = True
        if self.points[2].x >= point.x:
            hx = True
        if self.points[2].y >= point.y:
            ly = True
        return lx and hx and ly and hy

    def generateShape(self):
        pass

    def area(self):
        return abs(self.defpoints[0].x - self.defpoints[1].x)*abs(self.defpoints[0].y - self.defpoints[1].y)
    
    def drawShape(self):
        width = self.points[2].x - self.points[0].x
        height = self.points[2].y - self.points[0].y
        return matplotlib.patches.Rectangle((self.points[0].x, self.points[0].y), width, height, 
                         fill=False, linewidth=3, color="r")


class Triangle(Shape):

    @staticmethod
    def triangletest(p1: Point, p2: Point, p3: Point):
        return (p1.x - p3.x) * (p2.y - p3.y) - (p2.x - p3.x) * (p1.y - p3.y)

    def is_point_in_shape(self, point: Point) -> bool:
        d1 = self.triangletest(point, self.points[0], self.points[1])
        d2 = self.triangletest(point, self.points[1], self.points[2])
        d3 = self.triangletest(point, self.points[2], self.points[0])

        hasneg = (d1 < 0) or (d2 < 0) or (d3 < 0)
        haspos = (d1 > 0) or (d2 > 0) or (d3 > 0)

        return not (hasneg and haspos)

    def generateShape(self):
        pass

    def __init__(self, p1: Point, p2: Point, p3: Point):
        self.points = [p1, p2, p3]

    def area(self):
        left,right = 0,0
        for i in range(3):
            left += self.points[i].x * self.points[(i+1)%3].y
            right += self.points[i].y * self.points[(i+1)%3].x
        return abs(left - right) / 2

    def __new__(cls, p1: Point, p2: Point, p3: Point):
        if Triangle.test_colinear(p1, p2, p3):
            return None
        self = object.__new__(cls)
        return self
    
    def drawShape(self):
        xy = np.zeros((3, 2))
        for i in range(3):
            xy[i][0] = self.points[i].x
            xy[i][1] = self.points[i].y
        return matplotlib.patches.Polygon(xy, closed=True, fill=False, linewidth=3, color="r")


class Circle(Shape):
    center: Point
    radius: int

    def is_point_in_shape(self, point: Point) -> bool:
        pdist = self.dist_point_point(point, self.center)
        if pdist <= self.radius:
            return True
        return False

    def is_point_on_corner(self, point: Point) -> bool:
        return False

    def is_point_on_shape_boundary(self, point: Point) -> bool:
        pdist = self.dist_point_point(point, self.center)
        rdist = self.radius - pdist
        if 0 <= rdist < 1:
            return True
        return False

    def generateShape(self):
        pass

    def area(self):
        return math.pi*self.radius**2

    def __init__(self, center: Point, radius: int):
        # self.points = [center, outpoint]
        self.center = center
        # self.defpoints = (center, outpoint)
        # self.radius = self.dist_point_point(center, outpoint)
        self.radius = radius

    def __new__(cls, center: Point, outpoint: Point):
        if center == outpoint:
            return None
        self = object.__new__(cls)
        return self
    
    def drawShape(self):
        return matplotlib.patches.Circle((self.center.x, self.center.y), self.radius,
                                         fill=False, linewidth=3, color="r")
