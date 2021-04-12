"""CSC111 Project: COVID-19 Contact Visualizer

Module Description
==================
Simulation Module
This module contains ... # TODO: Finish this description

Copyright and Usage Information
===============================
This file is Copyright (c) 2021 Simon Chen, Patricia Ding, Salman Husainie, Makayla Duffus
"""
import random

import networkx as nx

import data_processing
import visualization
from dataclasses import Graph
from plotly.graph_objs import Scatter, Figure


def start_simulation() -> None:
    """Run the beginning of the simulation"""

    # create a graph and choose infected person randomly
    graph = data_processing.generate_connected_graph_no_csv(50)
    graph_nx = graph.to_nx()
    pos = getattr(nx, 'spring_layout')(graph_nx)

    init_infected = random.choice(list(graph.get_people()))
    graph.set_infected({init_infected})

    normal_infected = {init_infected}
    buffer_infected = set()

    # time limit for loop - 2 weeks
    for _ in range(20):
        normal_infected = normal_infected.union(buffer_infected)
        graph.set_infected(buffer_infected)
        buffer_infected = set()
        # checking every connection where one node is infected
        for person in normal_infected:
            for neighbour in graph.get_neighbours(person):
                result = determine_infected(graph.get_weight(person, neighbour))

                if result:
                    buffer_infected.add(neighbour)

        graph_nx = graph.to_nx_with_simulation_colour()

        # create frame
        colours = [graph_nx.nodes[node]['colour'] for node in graph_nx.nodes]
        x_values = [pos[k][0] for k in graph_nx.nodes]
        y_values = [pos[k][1] for k in graph_nx.nodes]
        labels = list(graph_nx.nodes)
        trace4 = Scatter(x=x_values,
                         y=y_values,
                         mode='markers',
                         name='nodes',
                         marker=dict(symbol='circle-dot',
                                     size=50,
                                     color=colours,
                                     line=dict(width=0.5)
                                     ),
                         text=labels,
                         hovertemplate='%{text}',
                         hoverlabel={'namelength': 0}
                         )


def determine_infected(edge_weight: float) -> bool:
    """Determine if neighbour becomes infected and set the person's infected bool accordingly."""
    return bool(random.choices([True, False], cum_weights=(edge_weight, 1-edge_weight)))


