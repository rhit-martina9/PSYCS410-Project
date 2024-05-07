import numpy as np
GRID_WIDTH = 11
GRID_HEIGHT = 0


def generate_rectangles():
    # returns a list of all possible rectangles - each rectangle is a list of points within the rectangle
    pass

def generate_circles():
    # returns a list of all possible circles - each circle is a list of points within the circle
    pass

def generate_triangles():
    # returns a list of all possible triangles - each triangle is a list of points within the triangle
    pass

def count_num_points_in_shape(shape):
    # returns number of lattice points in the shape. should be pretty simple if each shape is represented as a list of points
    pass

def is_point_in_shape(shape, point):
    # returns if a point is within a given shape. should be pretty simple if each shape is represented as a list of points
    pass

def generate_initial_distribution(shapes):
    # returns a 2D grid of probabilities for each hypothesis
    # this is based on just Bayes' rule and the size principle
    probs = np.zeros(len(shapes), GRID_WIDTH, GRID_HEIGHT)
    for s in range(len(shapes)):
        for i in range(0, GRID_WIDTH):
            for j in range(0, GRID_HEIGHT):
                pass
                # if shapes[s].isPointInShape((i,j)):
                    # probs[s][i][j] = 1 / shapes[s].numPointsInShape()
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
    probs = generate_initial_distribution()
    prior = generate_prior(shapes)
    new_probs = np.zeros(len(shapes), GRID_WIDTH, GRID_HEIGHT)
    for k in range(num_interations):
        for s in range(len(shapes)):
            for i in range(0, GRID_WIDTH):
                for j in range(0, GRID_HEIGHT):
                    new_probs[s][i][j] = (probs[s][i][j] * prior[s]) ^ alpha
        for s in range(len(shapes)):
            new_probs[s] /= np.sum(new_probs[s])
        probs = new_probs
    return probs

def main():
    #gen all shapes
    #get probabilities
    #calculate how much is near/far from the corners/boundaries for each type of shape
    #data viz
    pass

if __name__ == "__main__":
    main()