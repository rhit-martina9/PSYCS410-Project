import math
import numpy as np
from shapezzz import Point, Rectangle, Circle, Triangle
import analysis

GRID_WIDTH = 10
GRID_HEIGHT = 10

def creategridlist(maxgrid: Point) -> list[Point]:
    gridpoints: list[Point] = []
    for px in range(math.floor(maxgrid.x) + 1):
        for py in range(math.floor(maxgrid.y) + 1):
            gridpoints.append(Point(px, py))
    return gridpoints

def createshapegridlist(maxgrid: Point) -> list[Point]:
    gridpoints: list[Point] = []
    for px in range(math.floor(maxgrid.x)):
        for py in range(math.floor(maxgrid.y)):
            gridpoints.append(Point(px+.5, py+.5))
    return gridpoints


def generate_rectangles(maxgrid: Point, area_range: list[float]) -> list[Rectangle]:
    # returns a list of all possible rectangles - each rectangle is a list of points within the rectangle
    output: list[Rectangle] = []
    gridlist = createshapegridlist(maxgrid)
    for p1i, p1 in enumerate(gridlist):
        for p2i in range(p1i + 1, len(gridlist)):
            p2 = gridlist[p2i]

            new_rect = Rectangle(p1, p2)
            if new_rect is None:
                continue
            if area_range[0] < new_rect.area() < area_range[1]:
                if sum(1 if new_rect.points == rect.points else 0 for rect in output) == 0:
                    output.append(new_rect)
    return output


def generate_circles(maxgrid: Point, area_range: list[float]) -> list[Circle]:
    # returns a list of all possible circles - each circle is a list of points within the circle
    output: list[Circle] = []
    gridlist = createshapegridlist(maxgrid)
    min_radius = math.ceil(math.sqrt(area_range[0] / math.pi))
    max_radius = math.floor(math.sqrt(area_range[1] / math.pi))
    for p1 in gridlist:
        for radius in range(min_radius, max_radius + 1):
            if radius > min(p1.x, p1.y, maxgrid.x-p1.x, maxgrid.y-p1.y):
                continue

            output.append(Circle(p1, radius))
    return output


def generate_triangles(maxgrid: Point, area_range: list[float]) -> list[Triangle]:
    # returns a list of all possible triangles - each triangle is a list of points within the triangle
    output: list[Triangle] = []
    gridpoints: list[Point] = createshapegridlist(maxgrid)
    for p1i in range(len(gridpoints)):
        for p2i in range(p1i + 1, len(gridpoints)):
            for p3i in range(p2i + 1, len(gridpoints)):
                if not Triangle.test_colinear(gridpoints[p1i], gridpoints[p2i], gridpoints[p3i]):
                    new_tri = Triangle(gridpoints[p1i], gridpoints[p2i], gridpoints[p3i])
                    if area_range[0] < new_tri.area() < area_range[1]:
                        output.append(new_tri)
    return output


def count_num_points_in_shape(shape):
    # returns number of lattice points in the shape. should be pretty simple if each shape is represented as a list of points
    count = 0
    for x in range(0, GRID_WIDTH):
        for y in range(0, GRID_HEIGHT):
            if shape.is_point_in_shape(Point(x,y)):
                count += 1
    return count

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

def generate_data():
    #returns an array of all possible combination of 2 points
    num_squares = GRID_WIDTH * GRID_HEIGHT
    num_data = int(num_squares*(num_squares-1)/2)
    data = np.zeros((num_data, 2), Point)
    cur_index = 0
    for x1 in range(GRID_WIDTH):
        for y1 in range(GRID_HEIGHT):
            for j in range(1, num_squares):
                x2 = int(((j / GRID_WIDTH) + x1) % GRID_WIDTH)
                y2 = int(((j % GRID_WIDTH) + y1) % GRID_HEIGHT)
                if x1*GRID_WIDTH+y1 < x2*GRID_WIDTH+y2:
                    data[cur_index] = [Point(x1, y1), Point(x2, y2)]
                    cur_index += 1
    return data

