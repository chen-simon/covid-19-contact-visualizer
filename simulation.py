"""CSC111 Project: COVID-19 Contact Visualizer

Module Description
==================
Simulation Module
This module contains the dataclasses and their methods needed to create the simulation.

Copyright and Usage Information
===============================
This file is Copyright (c) 2021 Simon Chen, Patricia Ding, Salman Husainie, Makayla Duffus
"""
from typing import Optional
import random
import networkx as nx
import plotly.graph_objects as go
import data_processing
import visualization as vis
from social_graph import Graph


class Simulation:
    """A simulation of the spread of COVID-19 over time.

    Instance Attributes:
        - _graph: The graph this simulation is representing.
        - _frames: A list of Plotly graph object frames (each frame represents one week in
        simulation time).
        - _init_infected: The set of initially infected people.
        - _num_infected: The number of people who are initially infected.
    """
    _graph: Graph
    _frames: list[go.Frame]
    _init_infected: set[str]
    _num_infected: int

    def __init__(self, conditions: tuple[int, str, int, str],
                 graph: Optional[Graph] = None) -> None:
        """Initialize the values in this simulation.

        - conditions[0] is the number of people in this simulation
        - conditions[1] is the level of contact between people (edge weights)
        - conditions[2] is the number of initially infected people
        - conditions[3] is whether the graph is connected

        Preconditions:
            - 10 < conditions[0] <= 60
            - conditions[1] == 'high' or conditions[1] == 'medium' or conditions[1] == 'low'
            - 1 <= conditions[2] <= conditions[0]
            - conditions[3] == 'yes' or conditions[3] == 'no'
        """
        # for when a dataset is given
        if graph is not None:
            self._graph = graph

        # for when a graph needs to be generated
        elif conditions[3] == 'yes':
            self._graph = data_processing.generate_connected_graph(conditions[0], conditions[1])
        else:
            self._graph = data_processing.generate_disconnected_graph(conditions[0], conditions[1])

        # Setting the initially infected people
        self._num_infected = conditions[2]
        self._init_infected = set()

        # choosing random people to be the initially infected
        people_copy = set(self._graph.get_people())
        for _ in range(0, self._num_infected):
            self._init_infected.add(people_copy.pop())

        self._frames = []

    def run(self, ticks: int, with_degrees: bool = False) -> None:
        """Run the simulation for a given amount of ticks.
        """
        self._graph.set_infected(self._init_infected)

        # Creates simulation buffer and infected sets.
        infected = self._init_infected
        buffer_infected = set()

        if with_degrees:
            self._graph.recalculate_degrees()
            graph_nx = self._graph.to_nx_with_degree_colour()
        else:
            graph_nx = self._graph.to_nx_with_simulation_colour()

        # Establishes a shared position of all nodes when visualizing
        pos = getattr(nx, 'spring_layout')(graph_nx)

        # Renders the initial state frame
        sliders_dict = {"steps": []}
        self._frames.append(vis.render_simulation_frame(self._graph, pos, 0, with_degrees))

        # Loops for the amount of ticks, rendering each frame as it goes
        for i in range(ticks):
            # Updates the infected and
            infected = infected.union(buffer_infected)
            self._graph.set_infected(buffer_infected)
            buffer_infected = set()
            # checking every connection where one node is infected
            for person in infected:
                for neighbour in self._graph.get_neighbours(person):
                    result = determine_infected(self._graph.get_weight(person,
                                                                       neighbour.identifier))
                    if result:
                        buffer_infected.add(neighbour.identifier)

            if with_degrees:
                self._graph.recalculate_degrees()

            # Renders the frame for the end of tick.
            self._frames.append(vis.render_simulation_frame(self._graph, pos, i, with_degrees))
            vis.update_slider(sliders_dict, i)

        vis.render_simulation_full(self._frames, sliders_dict, len(graph_nx.nodes),
                                   len(self._init_infected))


def determine_infected(edge_weight: float) -> bool:
    """Determine if a node becomes infected using the edge weight between an infected node and a
    non-infected node

    >>> result = determine_infected(1)
    >>> result
    True
    >>> result = determine_infected(0.4)
    >>> result or not result
    True
    """
    return random.choices([True, False], weights=(edge_weight, 1 - edge_weight))[0]


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    import python_ta.contracts
    python_ta.contracts.check_all_contracts()

    import python_ta
    python_ta.check_all(config={
        'extra-imports': ['networkx', 'functools', 'math'],  # the names (strs) of imported modules
        'max-line-length': 100,
        'disable': ['E1136']
    })
