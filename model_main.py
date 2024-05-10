import math
import numpy as np
GRID_WIDTH = 10
GRID_HEIGHT = 10


from shapezzz import Point, Rectangle, Circle, Triangle


def creategridlist(maxgrid: Point) -> list[Point]:
    gridpoints: list[Point] = []
    for px in range(math.floor(maxgrid.x) + 1):
        for py in range(math.floor(maxgrid.y) + 1):
            gridpoints.append(Point(px, py))
    return gridpoints

def createshapegridlist(maxgrid: Point) -> list[Point]:
    gridpoints: list[Point] = []
    for px in range(math.floor(maxgrid.x) + 1):
        for py in range(math.floor(maxgrid.y) + 1):
            gridpoints.append(Point(px+.5, py+.5))
    return gridpoints


def generate_rectangles(maxgrid: Point) -> list[Rectangle]:
    # returns a list of all possible rectangles - each rectangle is a list of points within the rectangle
    output: list[Rectangle] = []
    gridlist = createshapegridlist(maxgrid)
    for p1i in range(len(gridlist)):
        p1 = gridlist[p1i]
        for p2i in range(p1i + 1, len(gridlist)):
            p2 = gridlist[p2i]

            new_rect = Rectangle(p1, p2)
            if new_rect.area() >= maxgrid.x and new_rect.area() <= maxgrid.x*(maxgrid.x - 1):
                output.append(new_rect)

    return output


def generate_circles(maxgrid: Point) -> list[Circle]:
    # returns a list of all possible circles - each circle is a list of points within the circle
    output: list[Circle] = []
    gridlist = createshapegridlist(maxgrid)
    for p1i in range(len(gridlist)):
        p1 = gridlist[p1i]

        min_radius = math.ceil(math.sqrt(maxgrid.x / math.pi))
        max_radius = math.floor(math.sqrt(maxgrid.x * (maxgrid.x + 1) / math.pi))
        for radius in range(min_radius, max_radius + 1):
        # for p2i in range(p1i + 1, len(gridlist)):
            # p2 = gridlist[p2i]
            # if p2.y <= p1.y:
                # continue
            # if Circle.dist_point_point(p1, p2) > min(p1.x, p1.y, maxgrid.x-p1.x, maxgrid.y-p1.y):
                # continue
            if radius > min(p1.x, p1.y, maxgrid.x-p1.x, maxgrid.y-p1.y):
                continue

            output.append(Circle(p1, radius))
    return output


def generate_triangles(maxgrid: Point) -> list[Triangle]:
    # returns a list of all possible triangles - each triangle is a list of points within the triangle
    output: list[Triangle] = []
    gridpoints: list[Point] = createshapegridlist(maxgrid)
    for p1i in range(len(gridpoints)):
        for p2i in range(p1i + 1, len(gridpoints)):
            for p3i in range(p2i + 1, len(gridpoints)):
                if not Triangle.test_colinear(gridpoints[p1i], gridpoints[p2i], gridpoints[p3i]):
                    new_tri = Triangle(gridpoints[p1i], gridpoints[p2i], gridpoints[p3i])
                    if new_tri.area() >= maxgrid.x and new_tri.area() <= maxgrid.x*(maxgrid.x - 1):
                        output.append(new_tri)
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
    probs = np.zeros((len(shapes), GRID_WIDTH, GRID_HEIGHT))
    for s in range(len(shapes)):
        for i in range(0, GRID_WIDTH):
            for j in range(0, GRID_HEIGHT):
                if shapes[s].is_point_in_shape(Point(i,j)):
                    probs[s][i][j] = 1 
    return probs

def generate_prior(shapes):
    # returns the prior probability for a list of shapes
    prior = np.zeros(len(shapes))
    for s in range(len(shapes)):
        prior[s] = 1 / len(shapes)
    return prior


def generate_predictions(shapes, alpha, num_interations):
    # get init distributions and then apply recursive process
    # returns a 2D grid of probabilities for each hypothesis
    probs = generate_initial_distribution(shapes)
    prior = generate_prior(shapes)
    new_probs = np.zeros((len(shapes), GRID_WIDTH, GRID_HEIGHT))
    for k in range(num_interations):
        for s in range(len(shapes)):
            for i in range(0, GRID_WIDTH):
                for j in range(0, GRID_HEIGHT):
                    new_probs[s][i][j] = math.pow((probs[s][i][j] * prior[s]), alpha)
        for s in range(len(shapes)):
            new_probs[s] /= np.sum(new_probs[s])
        probs = new_probs
    return probs

def main():
    rects = generate_rectangles(Point(GRID_WIDTH, GRID_HEIGHT))
    triangs = generate_triangles(Point(GRID_WIDTH, GRID_HEIGHT))
    circles = generate_circles(Point(GRID_WIDTH, GRID_HEIGHT))
    print(f"rects: {len(rects)}")
    print(f"triangs: {len(triangs)}")
    print(f"circs: {len(circles)}")
    probs = generate_predictions(rects, 1, 5)
    print(rects[113].points)
    print(probs[113])
    print(rects[113].is_point_in_shape(Point(1,1)))
    #gen all shapes
    #get probabilities
    #calculate how much is near/far from the corners/boundaries for each type of shape
    #data viz


if __name__ == "__main__":
    main()