def generate_init_likelihood(shapes, data):
    # uniform for all combos of points that are both within the shape
    # 0 otherwise
    likelihood = np.zeros(shape=(len(shapes), len(data)))
    for s in range(len(shapes)):
        for d in range((len(data))):
            if shapes[s].is_point_in_shape(data[d][0]) \
                and shapes[s].is_point_in_shape(data[d][1]):
                likelihood[s][d] = 1
        total = np.sum(likelihood[s])
        if total != 0:
            for d in range((len(data))):
                likelihood[s][d] /= total
    return likelihood

def generate_prior(shapes):
    # returns the prior probability for a list of shapes
    prior = np.zeros(len(shapes))
    for s in range(len(shapes)):
        prior[s] = 1/ len(shapes)
    return prior

def generate_posterior(shapes, data, likelihood, prior):
    posterior = np.zeros(shape=(len(shapes), len(data)))
    for s in range(len(shapes)):
        for d in range((len(data))):
            posterior[s][d] = likelihood[s][d] * prior[s]
    for d in range((len(data))):
        total = 0
        for s in range(len(shapes)):
            total += posterior[s][d]
        if total != 0:
            for s in range(len(shapes)):
                posterior[s][d] /= total
    return posterior

def log(posterior, iteration, shape_type, data_type):
    f = open(shape_type + "_" + data_type + "_" + str(iteration) + ".txt", "a")
    for s in range(len(posterior)):
        f.write(str(s) + ":")
        for data in posterior[s]:
            f.write(str(data))
            f.write(",")
        f.write("\n")
    f.close()


def generate_likelihood(shapes, data, posterior):
    likelihood = np.zeros(shape=(len(shapes), len(data)))
    for s in range(len(shapes)):
        for d in range((len(data))):
            likelihood[s][d] = posterior[s][d]
        total = np.sum(likelihood[s])
        if total != 0:
            for d in range((len(data))):
                likelihood[s][d] /= total
    return likelihood

def generate_predictions(shapes, data, num_interations, t):
    posterior = np.zeros((len(shapes), len(data)))
    likelihood = generate_init_likelihood(shapes, data)
    prior = generate_prior(shapes)
    for i in range(num_interations - 1):
        posterior = generate_posterior(shapes, data, likelihood, prior)
        # log(posterior, i, t, "posterior")
        likelihood = generate_likelihood(shapes, data, posterior)
        # log(likelihood, i, t, "likelihood")
    posterior = generate_posterior(shapes, data, likelihood, prior)
    
    predictions = np.zeros((len(shapes), GRID_WIDTH, GRID_HEIGHT))
    for s in range(len(shapes)):
        for d in range(len(data)):
            x1 = data[d][0].x
            x2 = data[d][1].x
            y1 = data[d][0].y
            y2 = data[d][1].y
            predictions[s][x1][y1] += posterior[s][d]
            predictions[s][x2][y2] += posterior[s][d]
        predictions[s] /= np.sum(predictions[s])
    return predictions

def gen_triangle_preds(area_range, pairs_of_points):
    triangs = generate_triangles(Point(GRID_WIDTH, GRID_HEIGHT), area_range)
    print(f"triangs: {len(triangs)}")
    triangs_pred = generate_predictions(triangs, pairs_of_points, 3, "triangs")

    ct, ft = analysis.calculate_percentage_corner(triangs, triangs_pred, GRID_WIDTH, GRID_HEIGHT)
    print("Triangles [Model ]: in corner {c}%, outiside corner {o}%".format(c=100*ct, o=100*ft))

    analysis.show_indiv_shape(triangs[33704], triangs_pred[33704], GRID_WIDTH, GRID_HEIGHT)
    analysis.show_indiv_shape(triangs[30349], triangs_pred[30349], GRID_WIDTH, GRID_HEIGHT)
    analysis.show_indiv_shape(triangs[4447], triangs_pred[4447], GRID_WIDTH, GRID_HEIGHT)

