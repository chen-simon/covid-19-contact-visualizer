"""CSC111 Project: COVID-19 Contact Visualizer

Module Description
==================
Visualization Module
This module contains the functions used to create the COVID-19 contact visualization.

Copyright and Usage Information
===============================
This file is Copyright (c) 2021 Simon Chen, Patricia Ding, Salman Husainie, Makayla Duffus
"""
import networkx as nx
from dataclasses import Graph
from plotly.graph_objs import Scatter, Figure
import data_processing
import plotly.graph_objects as go


# Degrees visualization
def render_degrees_apart(graph: Graph, init_infected: set[str]) -> None:
    """ Render the degrees visualization given a graph, and the initial set of infected people by
    ID.

    Preconditions:
        - all(not person.infected for person in graph._people.values())
    """
    # Degree calculation
    graph.set_infected(init_infected)
    graph.recalculate_degrees()

    # Converts to nx.Graph
    graph_nx = graph.to_nx_with_degree_colour()

    colours = [graph_nx.nodes[node]['colour'] for node in graph_nx.nodes]

    # i think this generates the positions randomly for each node according to the given layout
    # the layout is algorithm used by networkx
    pos = getattr(nx, 'spring_layout')(graph_nx)

    # put positions of nodes into lists
    x_values = [pos[k][0] for k in graph_nx.nodes]
    y_values = [pos[k][1] for k in graph_nx.nodes]
    labels = list(graph_nx.nodes)

    # put positions of edges into lists
    x_edges = []
    y_edges = []
    for edge in graph_nx.edges:
        x_edges += [pos[edge[0]][0], pos[edge[1]][0], None]
        y_edges += [pos[edge[0]][1], pos[edge[1]][1], None]

    # create the edges in plotly
    trace3 = Scatter(x=x_edges,
                     y=y_edges,
                     mode='lines',
                     name='edges',
                     line=dict(width=2,
                               color='rgb(0, 0, 0)'),
                     hoverinfo='none',
                     )

    # create the nodes in plotly
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

    # add these nodes and edges to the figure and show the graph
    data1 = [trace3, trace4]

    fig = Figure(data=data1)
    fig.update_layout({'showlegend': False})
    fig.update_xaxes(showgrid=False, zeroline=False, visible=False)
    fig.update_yaxes(showgrid=False, zeroline=False, visible=False)

    fig.show()


def visualize_dataset_animate() -> None:
    """Testing out plotly animations using frames"""
    # load the graph
    graph = data_processing.generate_connected_graph(20)
    graph_nx = graph.to_nx()

    # i think this generates the positions randomly for each node according to the given layout
    # the layout is algorithm used by networkx
    pos = getattr(nx, 'spring_layout')(graph_nx)

    # put positions of nodes into lists
    x_values = [pos[k][0] for k in graph_nx.nodes]
    y_values = [pos[k][1] for k in graph_nx.nodes]
    labels = list(graph_nx.nodes)

    # set colours of nodes
    colours1 = ['rgb(255, 0, 0)' for _ in range(len(graph_nx.nodes))]
    colours2 = ['rgb(0, 255, 0)' for _ in range(len(graph_nx.nodes))]
    colours3 = ['rgb(0, 0, 255)' for _ in range(len(graph_nx.nodes))]

    # put positions of edges into lists
    x_edges = []
    y_edges = []
    for edge in graph_nx.edges:
        x_edges += [pos[edge[0]][0], pos[edge[1]][0], None]
        y_edges += [pos[edge[0]][1], pos[edge[1]][1], None]

    # create the edges in plotly
    trace3 = Scatter(x=x_edges,
                     y=y_edges,
                     mode='lines',
                     name='edges',
                     line=dict(width=2,
                               color='rgb(0, 0, 0)'),
                     hoverinfo='none',
                     )

    # create the nodes in plotly
    trace4 = Scatter(x=x_values,
                     y=y_values,
                     mode='markers',
                     name='nodes',
                     marker=dict(symbol='circle-dot',
                                 size=50,
                                 color=colours1,
                                 line=dict(width=0.5)
                                 ),
                     text=labels,
                     hovertemplate='%{text}',
                     hoverlabel={'namelength': 0}
                     )
    trace5 = Scatter(x=x_values,
                     y=y_values,
                     mode='markers',
                     name='nodes',
                     marker=dict(symbol='circle-dot',
                                 size=50,
                                 color=colours2,
                                 line=dict(width=0.5)
                                 ),
                     text=labels,
                     hovertemplate='%{text}',
                     hoverlabel={'namelength': 0}
                     )

    trace6 = Scatter(x=x_values,
                     y=y_values,
                     mode='markers',
                     name='nodes',
                     marker=dict(symbol='circle-dot',
                                 size=50,
                                 color=colours3,
                                 line=dict(width=0.5)
                                 ),
                     text=labels,
                     hovertemplate='%{text}',
                     hoverlabel={'namelength': 0}
                     )

    # add these nodes and edges to the figure and show the graph
    data1 = [trace3, trace4]
    data2 = [trace3, trace5]
    data3 = [trace3, trace6]
    fig = Figure(data=data1,
                 layout=go.Layout(
                     xaxis=dict(range=[0, 5], autorange=False),
                     yaxis=dict(range=[0, 5], autorange=False),
                     title="Start Title",
                     updatemenus=[dict(
                         type="buttons",
                         buttons=[dict(label="Play",
                                       method="animate",
                                       args=[None])])]
                 ),
                 frames=[go.Frame(data=data1),
                         go.Frame(data=data2),
                         go.Frame(data=data3)]
                 )
    fig.update_layout({'showlegend': False})
    fig.update_xaxes(showgrid=False, zeroline=False, visible=False)
    fig.update_yaxes(showgrid=False, zeroline=False, visible=False)

    fig.show()


