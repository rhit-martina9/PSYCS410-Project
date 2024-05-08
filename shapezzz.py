import abc
import logging
import math
from dataclasses import dataclass


@dataclass()
class Point:
    x: float
    y: float


class Shape(abc.ABC):
    points: list[Point]

    def __init__(self):
        self.points = []
        self.generateShape()

    @abc.abstractmethod
    def is_point_in_shape(self, point: Point) -> bool:
        pass

    @abc.abstractmethod
    def is_point_on_shape_boundary(self, point: Point) -> bool:
        pass

    @abc.abstractmethod
    def is_point_on_corner(self, point: Point) -> bool:
        pass

    @abc.abstractmethod
    def generateShape(self):
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


class Rectangle(Shape):
    def __init__(self, p1: Point, p2: Point):
        p3 = Point(p1.x, p2.y)
        p4 = Point(p2.x, p1.y)
        if p1.y > p2.y:
            if p1.x < p2.x:
                self.points = [p1, p4, p2, p3]
            elif p1.x > p2.x:
                self.points = [p4, p1, p3, p2]
        elif p1.y < p2.y:
            if p1.x < p2.x:
                self.points = [p4, p2, p3, p1]
            elif p1.x > p2.x:
                self.points = [p2, p4, p1, p3]
        if self.points is None or len(self.points) == 0:
            logging.warning("can't make rectangle!")

    def is_point_in_shape(self, point: Point) -> bool:
        lx = False
        hx = False
        ly = False
        hy = False
        if self.points[0].x <= point.x:
            lx = True
        if self.points[0].y <= point.y:
            hy = True
        if self.points[3].x >= point.x:
            hx = True
        if self.points[3].y >= point.y:
            ly = True
        return lx and hx and ly and hy

    def is_point_on_shape_boundary(self, point: Point) -> bool:
        if not self.is_point_in_shape(point):
            return False
        d1, d2, d3, d4 = self.get_line_dists(point)
        if d1 < 1 or d2 < 1 or d3 < 1 or d4 < 1:
            return True
        return False

    def is_point_on_corner(self, point: Point) -> bool:
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

    def generateShape(self):
        pass


class Triangle(Shape):
    def triangletest(self, p1: Point, p2: Point, p3: Point):
        return (p1.x - p3.x)*(p2.y-p3.y)-(p2.x-p3.x)*(p1.y-p3.y)

    def is_point_in_shape(self, point: Point) -> bool:
        d1 = self.triangletest(point, self.points[0], self.points[1])
        d2 = self.triangletest(point, self.points[1], self.points[2])
        d3 = self.triangletest(point, self.points[2], self.points[0])

        hasneg = (d1<0) or (d2<0) or (d3<0)
        haspos = (d1>0) or (d2>0) or (d3>0)

        return not (hasneg and haspos)

    def is_point_on_shape_boundary(self, point: Point) -> bool:
        pass

    def is_point_on_corner(self, point: Point) -> bool:
        pass

    def generateShape(self):
        pass

    def __init__(self, p1: Point, p2: Point, p3: Point):
        self.points = [p1, p2, p3]