def gen_triangle_human_data(area_range):
    triangs = generate_triangles(Point(GRID_WIDTH, GRID_HEIGHT), area_range)

    triangs_pred = np.zeros((3, GRID_WIDTH, GRID_HEIGHT))
    triangs_pred[0][5][8] = 3
    triangs_pred[0][4][1] = 6
    triangs_pred[0][8][4] = 5
    triangs_pred[0][4][4] = 1
    triangs_pred[0][7][5] = 1
    triangs_pred[0][6][6] = 2
    triangs_pred[0][6][7] = 1
    triangs_pred[0][4][5] = 1

    triangs_pred[1][4][5] = 8
    triangs_pred[1][9][7] = 7
    triangs_pred[1][6][4] = 2
    triangs_pred[1][8][6] = 1
    triangs_pred[1][5][6] = 1
    triangs_pred[1][7][5] = 1

    triangs_pred[2][5][4] = 2
    triangs_pred[2][8][2] = 8
    triangs_pred[2][2][3] = 6
    triangs_pred[2][6][4] = 1
    triangs_pred[2][3][3] = 1
    triangs_pred[2][5][2] = 1
    triangs_pred[2][7][3] = 1

    ct, ft = analysis.calculate_percentage_corner([triangs[33704], triangs[30349], triangs[4447]], triangs_pred, GRID_WIDTH, GRID_HEIGHT)
    print("Triangles [Human]: in corner {c}%, outside corner {o}%".format(c=100*ct, o=100*ft))

    analysis.show_indiv_shape(triangs[33704], triangs_pred[0], GRID_WIDTH, GRID_HEIGHT)
    analysis.show_indiv_shape(triangs[30349], triangs_pred[1], GRID_WIDTH, GRID_HEIGHT)
    analysis.show_indiv_shape(triangs[4447], triangs_pred[2], GRID_WIDTH, GRID_HEIGHT)    

def gen_circle_preds(area_range, pairs_of_points):
    circles = generate_circles(Point(GRID_WIDTH, GRID_HEIGHT), area_range)
    print(f"circs: {len(circles)}")
    circ_pred = generate_predictions(circles, pairs_of_points, 3, "circs")

    cc, fc = analysis.calculate_percentage_boundary(circles, circ_pred, GRID_WIDTH, GRID_HEIGHT)
    print("Circles [Model]: on boundary {c}%, outside boundary {o}%".format(c=100*cc, o=100*fc))

    analysis.show_indiv_shape(circles[15], circ_pred[15], GRID_WIDTH, GRID_HEIGHT)
    analysis.show_indiv_shape(circles[48], circ_pred[48], GRID_WIDTH, GRID_HEIGHT)
    analysis.show_indiv_shape(circles[36], circ_pred[36], GRID_WIDTH, GRID_HEIGHT)

def gen_circle_human_data(area_range):
    circles = generate_circles(Point(GRID_WIDTH, GRID_HEIGHT), area_range)

    circ_pred = np.zeros((3, GRID_WIDTH, GRID_HEIGHT))
    circ_pred[0][3][9] = 4
    circ_pred[0][2][7] = 1
    circ_pred[0][2][8] = 2
    circ_pred[0][3][6] = 4
    circ_pred[0][4][6] = 3
    circ_pred[0][5][7] = 3
    circ_pred[0][4][9] = 3

    circ_pred[1][5][9] = 3
    circ_pred[1][4][6] = 1
    circ_pred[1][4][8] = 2
    circ_pred[1][5][4] = 3
    circ_pred[1][8][4] = 2
    circ_pred[1][6][4] = 1
    circ_pred[1][9][6] = 1
    circ_pred[1][9][5] = 3
    circ_pred[1][8][9] = 3
    circ_pred[1][6][9] = 1

    circ_pred[2][3][8] = 4
    circ_pred[2][2][5] = 1
    circ_pred[2][4][9] = 2
    circ_pred[2][4][2] = 2
    circ_pred[2][8][3] = 4
    circ_pred[2][5][2] = 1
    circ_pred[2][9][5] = 1
    circ_pred[2][7][2] = 2
    circ_pred[2][7][9] = 2
    circ_pred[2][5][9] = 1

    cc, fc = analysis.calculate_percentage_boundary([circles[15], circles[48], circles[36]], circ_pred, GRID_WIDTH, GRID_HEIGHT)
    print("Circles [Human]: on boundary {c}%, outside boundary {o}%".format(c=100*cc, o=100*fc))

    analysis.show_indiv_shape(circles[15], circ_pred[0], GRID_WIDTH, GRID_HEIGHT)
    analysis.show_indiv_shape(circles[48], circ_pred[1], GRID_WIDTH, GRID_HEIGHT)
    analysis.show_indiv_shape(circles[36], circ_pred[2], GRID_WIDTH, GRID_HEIGHT)

