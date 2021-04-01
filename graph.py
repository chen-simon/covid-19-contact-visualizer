""" COVID-19 Contact Visualizer
    Copyright Simon Chen, Patricia Ding, Salman Husainie, Makayla Duffus
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class _Person:
    """ A vertex in a graph. Each vertex corresponds to a person. Each of its neighbours is a
        contact.
    """
    _name: str
    _neighbours: Dict[_Person, float]  # These include weighted edges

    _age: int

    _degrees_apart: int  # Used for degree calculation; value is -1 if not calculated

    # BASIC METHODS
    #    TODO: put basic vertex methods here

    # SIMULATION CALCULATION
    #    TODO: put simulation vertex methods here

    # DEGREE CALCULATION
    def calculate_degrees_apart(self, curr_degree: int, visited: set) -> None:
        """ Update the _degrees_apart for all of its neighbours.
        """
        if not self.has_degree() or curr_degree < self._degrees_apart:
            self._degrees_apart = curr_degree

        visited.add(self)
        for person in self._neighbours:
            if person not in visited:
                person.calculate_degrees_apart(curr_degree + 1, visited.copy())

    def has_degree(self):
        """ Determine whether ar not the degree is calculated or not.
        """
        return self._degrees_apart != -1

    def get_degree(self):
        """ Return smallest degree apart from an infected vertex. Raise ValueError if has not
            been calculated yet.
        """
        if self.has_degree():
            return self._degrees_apart
        raise ValueError
    
    def reset_degree(self):
        """ Resets the _degrees_apart attribute to -1 to represent an uncalculated value
        """
        self._degrees_apart = -1


@dataclass
class Graph:
    """ A graph of people.
    """
    _vertices: Dict[str, _Person]  # Vertices mapping the names


def load_graph_from_csv() -> Graph:
    pass
