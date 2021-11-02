import matplotlib.pyplot as plt
import numpy

def plot(coords):
    """
    Shows color-coded transition (each marcher will be a different color, should be used only to test the transition solver.)
    @Param coords: list of (x, y) tuples
    Usage note: plt.show() should be called once you are done calling plot() to show all the plots you have created.
    """
    # seed random so colors will be the same if two things are plotted back-to-back
    numpy.random.seed(47289758)

    x_list = [coord[0] for coord in coords]
    y_list = [coord[1] for coord in coords]
    colors = numpy.random.rand(len(coords))

    plt.figure()
    plt.scatter(x_list, y_list, c=colors)

if __name__ == "__main__":
    plot([(0, 16), (0, 8), (8, 8), (8, 16)])
    plot([(0, 8), (0, 16), (8, 8), (8, 16)])
    plt.show()