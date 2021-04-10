import networkx as nx
from plotly.graph_objs import Scatter, Figure
from graph import Graph

INFECTED_COLOUR = 'rgb(255, 0, 0)'

# Degrees visualization
def render_degrees_apart(graph: Graph, init_infected: set[str]) -> None:
    """ Render the degrees visualization given a graph, and the initial set of infected people.

    Preconditions:
        - all(not person.infected for person in graph._people.values())
    """
    # Degree calculation
    graph.set_infected(init_infected)
    graph.recalculate_degrees()

    # Display
    graph_nx = graph.to_networkx(max_vertices)

    pos = getattr(nx, layout)(graph_nx)

    x_values = [pos[k][0] for k in graph_nx.nodes]
    y_values = [pos[k][1] for k in graph_nx.nodes]
    labels = list(graph_nx.nodes)
    kinds = [graph_nx.nodes[k]['kind'] for k in graph_nx.nodes]

    colours = [BOOK_COLOUR if kind == 'book' else USER_COLOUR for kind in kinds]

    x_edges = []
    y_edges = []
    for edge in graph_nx.edges:
        x_edges += [pos[edge[0]][0], pos[edge[1]][0], None]
        y_edges += [pos[edge[0]][1], pos[edge[1]][1], None]

    trace3 = Scatter(x=x_edges,
                     y=y_edges,
                     mode='lines',
                     name='edges',
                     line=dict(color=LINE_COLOUR, width=1),
                     hoverinfo='none',
                     )
    trace4 = Scatter(x=x_values,
                     y=y_values,
                     mode='markers',
                     name='nodes',
                     marker=dict(symbol='circle-dot',
                                 size=5,
                                 color=colours,
                                 line=dict(color=VERTEX_BORDER_COLOUR, width=0.5)
                                 ),
                     text=labels,
                     hovertemplate='%{text}',
                     hoverlabel={'namelength': 0}
                     )

    data1 = [trace3, trace4]
    fig = Figure(data=data1)
    fig.update_layout({'showlegend': False})
    fig.update_xaxes(showgrid=False, zeroline=False, visible=False)
    fig.update_yaxes(showgrid=False, zeroline=False, visible=False)

def rgb_to_str(rgb: )

