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


@dataclass
class Graph:
    """ A graph of people.
    """
    _vertices: Dict[str, _Person]  # Vertices mapping the names


def load_graph_from_csv() -> Graph:



