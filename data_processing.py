"""CSC111 Project: COVID-19 Contact Visualizer

Module Description
==================
Data Processing Module
This module contains the functions that load, process, and generate data to create a graph
representing people and connections.

Copyright and Usage Information
===============================
This file is Copyright (c) 2021 Simon Chen, Patricia Ding, Salman Husainie, and Makayla Duffus.
"""
from __future__ import annotations
import csv
import random
import string
from social_graph import Graph


def load_graph_csv(names_file: str, contact_file: str) -> Graph:
    """Return a Graph from the corresponding names_file and contact_file.

    Preconditions:
        - names_file and contact_file are in .csv format
    """
    graph = Graph()

    # Add vertices from names_file
    with open(names_file) as f:
        reader1 = csv.reader(f)
        next(reader1)

        for identifier, name, age, severity in reader1:
            graph.add_vertex(identifier, name, int(age), float(severity))

    # Add weighted edges from contact_file
    with open(contact_file) as f:
        reader2 = csv.reader(f)
        next(reader2)

        for id1, id2, weight in reader2:
            graph.add_edge(id1, id2, float(weight))

    return graph


# =========================
# Data Generation Functions
# =========================
def generate_connected_graph(n: int, level: str = 'medium') -> Graph:
    """Return a connected Graph containing n _Person objects with n + n // 5 total edges.

    The level, (high, medium, low) determines the range from which the weight between edges is
    chosen.

    Preconditions:
        - 10 <= n <= 60
        - level in {'high', 'medium', 'low'}
    """
    edges = n + n // 5
    people = []
    graph = Graph()

    # Add n _Person objects with randomly generated attributes to the graph
    for _ in range(0, n):
        identity, name = _generate_id_and_name(graph)
        people.append(identity)
        graph.add_vertex(identity, name, random.randint(18, 55), random.uniform(0, 1))

    remaining, visited = set(people), set()

    current_person = random.choice(list(remaining))
    remaining.remove(current_person)
    visited.add(current_person)

    # LOOP ACCUMULATOR: store the number of edges in the graph so far
    edges_so_far = 0

    while remaining != set():
        new_neighbor = random.choice(people)

        if new_neighbor not in visited:
            graph.add_edge(current_person, new_neighbor, get_leveled_weight(level))
            edges_so_far += 1
            remaining.remove(new_neighbor)
            visited.add(new_neighbor)

        current_person = new_neighbor   # Move on to the next person

    # Adding edges until max edge number is met
    while edges_so_far < edges:
        # Checking in case person_1 and person_2 are the same person
        person_1, person_2 = random.choice(people), random.choice(people)
        if person_1 != person_2:
            graph.add_edge(person_1, person_2, get_leveled_weight(level))
            edges_so_far += 1

    return graph


def generate_disconnected_graph(n: int, level: str = 'medium') -> Graph:
    """Return a non-connected graph of n _Person objects. The returned graph has a larger connected
     portion and a random smaller number of clusters/lone objects.

    The level, (high, medium, low) determines the range from which the weight
    between edges is chosen.

    Preconditions:
        - 10 <= n <= 60
        - level in {'high', 'low', 'medium'}
    """
    num_of_disconnected = n // 5
    graph = generate_connected_graph(n - num_of_disconnected, level)

    # LOOP ACCUMULATOR: stores the identifiers for the loner _Person objects
    loner = []

    # Add num_of_disconnected _Person objects with randomly generated information to the graph
    for _ in range(0, num_of_disconnected):
        identity, name = _generate_id_and_name(graph)
        loner.append(identity)
        graph.add_vertex(identity, name, random.randint(18, 55), get_leveled_weight(level))

    # Number of times connections between lone _Person objects will be made
    times = random.randint(0, num_of_disconnected // 2)

    # Adds random edges between lone _Person objects
    for _ in range(times):
        to_be_connected = _random_list_of_two(loner)
        graph.add_edge(to_be_connected[0], to_be_connected[1], get_leveled_weight(level))

    return graph


def _random_list_of_two(people: list[str]) -> list[str]:
    """Return a randomly generated list of two strings representing _Person identifier attributes.

    Preconditions:
        - len(people) >= 2
        - any(x != y for x in people for y in people)
    """
    person_1 = random.choice(people)
    person_2 = random.choice(people)

    if person_2 != person_1:
        return [person_1, person_2]
    else:
        return _random_list_of_two(people)


def _generate_id_and_name(graph: Graph) -> tuple[str, str]:
    """Return a tuple containing the following strings:
        1. A 6-digit id composed of uppercase ASCII letters and numbers for a _Person object.
        2. The initials for the name attribute of a _Person object.
    """
    id_chars = string.ascii_uppercase + string.digits
    name_chars = string.ascii_uppercase
    id_and_name = (''.join(random.choice(id_chars) for _ in range(6)), random.choice(name_chars)
                   + '. ' + random.choice(name_chars))

    if id_and_name[1] in graph.get_names():
        # If the name is already present in the graph, run the function again
        return _generate_id_and_name(graph)
    else:
        return id_and_name


def get_leveled_weight(level: str) -> float:
    """Return a float value to represent the weight of an edge between two _Person objects
    according to the given level. The level, (high, medium, low) determines the range from which the
    random float value is chosen.

    The range per level is as follows, where w is the weight:
        - 'high': 0.65 <= w <= 1.0
        - 'medium': 0.45 <= w <= 0.6
        - 'low': 0.05 <= w <= 0.4

    Preconditions:
        - level in {'high', 'low', 'medium'}
    """
    if level == 'high':
        weight = random.uniform(0.65, 1.0)
    elif level == 'medium':
        weight = random.uniform(0.45, 0.6)
    else:  # type == 'low'
        weight = random.uniform(0.05, 0.4)

    return weight


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    import python_ta.contracts
    python_ta.contracts.check_all_contracts()

    import python_ta
    python_ta.check_all(config={
        'extra-imports': ['csv', 'networkx', 'string', 'random', 'social_graph'],
        'max-line-length': 100,
        'allowed-io': ['load_graph_csv'],
        'disable': ['E1136']
    })
