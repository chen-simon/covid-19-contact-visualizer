"""CSC111 Project: COVID-19 Contact Visualizer

Module Description
==================
Simulation Module
This module contains ...

Copyright and Usage Information
===============================
This file is Copyright (c) 2021 Simon Chen, Patricia Ding, Salman Husainie, Makayla Duffus
"""
import random
import data_processing
import visualization


def start_simulation() ->...:
    graph = data_processing.generate_connected_graph_no_csv(50)
    init_infected = {random.choice(list(graph.get_people()))}
    graph.set_infected(init_infected)

    for graph.get_people()
