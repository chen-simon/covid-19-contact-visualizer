""" COVID-19 Contact Visualizer

Graph Module
This module contains the graph classes that store the contact tracing data.

This file is Copyright (c) 2021 Supreme Simon Chen, Patricia Ding, Salman Husainie, Makayla Duffus
"""
from __future__ import annotations
from typing import Dict, Optional
import csv


class _Person:
    """A person who undergoes contact tracing. Represents a vertex in a graph.

        Instance Attributes:
            - identifier: The unique identifier of the person
            - name: The person's first and last name
            - age: The person's age
            - severity_level: The severity of COVID-19 the person would experience if they develop
              the illness
            - infected: True if the person has developed COVID-19, false otherwise.
            - neighbours: People in this person's social circle, and their corresponding level of
              contact with this person
            - degrees_apart: The degree of separation between this person and an infected person in
              Degree Mode

        Representation Invariants:
            - self not in self.neighbours
            - all(self in u.neighbours for u in self.neighbours)
            - self.age >= 0
            - 1 <= self.severity_level <= 3
    """
    identifier: str
    name: str
    age: int
    severity_level: float
    infected: bool
    neighbours: Dict[_Person, float]
    degrees_apart: Optional[int] = None

    def __init__(self, identifier: str, name: str,  age: int, severity_level: float) -> None:
        """Initialize a new person vertex with the given name, identifier, age, and severity level.
        """
        self.identifier = identifier
        self.name = name
        self.age = age
        self.severity_level = severity_level
        self.infected = False
        self.neighbours = {}

    # BASIC METHODS
    def change_infection_status(self) -> None:
        """Reverses the current infection status of the person."""
        self.infected = not self.infected

    # SIMULATION CALCULATION
    #    TODO: put simulation vertex methods here

    # DEGREE CALCULATION
    def calculate_degrees_apart(self, curr_degree: int, visited: set) -> None:
        """Update degrees_apart for all the people this person is connected to,
        where degrees_apart is the smallest degree apart between this person and an infected
        person.
        """
        # This will ensure that degrees_apart is always calculating the smallest degree between
        # an infected person.
        if self.degrees_apart is None or curr_degree < self.degrees_apart:
            self.degrees_apart = curr_degree

        visited.add(self)
        for person in self.neighbours:
            if person not in visited:
                person.calculate_degrees_apart(curr_degree + 1, visited.copy())

    def get_degree(self) -> int:
        """Return smallest degree apart from an infected vertex. Raise ValueError if has not
        been calculated yet.
        """
        if self.degrees_apart is not None:
            return self.degrees_apart
        raise ValueError

    def reset_degree(self) -> None:
        """Resets the degrees_apart attribute to None to represent an uncalculated value."""
        self.degrees_apart = None


class Graph:
    """A weighted graph used to represent a network of people that keeps track of the level of
    contact between any two people.
    """
    # Private Instance Attributes:
    #     - _people:
    #         A collection of the people in this graph.
    #         Maps person identifier to _Person object.
    _people: Dict[str, _Person]

    def __init__(self) -> None:
        """Initialize an empty graph."""
        self._people = {}

    def add_vertex(self, identifier: str, name: str, age: int, severity_level: float) -> None:
        """Add a vertex with the given identifier, name, age, and severity level to this graph.
        """
        if identifier not in self._people:
            self._people[identifier] = _Person(identifier, name, age, severity_level)

    def add_edge(self, identifier1: str, identifier2: str, contact_level: float) -> None:
        """Add an edge between two people with the given identifiers in this graph, with the given
        weight, representing their level of contact.

        Raise a ValueError if identifier1 or identifier2 are not vertices in this graph.

        Preconditions:
            - identifier1 != identifier2
        """
        if identifier1 in self._people and identifier2 in self._people:
            person1 = self._people[identifier1]
            person2 = self._people[identifier2]

            person1.neighbours[person2] = contact_level
            person2.neighbours[person1] = contact_level

        else:
            raise ValueError

    def get_contact_level(self, identifier1: str, identifier2: str) -> float:
        """Return the level of contact between the given items (the weight of their edge).

        Return 0 if identifier1 and identifier2 are not adjacent.
        """
        person1 = self._people[identifier1]
        person2 = self._people[identifier2]

        return person1.neighbours.get(person2, 0)


def load_graph_csv(names_file: str, contact_file: str) -> Graph:
    """ Return a Graph from the corresponding names file and contacts file which are in .csv format.
    """
    graph = Graph()

    with open(names_file) as f:
        reader1 = csv.reader(f)
        next(reader1)

        for identifier, name, age, severity in reader1:
            graph.add_vertex(identifier, name, int(age), float(severity))

    with open(contact_file) as f:
        reader2 = csv.reader(f)
        next(reader2)

        for id1, id2, weight in reader2:
            graph.add_edge(id1, id2, float(weight))

    return graph


def load_graph_json(names_file: str, contact_file: str) -> Graph:
    """ Return a Graph from the corresponding names file and contacts file which are in .json
    format.
    """
    # TODO: Implement this method if we're feeling spicy
