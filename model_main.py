# Question would it be possible for us to enumerate our shapes? 
# This way we could do somethin similar to our HW2 code, where we worked with a list of 5050 hypotheses 
# Global array of shapes - each index has a list of points within the shape
# Not sure how we would clearly indicate with points are at the corners or boundaries

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
    pass

def generate_predictions(shapes, alpha, num_interations):
    # get init distributions and then apply recursive process
    # returns a 2D grid of probabilities for each hypothesis
    pass


def main():
    #gen all shapes
    #get probabilities
    #calculate how much is near/far from the corners/boundaries for each type of shape
    #data viz
    pass

if __name__ == "__main__":
    main()