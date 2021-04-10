""" COVID-19 Contact Visualizer

Data Processing Module
This module contains the functions that extract, process, and generate data for the
COVID-19 contact visualizer.

This file is Copyright (c) 2021 Simon Chen, Patricia Ding, Salman Husainie, Makayla Duffus
"""
from __future__ import annotations
import csv
import random
import string
from typing import Tuple
from graph import Graph


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


def create_test_graph(n: int) -> Graph:
    """ Return a connected Graph containing n _Person objects.

    Preconditions:
        - n >= 20
    """
    graph = Graph()

    # Add vertices to graph
    for i in range(0, n):
        id, name = generate_id_and_name()
        graph.add_vertex(identifier=str(i), name=name, age=random.randint(18, 55),
                         severity_level=random.uniform(0, 1))

        k = random.randint(0, n // 3)
        for j in range(0, k):
            graph.add_edge(str(k), str(j), random.uniform(0, 1))

    return graph


def generate_id_and_name() -> Tuple[str, str]:
    """ Return a tuple containing the following strings:
        1. A 6-digit id composed of uppercase ASCII letters and numbers for a _Person object.
        2. The initials for a _Person object.
    """
    id_chars = string.ascii_uppercase + string.digits
    name_chars = string.ascii_uppercase
    return (''.join(random.choice(id_chars) for _ in range(6)), random.choice(name_chars) + '. ' +
            random.choice(name_chars))


def load_graph_json(names_file: str, contact_file: str) -> Graph:
    """ Return a Graph from the corresponding names file and contacts file which are in .json
    format.
    """
    # TODO: Implement this method if we're feeling spicy
