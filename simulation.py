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
import dataclasses
import visualization as vis
from dataclasses import Graph
import plotly.graph_objects as go
from typing import Optional


class Simulation:
    """ A simulation of the graph over time.
    """
    _graph: dataclasses.Graph
    _frames: list[go.Frame]
    _init_infected: set[str]

    def __init__(self, graph: Optional[Graph] = None):
        if graph is not None:
            self._graph = graph
        else:
            self._graph = data_processing.generate_connected_graph(50)

        self._init_infected = {random.choice(list(self._graph.get_people()))}
        self._frames = []

    def run(self, ticks: int) -> None:
        """Run the simulation for a given amount of ticks.
        """
        # Establish
        graph_nx = self._graph.to_nx()
        pos = getattr(nx, 'spring_layout')(graph_nx)
        self._graph.set_infected(self._init_infected)

        infected = self._init_infected
        buffer_infected = set()

        # Renders the initial state frame
        sliders_dict = {"steps": []}
        self._frames.append(vis.render_simulation_frame(self._graph, pos))

        # Loops for the amount of ticks, rendering each frame as it goes
        for i in range(ticks):
            # Updates the infected and
            infected = infected.union(buffer_infected)
            self._graph.set_infected(buffer_infected)
            buffer_infected = set()
            # checking every connection where one node is infected
            for person in infected:
                for neighbour in self._graph.get_neighbours(person):
                    result = determine_infected(self._graph.get_weight(person, neighbour))

                    if result:
                        buffer_infected.add(neighbour.identifier)

            # Renders the frame for the end of tick.
            self._frames.append(vis.render_simulation_frame(self._graph, pos, i))
            vis.update_slider(sliders_dict, i)

        vis.render_simulation_full(self._frames, sliders_dict)


def determine_infected(edge_weight: float) -> bool:
    """Determine if neighbour becomes infected and set the person's infected bool accordingly."""
    return bool(random.choices([True, False], cum_weights=(edge_weight, 1-edge_weight)))
