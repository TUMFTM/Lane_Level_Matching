# Lane_Level_Matching
The python algorithm can be found under the "Releases" tab


# Determine a Map Matching Algorithm with Lane Level Precision

Contact: [Frederic Brenner](mailto:frederic.brenner@tum.de)

Contact: [Julian Kreibich](mailto:julian.kreibich@tum.de)

## Algorithm usage
The python environment is saved as conda environment "environment.yml" in the folder "python_environment"

Alternatively the necessary libraries are listed in the file "Libraries.txt" in the same folder

The main algorithm is divided into chapters which can be run separately

Data source for map: Bayerische Straßenbauverwaltung - BAYSIS (https://www.baysis.bayern.de)

Licence for BAYSIS map: Creative Commons Namensnennung 4.0 Lizenz


### 1. Import dataset
At first the measurement dataset must be defined

The dataset is loaded with the import_to_main.py script into the project

This script also ensures the correct format

### 2. Run main script 
The main script (main.py) runs the complete modular algorithm for map matching and lane matching

The modules can be run independently, e.g. it can be chosen if the digital map shall be updated

After the lane matching the results are analyzed if there is ground truth data available

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

The workspace path is determined automatically, change it to the project folder if there are any problems

### Data module
This module contains all measurement datasets, folder hierarchy must be the same as in config module

### Import_to_main
This module is used to import the measurements (from data loggers) into the main algorithm

Needs to be run before main for every new dataset in this version


## Code Modules for main script

### BAYSIS module
This module connects to BAYSIS API and saves the response as xml file
(skipped in this extract due to limitation on bavarian streets)

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

It also contains the sensor fusion (combine_prob.py)

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
This is the optimum curve based on the collected ground truth data sets in this project.



## The following modules are not included in this extract
Functions regarding to the download and conversion of the BAYSIS street dataset
and the script for analyzing multiple datasets (import + main function in a loop)

If you want to gain insight in these modules, feel free to contact the contributors (listed at the top)

### Optimization module
This module is used for parameter-tuning of GNSS and ACC parameters

### Tests module
This module contains scripts used for testing the algorithm and specific dataset values

### Evaluation module
This module contains scripts used for evaluating the measurement data for example total distance traveled
