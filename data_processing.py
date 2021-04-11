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


def create_test_graph(n: int) -> Graph:
    """ Return a connected Graph containing n _Person objects.

    Preconditions:
        - n >= 5
    """
    graph = Graph()
    people = []     # An accumulator containing the id's of each _Person object added

    for _ in range(0, n):
        identity, name = _generate_id_and_name()
        people.append(identity)
        graph.add_vertex(identifier=str(identity), name=name, age=random.randint(18, 55),
                         severity_level=random.uniform(0, 1))

    times = random.randint(1, n // 2)  # Setting a boundary for maximum weighted edges for a vertex

    for _ in range(0, times):
        rand_list = _random_list(people)
        combos = [(i, j) for i in rand_list for j in rand_list if i != j]

        for pair in combos:
            weight = random.uniform(0, 1)
            graph.add_edge(pair[0], pair[1], weight)

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
