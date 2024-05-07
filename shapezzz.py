import abc
import logging
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
        return False

    @abc.abstractmethod
    def is_point_on_shape_boundary(self, point: Point) -> bool:
        return False

    @abc.abstractmethod
    def generateShape(self):
        pass

    def dist_line_to_point(self, l1: Point, l2: Point, p1: Point) -> float:


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
        if self.points[0].x < point.x:
            lx = True
        if self.points[0].y < point.y:
            hy = True
        if self.points[3].x > point.x:
            hx = True
        if self.points[3].y > point.y:
            ly = True
        return lx and hx and ly and hy

    def is_point_on_shape_boundary(self, point: Point) -> bool:
        pass

    def generateShape(self):
        pass
