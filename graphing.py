import random
from typing import List, Tuple
import plotly
from plotly.graph_objs import Figure
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def plot_datasets(year: List[int], red_list_y: List[float],
                  other_datasets: List[Tuple[str, List[float]]],
                  a: float, b: float, x_max: float, x_min: float,
                  new_point_x: list, new_point_y: list, sigma: float) -> None:
    """Create a plotly graph of the all the datasets apart from red list
        This function takes in a dictionary with one to one pairings only.
        The dictionaries are created by using the functions in formatting.py
    """
    # Create a blank figure
    fig = make_subplots(rows=1, cols=2)

    # Add the given data
    make_graph1(fig, year, red_list_y, other_datasets, new_point_y, sigma)
    if len(other_datasets) == 1:
        make_graph2(fig, other_datasets[0][1], red_list_y, x_min, x_max, a, b, new_point_x, new_point_y, sigma)

    # Naming of axis and title

    fig.update_layout(title='Prediction',
                      xaxis_title='Year',
                      yaxis_title='Number of Threatened Species')

    # Display the figure in a web browser.
    fig.show()


def make_graph1(fig: Figure, year: list, red_list_y: list,
                other_datasets: List[Tuple[str, List[float]]], new_point_y: list,
                sigma: float) -> None:
    """ Produces a graph where x axis is the years and y axis is the actual values of the datasets.
    """
    fig.add_trace(go.Scatter(x=year, y=red_list_y,
                             mode='lines+markers', name='Threatened Species'), row=1, col=1)

    for dataset in other_datasets:
        fig.add_trace(go.Scatter(x=year, y=dataset[1],
                      mode='lines+markers', name=dataset[0]), row=1, col=1)

    fig.add_trace(go.Scatter(x=[2020], y=new_point_y, mode='markers', name='Prediction Interval',
                             error_y=dict(type='constant', value=sigma)), row=1, col=1)



def make_graph2(fig: Figure, graph2_x_coords: list, y_coords: list, x_min: float, x_max: float,
                a: float, b: float, new_point_x: list, new_point_y: list, sigma: float, r_squared: float):
    """ Produces a graph where x axis is the selected dataset and the y axis is the red list data.
    """
    fig.add_trace(go.Scatter(x=graph2_x_coords, y=y_coords, mode='markers', name='Data'), row=1, col=2)

    # Add the regression line
    fig.add_trace(go.Scatter(x=[x_min, x_max], y=[a + b * x_min,
                                                  a + b * x_max],
                             mode='lines', name='Regression line'), row=1, col=2)

    fig.add_trace(go.Scatter(x=new_point_x, y=new_point_y, mode='markers', name='Prediction Interval',
                             error_y=dict(type='constant', value=sigma)), row=1, col=2)

