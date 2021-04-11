from math import e
from typing import Optional, Tuple

INFECTED_COLOUR = (255, 0, 0)


def degrees_apart_get_colour(degrees_apart: Optional[int]) -> Tuple[int, int, int]:
    """ Given a degrees_apart, return the appropriate colour of the person. The colour calculation
    is a sigmoid function.
    """
    if degrees_apart is None:
        return 255, 255, 255  # white

    stretch = 2.2
    offset = 4.4  # Hard coded values for sigmoid curve

    percent_fill = 1 / (1 + e ** (stretch * degrees_apart - offset))  # Sigmoid function
    return (int(INFECTED_COLOUR[0] * percent_fill),
            int(INFECTED_COLOUR[1] * percent_fill),
            int(INFECTED_COLOUR[2] * percent_fill))


def rgb_to_str(rgb: Tuple[int, int, int]) -> str:
    """ Converts a colour from a tuple of ints to to a string in the form "rgb(255, 255, 255)".
    """
    return 'rgb({}, {}, {})'.format(rgb[0], rgb[1], rgb[2])