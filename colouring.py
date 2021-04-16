"""CSC111 Project: COVID-19 Contact Visualizer

Module Description
==================
Colouring Module
This module contains the functions used to calculate and update the colours for the contact
visualization. Due to frequent similar calls, results are memoized using the @cache decorator.

Copyright and Usage Information
===============================
This file is Copyright (c) 2021 Simon Chen, Patricia Ding, Salman Husainie, Makayla Duffus
"""
from math import e, log
from typing import Optional, Tuple
from functools import cache


# DEGREES APART CONSTANTS
INFECTED_COLOUR = (255, 0, 0)

MIN_FILL = 0.95
STRETCH = 0.6
OFFSET = log(MIN_FILL)  # for the degrees apart exponential curve


@cache  # To avoid unnecessary re-calculations
def degrees_apart_get_colour(degrees_apart: Optional[int]) -> Tuple[int, int, int]:
    """ Given a degrees_apart, return the appropriate colour of the person.
    The colour calculation is an exponential decay function.

    >>> degrees_apart_get_colour(0)  # Based off of INFECTED_COLOUR
    (255, 0, 0)
    >>> degrees_apart_get_colour(2)  # Exponential decay starts
    (255, 169, 169)
    """
    # Hard coded base case degree colours
    if degrees_apart is None:
        return 255, 255, 255  # white
    elif degrees_apart == 0:
        return INFECTED_COLOUR

    percent_fill = -(e ** -(STRETCH * degrees_apart - OFFSET)) + MIN_FILL  # Exponential curve
    # Gradient from INFECTED_COLOUR to white
    return (int(INFECTED_COLOUR[0] + ((255 - INFECTED_COLOUR[0]) * percent_fill)),
            int(INFECTED_COLOUR[1] + ((255 - INFECTED_COLOUR[1]) * percent_fill)),
            int(INFECTED_COLOUR[2] + ((255 - INFECTED_COLOUR[2]) * percent_fill)))


@cache
def rgb_to_str(rgb: Tuple[int, int, int]) -> str:
    """ Converts a colour from a tuple of ints to to a string in the form "rgb(255, 255, 255)".

    >>> rgb_to_str((255, 255, 255))
    "rgb(255, 255, 255)"
    """
    return 'rgb({}, {}, {})'.format(rgb[0], rgb[1], rgb[2])
