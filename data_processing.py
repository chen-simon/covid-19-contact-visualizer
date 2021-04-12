"""CSC111 Project: COVID-19 Contact Visualizer

Module Description
==================
Data Processing Module
This module contains the functions that extract, process, and generate data for the
COVID-19 contact visualizer.

Copyright and Usage Information
===============================
This file is Copyright (c) 2021 Simon Chen, Patricia Ding, Salman Husainie, and Makayla Duffus.
"""
from __future__ import annotations
import csv
import random
import string
from typing import Tuple, List
from dataclasses import Graph


def load_graph_csv(names_file: str, contact_file: str) -> Graph:
    """ Return a Graph from the corresponding names_file and contact_file.

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


def generate_connected_graph_no_csv(n: int) -> Graph:
    """ Return a connected Graph containing n _Person objects with
        n + n // 5 total edges.

        Preconditions:
            - 5 <= n <= 100
    """
    edges = n + n // 5
    people = []
    graph = Graph()

    # Add n _Person objects with randomly generated attributes to the graph
    for _ in range(0, n):
        identity, name = _generate_id_and_name()
        people.append(identity)
        graph.add_vertex(identity, name, random.randint(18, 55), random.uniform(0, 1))

    remaining, visited = set(people), set()

    current_person = random.choice(list(remaining))
    remaining.remove(current_person)
    visited.add(current_person)

    # LOOP ACCUMULATOR: store the number of edges in the graph so far
    edges_so_far = 0

    while remaining != set():
        new_neighbor = random.choice(people)    # Check if error

        if new_neighbor not in visited:
            graph.add_edge(current_person, new_neighbor, random.uniform(0, 1))
            edges_so_far += 1
            remaining.remove(new_neighbor)
            visited.add(new_neighbor)

        current_person = new_neighbor   # Move on to the next person

    while edges_so_far < edges:
        # Checking in case person_1 and person_2 are the same person
        person_1, person_2 = random.choice(people), random.choice(people)
        if person_1 != person_2:
            graph.add_edge(person_1, person_2, random.uniform(0, 1))
            edges_so_far += 1

    return graph


def _random_list(people: List[str]) -> List[str]:
    """Return a randomly generated list with at most len(people) // 2 strings

    Preconditions:
        - len(people) >= 5
    """
    new_list = []
    length = random.randint(2, len(people) // 2)
    for _ in range(0, length):
        new_list.append(random.choice(people))

    return new_list


def _generate_id_and_name() -> Tuple[str, str]:
    """ Return a tuple containing the following strings:
            1. A 6-digit id composed of uppercase ASCII letters and numbers for a _Person object.
            2. The initials for the name attribute of a _Person object.
    """
    id_chars = string.ascii_uppercase + string.digits
    name_chars = string.ascii_uppercase
    return (''.join(random.choice(id_chars) for _ in range(6)), random.choice(name_chars) + '. ' +
            random.choice(name_chars))


def get_random_weight(level: str) -> float:
    """ Return a float value to represent the weight of an edge between two _Person objects
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
