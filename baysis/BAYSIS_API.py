#####################################################
## This script connects to BAYSIS API
## and saves response xml
#####################################################
## Author: Frederic Brenner
## frederic.brenner@tum.de
#####################################################
## Date: 05.2020
#####################################################


from http.client import HTTPSConnection
import time
import numpy as np

import os, sys, inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
from utils.ConvertCoordinates import convert_krueger_to_wgs84


def baysis_api(type_name, type_service, type_coordinate, max_features, bbox_flag, paths, config):

    ############
    # PARAMETERS
    ############

    url = 'www.baysis.bayern.de'
    # version = '2.0.0'

    # type_service = 'BAYSIS_Strassenbestand'      # Tagesaktuelle Daten Fahrbahnbreite, Streifen, usw.
    # type_name = 'STRBESTAND_WFS:Fahrstreifen'        # visuell
    # type_name = 'STRBESTAND_WFS:Fahrbahnbreiten'   # Fahrbahnbreite

    # Coordinate Types
    if type_coordinate == 'Krueger':
        srs_name = config.type_coordinate_baysis_code[1]             # Krueger

    elif type_coordinate == 'WGS84':
        srs_name = config.type_coordinate_baysis_code[2]             # WGS84 (GPS)

    elif type_coordinate == 'UTM':
        srs_name = config.type_coordinate_baysis_code[0]

    else:
        srs_name = None
        print('Warning: No coordinate specified, check output.')

    # Bounding Box
    if not bbox_flag:
        bbox = None
    else:   # use coords for Munich north / Garching
        # Define bounds in GPS format
        east_bound = np.asarray([11.50, 11.72])
        north_bound = np.asarray([48.14, 48.34])
        if type_coordinate == 'WGS84':
            # Transform in string for upload
            bbox = f'{east_bound[0]},{north_bound[0]},{east_bound[1]},{north_bound[1]}'
        elif type_coordinate == 'UTM':
            # UTM (lower left: N/E, upper right: N/E)
            df = convert_krueger_to_wgs84(east_bound, north_bound, from_epsg=4258, to_epsg=25832)
            df = df.astype('int')
            bbox = f'{df.at[0,"north"]},{df.at[0,"east"]},{df.at[1,"north"]},{df.at[1,"east"]}'
        elif type_coordinate == 'Krueger':
            df = convert_krueger_to_wgs84(east_bound, north_bound, from_epsg=4258, to_epsg=31468)
            df = df.astype('int')
            bbox = f'{df.at[0,"east"]},{df.at[0,"north"]},{df.at[1,"east"]},{df.at[1,"north"]}'
        else:
            print("Unrecognized coordinate type. Exit")
            exit()


    ######################## Request Data #########################

    # Determine combined request - WFS
    WFSrequest = f'/gis/services/wfs/{type_service}/MapServer/WFSServer?request=GetFeature' \
                 f'&service=WFS&version={config.baysis_version}&TypeName={type_name}'
    if srs_name is not None:
        WFSrequest += f'&srsName={srs_name}'
    if max_features != 0:
        WFSrequest += f'&maxFeatures={max_features}'
    if bbox is not None:
        WFSrequest += f'&BBOX={bbox}'

    print('Requested format: ' + type_coordinate)
    print('The URL requested: \t' + url + WFSrequest)

    ####################### CONNECT TO API ########################

    start_time = time.time()
    # Request and Receive Response
    con = HTTPSConnection(url, timeout=3600)
    con.request('GET', WFSrequest)
    response = con.getresponse()
    end_time = time.time()
    xml = response.read()
    con.close()

    if max_features == 0:
        print('Time needed for Server response: {0:.1f}s (unlimited features)'.format(end_time - start_time))
    else:
        print('Time needed for Server response: {0:.1f}s ({1} features)'.format(end_time - start_time, max_features))

    ####################### Save As XML ########################
    t_name = type_name.replace(':', '_')
    filename = f'{t_name}_{type_coordinate}.xml'
    with open(paths.baysis_data_path + filename, 'wb') as f:
        f.write(xml)

    # Finish
    print('Finished loading <{}> from BAYSIS' .format(t_name))


if __name__ == '__main__':
    from config import paths as paths
    from config import config as config

    # Test code snippet
    type_service = 'BAYSIS_Strassenbestand'
    type_coordinate = 'Krueger'
    type_name = 'STRBESTAND_WFS:Fahrstreifen'  # visuell
    # type_name = 'STRBESTAND_WFS:Fahrbahnbreiten'   # Fahrbahnbreite
    max_features = 20
    baysis_api(type_name,  type_service, type_coordinate, max_features, paths, config)


####################### EXAMPLE URL ########################
# https://www.baysis.bayern.de/gis/services/wfs/BAYSIS_Strassenbestand/MapServer/WFSServer?request=GetFeature&Service=WFS&Version=2.0.0&TypeName=STRBESTAND_WFS:Fahrbahnbreiten&srsName=urn:ogc:def:crs:EPSG:31468&maxFeatures=10
