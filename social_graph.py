"""CSC111 Project: COVID-19 Contact Visualizer

Module Description
==================
Social Graph Dataclasses Module
This module contains the classes that store the contact tracing data.

Copyright and Usage Information
===============================
This file is Copyright (c) 2021 Simon Chen, Patricia Ding, Salman Husainie, Makayla Duffus
"""
from __future__ import annotations
from typing import Any, Dict, Optional
import colouring as colour
import networkx as nx


class _Person:
    """ A person who undergoes contact tracing. Represents a vertex in a graph.

        Instance Attributes:
            - identifier: The unique identifier of the person.
            - name: The person's first and last name.
            - age: The person's age.
            - severity_level: The severity of COVID-19 the person would experience if they develop
              the illness.
            - infected: True if the person has developed COVID-19, False otherwise.
            - neighbours: The people in this person's social circle, and their corresponding level
              of contact with this person. Maps _Person object to their contact level to self.
            - degrees_apart: The degree of separation between this person and an infected person in
              Degree Mode.

        Representation Invariants:
            - self not in self.neighbours
            - all(self in u.neighbours for u in self.neighbours)
            - self.age >= 0
            - 0 <= self.severity_level <= 1
    """
    identifier: str
    name: str
    age: int
    severity_level: float
    infected: bool
    neighbours: Dict[_Person, float]
    degrees_apart: Optional[int] = None

    def __init__(self, identifier: str, name: str, age: int, severity_level: float) -> None:
        """ Initialize a new person vertex with the given name, identifier, age, and severity level.
        """
        self.identifier = identifier
        self.name = name
        self.age = age
        self.severity_level = severity_level
        self.infected = False
        self.neighbours = {}

    # BASIC METHODS
    def change_infection_status(self) -> None:
        """ Reverses the current infection status of the person."""
        self.infected = not self.infected

    # DEGREE CALCULATION
    def calculate_degrees_apart(self, curr_degree: int, visited: set,
                                init_call: bool = True) -> None:
        """ Update degrees_apart for all the people this person is connected to,
        where degrees_apart is the smallest degree apart between this person and an infected
        person.
        """
        # This will ensure that degrees_apart is always calculating the smallest degree between
        # an infected person.
        if not init_call and curr_degree == 0:
            return  # To avoid redundant calculations

        if self.degrees_apart is None or curr_degree < self.degrees_apart:
            self.degrees_apart = curr_degree

        visited.add(self)
        for person in self.neighbours:
            if person not in visited:
                person.calculate_degrees_apart(curr_degree + 1, visited.copy(), False)

    def get_degree(self) -> int:
        """ Return smallest degree apart from an infected vertex. Raise ValueError if has not
        been calculated yet.
        """
        if self.degrees_apart is not None:
            return self.degrees_apart
        raise ValueError

    def reset_degree(self, zero: Optional[bool] = False) -> None:
        """ Resets the degrees_apart attribute to None to represent an uncalculated value.
        If zero is true, set it to 0 instead.
        """
        if zero:
            self.degrees_apart = 0
        else:
            self.degrees_apart = None


class Graph:
    """ A weighted graph used to represent a network of people that keeps track of the level of
    contact between any two people.
    """
    # Private Instance Attributes:
    #     - _people:
    #         A collection of the people in this graph.
    #         Maps person identifier to _Person object.
    _people: Dict[str, _Person]

    def __init__(self) -> None:
        """ Initialize an empty graph."""
        self._people = {}

    def get_people(self) -> Dict[str, _Person]:
        """ Return a __ of all the people"""
        return self._people

    def get_neighbours(self, item: Any):
        """ Return the neighbours of this person"""
        return list(self._people[item].neighbours)

    def get_weight(self, person1: Any, person2: Any) -> float:
        """ Return the weight between person1 and person2"""
        return self._people[person1].neighbours[person2]

    def get_names(self) -> set[str]:
        """ Return a set containing the names of every _Person object in this graph.
        """
        names_so_far = set()

        for person in self._people:
            names_so_far.add(self._people[person].name)

        return names_so_far

    def add_vertex(self, identifier: str, name: str, age: int, severity_level: float) -> None:
        """ Add a vertex with the given identifier, name, age, and severity level to this graph.
        """
        if identifier not in self._people:
            self._people[identifier] = _Person(identifier, name, age, severity_level)

    def add_edge(self, identifier1: str, identifier2: str, contact_level: float) -> None:
        """ Add an edge between two people with the given identifiers in this graph, with the given
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

    def set_infected(self, init_infected: set[str]) -> None:
        """ Sets the initial infected people for the graph, given their ids
        """
        for identifier in init_infected:
            self._people[identifier].infected = True

    def recalculate_degrees(self) -> None:
        """ Recalculates the degrees_apart attribute for each connected person to an infected.
        """
        self._reset_degrees()

        infected_people = set()

        for person in self._people.values():
            if person.infected:
                person.reset_degree(zero=True)
                infected_people.add(person)

        for infected_person in infected_people:
            # This method calculates it for its neighbours
            infected_person.calculate_degrees_apart(0, set())

    def _reset_degrees(self) -> None:
        """ Resets all degrees_apart attributes in graph to be None
        """
        for person in self._people.values():
            person.reset_degree()  # Reset all degrees to None

    def to_nx(self) -> nx.Graph:
        """ Return a networkx Graph representing self."""

        graph_nx = nx.Graph()
        for p in self._people.values():
            graph_nx.add_node(p.name, colour='rgb(155, 234, 58)')  # add node for each person

            for u in p.neighbours:
                if u.name in graph_nx.nodes:
                    graph_nx.add_edge(p.name, u.name)  # add edge edge between each neighbour pair

        return graph_nx

    def to_nx_with_degree_colour(self) -> nx.Graph:
        """ Return a networkx Graph representing self. This function also sets an additional
        attribute, 'colour', for each node in the networkx graph.
        """
        graph_nx = nx.Graph()

        for p in self._people.values():
            graph_nx.add_node(p.name)  # add node for each person
            node_colour = colour.rgb_to_str(colour.degrees_apart_get_colour(p.degrees_apart))
            graph_nx.nodes[p.name]['colour'] = node_colour

            for u in p.neighbours:
                if u.name in graph_nx.nodes:
                    graph_nx.add_edge(p.name, u.name)  # add edge edge between each neighbour pair

        return graph_nx

    def to_nx_with_simulation_colour(self) -> nx.Graph:
        """ Return a networkx Graph representing self. This function also sets an additional
        attribute, 'colour', for each node in the networkx graph.

        This function is used for the simulations.
        """
        graph_nx = nx.Graph()

        for p in self._people.values():
            graph_nx.add_node(p.name)  # add node for each person
            node_colour = colour.rgb_to_str(colour.INFECTED_COLOUR) if p.infected else 'rgb(255, ' \
                                                                                       '255, 255) '
            graph_nx.nodes[p.name]['colour'] = node_colour

            for u in p.neighbours:
                if u.name in graph_nx.nodes:
                    graph_nx.add_edge(p.name, u.name)  # add edge edge between each neighbour pair

        return graph_nx
