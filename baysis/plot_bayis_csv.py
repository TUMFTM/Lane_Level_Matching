####################################################
## This script plots the data from  excel sheet map_data_final
####################################################
## Author: Frederic Brenner
## Email: frederic.brenner@tum.de
####################################################
## Date: 07.2020
####################################################

import pandas as pd
# import numpy as np
import mplleaflet
import matplotlib.pyplot as plt
import config.paths as paths


def plot_baysis_csv(map_data, new_format, output_sorted_map):
    """
    This function plots the result of street concatenation from connect_map.py

    :param map_data: pandas dataframe with concatenated street data
    :param new_format:  bool flag: german or english dataframe columns
    :return: road sorted dataframe if output_sorted_map==True
    """

    if new_format:
        fromNode = 'fromNode'
        toNode = 'toNode'
    else:
        fromNode = 'Von-NK'
        toNode = 'Nach-NK'

    # Exclude first row from csv import
    if 'Unnamed: 0' in map_data.columns:
        map_data = map_data.drop(columns='Unnamed: 0')

    multi_col = ['latitude', 'longitude', 'cumulativeDistance', 'orientation']
    #'sameDirection', 'againstDirection', 'lanesTotal', 'fromWidth_cm', 'toWidth_cm', 'offsetSameDir', 'offsetAgainstDir']

    road_group = map_data.groupby([fromNode, toNode, 'fromStationWidth', 'toStationWidth'])
    road = pd.DataFrame(columns=map_data.columns)
    idx = 0
    for name, group in road_group:
        index_group = group.index[0]
        for col in road.columns:

            # Multiple values in row
            if col in multi_col:
                road.loc[idx, col] = group.loc[:, col].values

            # Single value
            else:
                road.loc[idx, col] = group.loc[index_group, col]

        # next row
        idx += 1

    #
    ## mplleaflet has a bug in this version: AttributeError: 'XAxis' object has no attribute '_gridOnMajor'
    ## replace in lib\site-packages\mplleaflet\mplexporter\utils.py
    #
    # def get_grid_style(axis):
    #     gridlines = axis.get_gridlines()
    #     if axis._gridOnMajor and len(gridlines) > 0:
    #         color = color_to_hex(gridlines[0].get_color())
    #         alpha = gridlines[0].get_alpha()
    #         dasharray = get_dasharray(gridlines[0])
    #         return dict(gridOn=True,
    #                     color=color,
    #                     dasharray=dasharray,
    #                     alpha=alpha)
    # else:
    #     return {"gridOn": False}
    #
    ## with
    # def get_grid_style(axis):
    #     return {"gridOn": False}

    fig = plt.figure()
    for idx in road.index:
        plt.plot(road.loc[idx, 'longitude'], road.loc[idx, 'latitude'], linewidth=5)
    mplleaflet.show(fig=fig, path=paths.map_plot_path + 'plot_baysis_roads.html')

    if output_sorted_map:
        return road
