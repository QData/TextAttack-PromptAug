import os
import sys
import matplotlib.pyplot as plt

from utils import json_to_shapes
from constants import X_MIN, X_MAX, Y_MIN, Y_MAX


def plot_canvas(filepath):
    fig, ax = plt.subplots()
    fig.set_size_inches(10, 10)

    # Scale the ticks correctly for plotting
    ax.set_xticks(range(X_MIN, X_MAX + 1))
    ax.set_yticks(range(Y_MIN, Y_MAX + 1))

    # Make the ticks not visible
    ax.tick_params(
        axis="both", 
        which="both", 
        bottom=False,
        top=False,
        left=False,
        right=False, 
        labelleft=False,
        labelbottom=False
    )


    shapes = json_to_shapes(filepath)
    for shape in shapes:
        ax.add_patch(shape.get_plot_shape())

    basename, _ = os.path.splitext(os.path.basename(filepath))
    if not os.path.isdir("plots"):
        os.makedirs("plots")
    plt.savefig(f"plots/{basename}.jpg")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python plot_canvas.py <path to data file>")
        exit()

    plot_canvas(sys.argv[1])
