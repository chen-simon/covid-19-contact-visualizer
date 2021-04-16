"""CSC111 Project: COVID-19 Contact Visualizer

Module Description
==================
Main Module
This module contains the runner functions that create the simulation.

Copyright and Usage Information
===============================
This file is Copyright (c) 2021 Simon Chen, Patricia Ding, Salman Husainie, Makayla Duffus
"""
import visualization
import data_processing
import random
from simulation import Simulation
import menu


###########################################################
# csv runners
###########################################################
def run_degrees_graph_csv(persons_dataset: str, connections_dataset: str) -> None:
    """Run the example degrees risk visualization using the graph of people loaded from
    a csv file. Example datasets can be found in 'data/persons.csv' and 'data/connections.csv'
    """
    graph = data_processing.load_graph_csv(persons_dataset, connections_dataset)
    init_infected = {random.choice(list(graph.get_people()))}

    visualization.render_degrees_apart(graph, init_infected)


def run_simulation_csv(persons_dataset: str, connections_dataset: str) -> None:
    """Run the simulation using a graph of people loaded from the csv files. The level of contact
    between people is automatically set to 'medium'. Example datasets can be found in
    'data/persons.csv' and 'data/connections.csv'

    Preconditions:
        - the number of rows in persons_dataset is greater than 1
    """
    graph = data_processing.load_graph_csv(persons_dataset, connections_dataset)

    # Update these conditions accordingly if sample datasets deviate from original
    conditions = (len(graph.get_people()),  # Number of people in graph
                  'medium',  # Contact level between people
                  1,  # Number of initially infected people
                  'no'  # Whether the graph is connected or not
                  )
    sim = Simulation(conditions, graph)
    sim.run(10, with_degrees=True)


###########################################################
# data generation runners
###########################################################
def open_gui_menu() -> None:
    """Opens a Pygame-based GUI Menu that allows for customization of the simulation
    """
    menu.run_interface()


def run_degrees_graph_generated(n: int = 50) -> None:
    """Run the example degrees risk visualization using a randomly generated graph of n people. One
    person is randomly chosen as the initially infected.

    Preconditions:
        - 10 < n <= 60
    """
    graph = data_processing.generate_connected_graph(n)
    init_infected = {random.choice(list(graph.get_people()))}
    visualization.render_degrees_apart(graph, init_infected)


def run_simulation_no_degrees_preview(
        sim_conditions: tuple[int, str, int, str] = (50, 'medium', 1, 'yes')) -> None:
    """Run the simulation with the given conditions. This simulation does not show the degrees
    of separation between nodes.

    Parameter Descriptions:
        - sim_conditions[0] is the number of people in this simulation
        - sim_conditions[1] is the level of contact between people (edge weights)
        - sim_conditions[2] is the number of initially infected people
        - sim_conditions[3] is whether the graph is connected

    Preconditions:
        - 10 < sim_conditions[0] <= 60
        - sim_conditions[1] == 'high' or sim_conditions[1] == 'medium' or sim_conditions[1] == 'low'
        - 1 <= sim_conditions[2] <= sim_conditions[0]
        - sim_conditions[3] == 'yes' or sim_conditions[3] == 'no'
    """
    sim = Simulation(sim_conditions)
    sim.run(21)


def run_simulation_with_degrees_preview(
        sim_conditions: tuple[int, str, int, str] = (50, 'medium', 1, 'yes')) -> None:
    """Run the simulation with the given conditions. This simulation previews the degrees
    of separation between nodes.

    Parameter Descriptions:
        - sim_conditions[0] is the number of people in this simulation
        - sim_conditions[1] is the level of contact between people (edge weights)
        - sim_conditions[2] is the number of initially infected people
        - sim_conditions[3] is whether the graph is connected

    Preconditions:
        - 10 < sim_conditions[0] <= 60
        - sim_conditions[1] == 'high' or sim_conditions[1] == 'medium' or sim_conditions[1] == 'low'
        - 1 <= sim_conditions[2] <= sim_conditions[0]
        - sim_conditions[3] == 'yes' or sim_conditions[3] == 'no'
    """
    sim = Simulation(sim_conditions)
    sim.run(21, with_degrees=True)


# Comment out this code-block when wanting to use other runner functions
if __name__ == '__main__':
    open_gui_menu()
