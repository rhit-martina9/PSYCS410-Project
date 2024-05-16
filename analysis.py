import matplotlib.pyplot as plt
import numpy as np
from shapezzz import Point

def show_indiv_shape(shape, preds, width, height):
    preds = np.transpose(preds)
    fig, ax = plt.subplots()
    ax.imshow(preds, cmap="Blues", origin="lower")

    shape_patch = shape.drawShape()
    ax.add_patch(shape_patch)
    ax.set_xlim(xmin=0, xmax=width)
    ax.set_ylim(ymin=0, ymax=height)

    ax.set_xticks(np.arange(0, width+1, 1))
    ax.set_yticks(np.arange(0, height+1, 1))
    ax.grid(True, markevery=1, color="k")
    plt.show()

def calculate_percentage_corner(shapes, preds, width, height):
    num_close = 0.0
    num_far = 0.0
    for s in range(len(shapes)):
        for x in range(width):
            for y in range(height):
                    if shapes[s].is_point_on_corner(Point(x,y)):
                        num_close += preds[s][x][y]
                    else:
                         num_far += preds[s][x][y]
    percent_close = num_close / (num_close + num_far)
    percent_far = num_far / (num_close + num_far)
    return (percent_close, percent_far)

def calculate_percentage_boundary(shapes, preds, width, height):
    num_close = 0.0
    num_far = 0.0
    for s in range(len(shapes)):
        for x in range(width):
            for y in range(height):
                    if shapes[s].is_point_on_shape_boundary(Point(x,y)):
                        num_close += preds[s][x][y]
                    else:
                         num_far += preds[s][x][y]
    percent_close = num_close / (num_close + num_far)
    percent_far = num_far / (num_close + num_far)
    return (percent_close, percent_far)

def gen_boundary_vis():
    shapes = ["Rectangles", "Circles", "Triangles"]
    label = ["Corner", "Boundary", "Corner"]
    data_type = ["Model", "Human"]
    data = []
    data.append({"In Corner": np.array([0.893849, 1]), "Outside Corner": np.array([0.106151, 0])})
    data.append({"On Boundary": np.array([0.803692, 1]), "Outside Bundary": np.array([0.196308, 0])})
    data.append({"In Corner": np.array([0.958974, 0.7]), "Outside Corner": np.array([0.041026, 0.3])})

    for i in range(len(shapes)):
        fig, ax = plt.subplots()
        bottom = np.array([0.0,0.0])

        for boolean, percent in data[i].items():
            p = ax.bar(data_type, percent, 0.5, label=boolean, bottom=bottom)
            bottom += percent

        ax.set_title("Percent of Predictions on the " + label[i] + " of " + shapes[i])
        ax.set_ylim(ymin=0, ymax=1)
        ax.legend(loc="upper right")

        plt.show()




