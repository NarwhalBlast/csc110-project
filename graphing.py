"""
Graphing Module

This module contains the functions that are needed to plot the data. The data is plotted with plotly.

This file is Copyright (c) 2020 Patricia Ding, Makayla Duffus, Simon Chen.
"""
from typing import List, Tuple
from plotly.graph_objs import Figure
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def plot_datasets(year: List[int], red_list_y: List[float],
                  other_datasets: List[Tuple[str, List[float], float]],
                  a: float, b: float, x_max: float, x_min: float,
                  new_point_x: list, new_point_y: list, sigma: float, r_squared: float) -> None:
    """ Plot the data that has been computed. If a simple linear regression was performed, two graphs will be created.
    The left graph (graph1) will be the values of the datasets over time. The right graph (graph2) will be the linear
    regression of the independent variable and the red list data.  If a multiple linear regression was performed, one
    graph (graph1) will be created, that will represent the datasets over time.
    """
    # Create a blank figure and two graphs
    if len(other_datasets) == 1:
        fig = make_subplots(rows=1, cols=2,
                            subplot_titles=("Change in Red List and " + str(other_datasets[0][0]) + " Over Time",
                                            str(other_datasets[0][0]) + " vs. Number of Threatened Species"))
        fig.update_layout(title='Predicting Future Value - R squared = ' + str(r_squared),
                          xaxis_title='Year',
                          yaxis_title='Data')

    # create a blank figure with one graph
    else:
        fig = make_subplots(rows=1, cols=1)
        fig.update_layout(title='Predicting Future Value',
                          xaxis_title='Year',
                          yaxis_title='Data')

    # Add data to graph1
    make_graph1(fig, year, red_list_y, other_datasets, new_point_y, sigma)

    # Add data to graph2
    if len(other_datasets) == 1:
        make_graph2(fig, other_datasets[0][1], red_list_y,
                    x_min, x_max, a, b, new_point_x, new_point_y, sigma, str(other_datasets[0][0]))

    # Display the figure in a web browser.
    fig.show()


def make_graph1(fig: Figure, year: list, red_list_y: list,
                other_datasets: List[Tuple[str, List[float], float]], new_point_y: list,
                sigma: float) -> None:
    """ Produces a graph where x axis is the years and y axis is the actual values of the datasets.
    """
    # red list data
    fig.add_trace(go.Scatter(x=year, y=red_list_y,
                             mode='lines+markers', name='Threatened Species'), row=1, col=1)

    # plot the other datasets
    for dataset in other_datasets:
        fig.add_trace(go.Scatter(x=year, y=dataset[1],
                      mode='lines+markers', name=dataset[0]), row=1, col=1)
        fig.add_trace(go.Scatter(x=[2020], y=[dataset[2]], mode='markers', name='Future ' + dataset[0]), row=1, col=1)

    # plot predicted value
    fig.add_trace(go.Scatter(x=[2020], y=new_point_y, mode='markers', name='Predicted Number of Threatened Species',
                             error_y=dict(type='constant', value=sigma)), row=1, col=1)


def make_graph2(fig: Figure, graph2_x_coords: list, y_coords: list, x_min: float, x_max: float,
                a: float, b: float, new_point_x: list, new_point_y: list, sigma: float, label: str):
    """ Produces a graph where x axis is the selected dataset and the y axis is the red list data.
    """
    # Add data points
    fig.add_trace(go.Scatter(x=graph2_x_coords, y=y_coords, mode='markers', name='Data'), row=1, col=2)

    # Add the regression line
    fig.add_trace(go.Scatter(x=[x_min, x_max], y=[a + b * x_min,
                                                  a + b * x_max],
                             mode='lines', name='Regression line'), row=1, col=2)

    # add predicted value
    fig.add_trace(go.Scatter(x=new_point_x, y=new_point_y, mode='markers', name='Prediction Interval',
                             error_y=dict(type='constant', value=sigma)), row=1, col=2)

    fig.update_xaxes(title_text=label, row=1, col=2)
    fig.update_yaxes(title_text="Number of Threatened Species", row=1, col=2)