def render_simulation_frame(graph: Graph, pos: list, num: int = 0,
                            with_degrees: bool = False) -> go.Frame:
    """ Return a plotly graph object Frame given a graph and the positions of each person on the
    rendered graph.
    """
    if with_degrees:
        graph_nx = graph.to_nx_with_degree_colour()
    else:
        graph_nx = graph.to_nx_with_simulation_colour()

    # create frame
    colours = [graph_nx.nodes[node]['colour'] for node in graph_nx.nodes]
    x_values = [pos[k][0] for k in graph_nx.nodes]
    y_values = [pos[k][1] for k in graph_nx.nodes]
    labels = list(graph_nx.nodes)

    # put positions of edges into lists
    x_edges = []
    y_edges = []
    for edge in graph_nx.edges:
        x_edges += [pos[edge[0]][0], pos[edge[1]][0], None]
        y_edges += [pos[edge[0]][1], pos[edge[1]][1], None]

    # create the edges in plotly
    trace3 = Scatter(x=x_edges,
                     y=y_edges,
                     mode='lines',
                     name='edges',
                     line=dict(width=2,
                               color='rgb(0, 0, 0)'),
                     hoverinfo='none',
                     )

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

    return go.Frame(data=[trace3, trace4], name=num)


def update_slider(sliders_dict: dict, num: int = 0) -> None:
    """Updates slider_dict for the layout of plotly figure"""

    slider_step = {"args": [[num], {"frame": {"duration": 700, "redraw": False},
                                    "mode": "immediate",
                                    "transition": {"duration": 100}}], "label": 'Week ' + str(num),
                   "method": "animate"}
    sliders_dict["steps"].append(slider_step)


def render_simulation_full(frames: list[go.Frame], sliders_dict: dict) -> None:
    fig = Figure(data=frames[0].data,
                 layout=go.Layout(
                     xaxis=dict(range=[0, 5], autorange=False),
                     yaxis=dict(range=[0, 5], autorange=False),
                     title="Start Title",
                     updatemenus=[dict(
                         type="buttons",
                         buttons=[dict(label="Play",
                                       method="animate",
                                       args=[None, {"frame": {"duration": 700, "redraw": False},
                                                    "fromcurrent": True}]),

                                  dict(label="Pause",
                                       method="animate",
                                       args=[[None], {"frame": {"duration": 0, "redraw": False},
                                                      "mode": "immediate",
                                                    "transition": {"duration": 0}}])
                                  ])],
                     sliders=[sliders_dict]),
                 frames=frames
                 )

    fig.update_layout({'showlegend': False})
    fig.update_xaxes(showgrid=False, zeroline=False, visible=False)
    fig.update_yaxes(showgrid=False, zeroline=False, visible=False)

    fig.show()