def gen_rectangle_preds(area_range, pairs_of_points):
    rects = generate_rectangles(Point(GRID_WIDTH, GRID_HEIGHT), area_range)
    print(f"rects: {len(rects)}")
    rects_pred = generate_predictions(rects, pairs_of_points, 3, "rects")

    cr, fr = analysis.calculate_percentage_corner(rects, rects_pred, GRID_WIDTH, GRID_HEIGHT)
    print("Rectangles [Model]: in corner {c}%, outside corner {o}%".format(c=100*cr, o=100*fr))

    analysis.show_indiv_shape(rects[216], rects_pred[216], GRID_WIDTH, GRID_HEIGHT)
    analysis.show_indiv_shape(rects[862], rects_pred[862], GRID_WIDTH, GRID_HEIGHT)
    analysis.show_indiv_shape(rects[652], rects_pred[652], GRID_WIDTH, GRID_HEIGHT)

def gen_rectangle_human_data(area_range):
    rects = generate_rectangles(Point(GRID_WIDTH, GRID_HEIGHT), area_range)
    print(f"rects: {len(rects)}")

    rects_pred = np.zeros((3, GRID_WIDTH, GRID_HEIGHT))
    rects_pred[0][1][7] = 4
    rects_pred[0][1][9] = 6
    rects_pred[0][6][7] = 6
    rects_pred[0][6][9] = 4

    rects_pred[1][7][2] = 3
    rects_pred[1][7][5] = 7
    rects_pred[1][9][5] = 3
    rects_pred[1][9][2] = 7

    rects_pred[2][4][7] = 8
    rects_pred[2][4][3] = 2
    rects_pred[2][8][3] = 8
    rects_pred[2][8][7] = 2
    cr, fr = analysis.calculate_percentage_corner([rects[216], rects[862], rects[652]], rects_pred, GRID_WIDTH, GRID_HEIGHT)
    print("Rectangles [Human]: in corner {c}%, outside corner {o}%".format(c=100*cr, o=100*fr))

    analysis.show_indiv_shape(rects[216], rects_pred[0], GRID_WIDTH, GRID_HEIGHT)
    analysis.show_indiv_shape(rects[862], rects_pred[1], GRID_WIDTH, GRID_HEIGHT)
    analysis.show_indiv_shape(rects[652], rects_pred[2], GRID_WIDTH, GRID_HEIGHT)

def main():
    area_range = [0.1*GRID_WIDTH*GRID_HEIGHT, 0.7*GRID_WIDTH*GRID_HEIGHT]
    pairs_of_points = generate_data()

    gen_circle_preds(area_range, pairs_of_points)
    gen_circle_human_data(area_range)

    gen_rectangle_preds(area_range, pairs_of_points)
    gen_rectangle_human_data(area_range)

    gen_triangle_preds([0.1*GRID_WIDTH*GRID_HEIGHT, 0.25*GRID_WIDTH*GRID_HEIGHT], pairs_of_points)
    gen_triangle_human_data([0.1*GRID_WIDTH*GRID_HEIGHT, 0.25*GRID_WIDTH*GRID_HEIGHT])

    analysis.gen_boundary_vis()


if __name__ == "__main__":
    main()
