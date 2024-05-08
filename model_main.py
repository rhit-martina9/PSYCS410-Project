# Question would it be possible for us to enumerate our shapes? 
# This way we could do somethin similar to our HW2 code, where we worked with a list of 5050 hypotheses 
# Global array of shapes - each index has a list of points within the shape
# Not sure how we would clearly indicate with points are at the corners or boundaries
import math

from shapezzz import Point, Rectangle, Circle, Triangle


def creategridlist(maxgrid: Point) -> list[Point]:
    gridpoints: list[Point] = []
    for px in range(math.floor(maxgrid.x) + 1):
        for py in range(math.floor(maxgrid.y) + 1):
            gridpoints.append(Point(px, py))
    return gridpoints


def generate_rectangles(maxgrid: Point) -> list[Rectangle]:
    # returns a list of all possible rectangles - each rectangle is a list of points within the rectangle
    output: list[Rectangle] = []
    gridlist = creategridlist(maxgrid)
    for p1i in range(len(gridlist)):
        p1 = gridlist[p1i]
        for p2i in range(p1i + 1, len(gridlist)):
            p2 = gridlist[p2i]
            output.append(Rectangle(p1, p2))

    return output


def generate_circles(maxgrid: Point) -> list[Circle]:
    # returns a list of all possible circles - each circle is a list of points within the circle
    output: list[Circle] = []
    gridlist = creategridlist(maxgrid)
    for p1i in range(len(gridlist)):
        p1 = gridlist[p1i]
        for p2i in range(p1i + 1, len(gridlist)):
            p2 = gridlist[p2i]
            if p2.y <= p1.y:
                continue
            if Circle.dist_point_point(p1, p2) > min(p1.x, p1.y, maxgrid.x-p1.x, maxgrid.y-p1.y):
                continue
            output.append(Circle(p1, p2))
    return output


def generate_triangles(maxgrid: Point) -> list[Triangle]:
    # returns a list of all possible triangles - each triangle is a list of points within the triangle
    output: list[Triangle] = []
    gridpoints: list[Point] = creategridlist(maxgrid)
    for p1i in range(len(gridpoints)):
        for p2i in range(p1i + 1, len(gridpoints)):
            for p3i in range(p2i + 1, len(gridpoints)):
                if not Triangle.test_colinear(gridpoints[p1i], gridpoints[p2i], gridpoints[p3i]):
                    output.append(Triangle(gridpoints[p1i], gridpoints[p2i], gridpoints[p3i]))
    return output


def count_num_points_in_shape(shape):
    # returns number of lattice points in the shape. should be pretty simple if each shape is represented as a list of points
    pass


def is_point_in_shape(shape, point):
    # returns if a point is within a given shape. should be pretty simple if each shape is represented as a list of points
    pass


def generate_initial_distribution(shapes):
    # returns a 2D grid of probabilities for each hypothesis
    # this is based on just Bayes' rule and the size principle
    pass


def generate_predictions(shapes, alpha, num_interations):
    # get init distributions and then apply recursive process
    # returns a 2D grid of probabilities for each hypothesis
    pass


def main():
    rects = generate_rectangles(Point(6, 6))
    triangs = generate_triangles(Point(6, 6))
    circles = generate_circles(Point(6, 6))
    print(f"rects: {len(rects)}")
    print(f"triangs: {len(triangs)}")
    print(f"circs: {len(circles)}")
    #gen all shapes
    #get probabilities
    #calculate how much is near/far from the corners/boundaries for each type of shape
    #data viz
    pass


if __name__ == "__main__":
    main()
