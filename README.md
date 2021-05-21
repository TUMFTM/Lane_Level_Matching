# Lane_Level_Matching

# Determine a Map Matching Algorithm with Lane Level Precision

Contact: [Frederic Brenner](mailto:frederic.brenner@tum.de)

Contact: [Julian Kreibich](mailto:julian.kreibich@tum.de)

## Algorithm usage
The python environment is saved as conda environment "environment.yml" in the folder "python_environment".
Alternatively the necessary libraries are listed in the file "Libraries.txt" in the same folder.

The Code is divided into chapters which are run by entering "y" or skipped with "n".

Data source for map: Bayerische Straßenbauverwaltung - BAYSIS (https://www.baysis.bayern.de)
Licence for BAYSIS map: Creative Commons Namensnennung 4.0 Lizenz


### Import dataset (is automatically implemented in main_multi.py)
At first the measurement dataset must be defined

The dataset is loaded with the import_to_main.py script into the project

This script also ensures the correct format

### Run main script 
The main script (main.py) runs the complete algorithm for map matching and lane matching

It can be chosen for every run if the digital map from baysis shall be updated

After the matching the results are analyzed if there is ground truth data available

### See results and plots
The important results (progress, street matching, accuracy) are shown in the command window

The algorithm result (matched roads and lanes) is saved as a pandas Dataframe pickled in pathTaken.pkl

Further information plots like the street map, matching etc. can be taken from the folder data/map_plots

Further the street usage is saved in digital_map/street_usage.txt


## Overview
This work is divided into the modules data configuration, main code and merged utils

For multiple measurements the main_multi.py script can be used but is has the same algorithm as main.py implemented

## Data and configuration

### Config module
This module contains all file paths and configuration parameters

### Data module
This module contains all measurement datasets, folder system is saved in config module

### Import_to_main
This module is used to import the measurements from 2020 into the main algorithm

Needs to be run before main for every new dataset


## Code Modules for main script

### BAYSIS module
This module connects to BAYSIS API and saves the response as xml file (skipped in this extract)

### To_pandas module
This module converts the BAYSIS xml files into pandas dataframes (skipped in this extract)

### Digital_map module
This module creates a digital map from the baysis xml files (skipped in this extract, 
the result can be seen in </data/map_plots/plot_baysis_roads.html>)

### Markov_model module
This module contains the map matching from coordinates to street

It was originally implemented as Hidden Markov Model but is now a linear model

### Lane module
This module contains the map matching from GNSS and ACC data to lane probability

It also contains the sensor fusion (combine_prob)

### Ground_truth module
This module contains the algorithm for automatic accuracy calculation

## Further modules

### Utils module
This module contains several small scripts used in the main algorithm

### Filter module
This module contains different filters for data preprocessing

### Sine filter module
This module contains the custom sine curve used for lane change detection on acc signal.
The custom curve is shown by running the script show_custom_sine_filter.py.
This is the optimum curve based on the collected ground truth data sets.



## The following modules are not included in this extract:

### Optimization module
This module is used for parameter-tuning of GNSS and ACC parameters

### Thomas module
This module prepares the dataset from another project to be run in the main algorithm

### Tests module
This module contains scripts used for testing specific dataset values

### Evaluation module
This module contains scripts used for evaluating the measurement data for example total distance traveled
