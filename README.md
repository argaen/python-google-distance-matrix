#python-google-distance-matrix

Code to retrieve information about distance matrix service from Google.

Use the test.py for a sample execution.

Example output from test.py: 
    {'41.129085, 1.242108': 90204, '41.120085, 1.444108': 78072}
    {'41.129085, 1.243108': 90283, '41.129085, 1.242108': 90204, '41.129087, 1.244108': 90348, '41.139085, 1.244108': 92046, '41.129085, 1.244108': 90348, '41.120085, 1.444108': 78072, '42.129085, 1.244108': 127176}

First line is the result of call `a.get_closest_points(max_distance=90250)` which returns points within 90250 meters in radius from the fixed origin in the `make_request` call.
Second line returns the distances from the origin to all destinations set in the `make_request` call.

You can set more than one origin. If you set 2 origins and 2 destinations, you will be returned a dictionary with 4 elements. Distances from 1st origin to all destinations (2) and distances from 2nd origin to all destinations (2).


##Features
* Get distance (in meters) between origin/s and destination/s points. Use wether coordinates or addresses as input data.
* Get time (in seconds) between origin/s and destination/s points. Use wether coordinates or addresses as input data.

##TODO
* Use api key
