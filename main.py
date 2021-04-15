"""CSC111 Project: COVID-19 Contact Visualizer

Module Description
==================
Main Module
This module contains the runner functions that create the COVID-19 Contact Tracing simulation.

Copyright and Usage Information
===============================
This file is Copyright (c) 2021 Simon Chen, Patricia Ding, Salman Husainie, Makayla Duffus
"""
from typing import Tuple
import visualization
import data_processing
import random
from simulation import Simulation
import menu


def open_gui_menu() -> None:
    """ Opens a Pygame-based GUI Menu that allows easy selection of the functionality of the
    projects features.
    """
    menu.run_interface()


def run_degrees_example() -> None:
    """ Run the example degrees risk visualization using a graph of people loaded from
    a csv file.
    """
    graph = data_processing.load_graph_csv('data/persons.csv', 'data/connections.csv')
    init_infected = {'WJ5751'}

    visualization.render_degrees_apart(graph, init_infected)


def run_degrees_example_generated() -> None:
    """ Run the example degrees risk visualization using a randomly generated graph of
    50 people.
    """
    graph = data_processing.generate_connected_graph(50)
    init_infected = {random.choice(list(graph.get_people()))}

    visualization.render_degrees_apart(graph, init_infected)


def run_simulation_example(sim_conditions: Tuple[int, str, int, str]) -> None:
    """ Run the example simulation using the sample graph of people.
    """
    sim = Simulation(sim_conditions)
    sim.run(10)


def run_simulation_example_with_degrees_preview(sim_conditions: Tuple[int, str, int, str]) -> None:
    """ Run the example simulation using the sample graph of people, and the degree preview.
    """
    sim = Simulation(sim_conditions)
    sim.run(21, with_degrees=True)


if __name__ == '__main__':
    open_gui_menu()
