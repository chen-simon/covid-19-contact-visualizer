"""CSC111 Project: COVID-19 Contact Visualizer

Module Description
==================
Main Module
This module runs the entire COVID-19 Contact Visualizer. # TODO: Make this better after done.

Copyright and Usage Information
===============================
This file is Copyright (c) 2021 Simon Chen, Patricia Ding, Salman Husainie, Makayla Duffus
"""
from networkx import nx
from plotly.graph_objs import Scatter, Figure
import visualization
import data_processing

def run_degrees_example() -> None:
    """ Run the example degrees risk visualization using the sample graph of people.
    """
    graph = data_processing.load_graph_csv('data/persons.csv', 'data/connections.csv')
    init_infected = {'WJ5751'}

    visualization.render_degrees_apart(graph, init_infected)
