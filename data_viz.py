import matplotlib.pyplot as plt
import numpy as np

def show_indiv_shape(shape, preds, width, height):
    preds = np.transpose(preds)
    fig, ax = plt.subplots()
    ax.imshow(preds, cmap="Blues", origin="lower")

    shape_patch = shape.drawShape()
    ax.add_patch(shape_patch)

    ax.set_xticks(np.arange(0, width, 1))
    ax.set_yticks(np.arange(0, height, 1))
    ax.grid(True, markevery=1, color="k")
    plt.show()

def show_summary(shapes, type):
    pass