import networkx as nx
from plotly.graph_objs import Scatter, Figure
from graph import Graph
from typing import Tuple

INFECTED_COLOUR = (255, 0, 0)


# Degrees visualization
def render_degrees_apart(graph: Graph, init_infected: set[str]) -> None:
    """ Render the degrees visualization given a graph, and the initial set of infected people.

    Preconditions:
        - all(not person.infected for person in graph._people.values())
    """
    # Degree calculation
    graph.set_infected(init_infected)
    graph.recalculate_degrees()

    # Display


def degrees_apart_get_colour(degrees_apart: int) -> Tuple[int, int, int]:
    """ Given a degrees_apart, return the appropriate colour of the person. The colour calculation
    is a reciprocal function
    """
    percent_fill = 1 / (degrees_apart + 1)
    return (int(INFECTED_COLOUR[0] * percent_fill),
            int(INFECTED_COLOUR[1] * percent_fill),
            int(INFECTED_COLOUR[2] * percent_fill))


def rgb_to_str(rgb: Tuple[int, int, int]) -> str:
    """ Converts a colour from a tuple of ints to to a string in the form "rgb(255, 255, 255)".
    """
    return 'rgb({}, {}, {})'.format(rgb[0], rgb[1], rgb[2])
