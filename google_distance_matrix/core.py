# Python Google Distance Matrix. Code to calculate distances between different points using google distance matrix.
# Copyright (C) 2014  Manuel Miranda de Cid (manu.mirandad@gmail.com)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.



import json
import urllib2
import urllib
import os
import copy
import ast
import operator

DISTANCE_MATRIX_URL = "http://maps.googleapis.com/maps/api/distancematrix/"


class DM(object):

    def __init__(self, api_key=None, url=DISTANCE_MATRIX_URL):
        """
        :param api_key: google api key. default: None (queries limited by ip).
        :param url: google api url for distance matrix. default: DISTANCE_MATRIX_URL
        """

        self.api_key = api_key
        self.url = url
        self.response = ''
        self.dict_response = {'distance': {'value': {}, 'text': {}, },
                              'duration': {'value': {}, 'text': {}, },
                              }

        self.origins = ''
        self.destinations = ''

    def make_request(self, origins, destinations, mode='driving'):
        data = {}
        self.origins = [origins] if type(origins) == str else origins
        self.destinations = [destinations] if type(destinations) == str else destinations
        data['origins'] = origins if type(origins) == str else '|'.join(origins)
        data['destinations'] = destinations if type(destinations) == str else '|'.join(destinations)

        data['mode'] = mode

        url_values = urllib.urlencode(data)
        output_format = 'json'
        url = os.path.join(self.url, output_format)

        # print ast.literal_eval(urllib2.urlopen(url + '?' + url_values).read())
        self.response = ast.literal_eval(urllib2.urlopen(url + '?' + url_values, timeout=5).read())['rows']
        self.dict_response = {'distance': {'value': {}, 'text': {}, },  # Reset temporary dict
                              'duration': {'value': {}, 'text': {}, },
                              }
        return True


    def __get_response_element_data(self, key1, key2):
        """
        For each origin an elements object is created in the ouput.
        For each destination, an object is created inside elements object. For example, if there are
        2 origins and 1 destination, 2 element objects with 1 object each are created. If there are
        2 origins and 2 destinations, 2 element objects with 2 objects each are created.
        """
        if not self.dict_response[key1][key2]:
            l = self.response
            for i, orig in enumerate(self.origins):
                self.dict_response[key1][key2][orig] = {}
                for j, dest in enumerate(self.destinations):
                    if l[i]['elements'][j]['status'] == 'OK':
                        self.dict_response[key1][key2][orig][dest] = l[i]['elements'][j][key1][key2]
                    else:
                        self.dict_response[key1][key2][orig][dest] = l[i]['elements'][j]['status']

        return self.dict_response[key1][key2]

    def get_distance_values(self):
        """
        Get distance values in meters between all the origins and destinations.
        """
        return self.__get_response_element_data('distance', 'value')

    def get_distance_texts(self):
        """
        Get distance values in text mode (less accurated) between all the origins and destinations.
        """
        return self.__get_response_element_data('distance', 'text')

    def get_time_values(self):
        """
        Get time values in seconds between all the origins and destinations.
        """
        return self.__get_response_element_data('duration', 'value')

    def get_time_texts(self):
        """
        Get time values in text mode (less accurated) between all the origins and destinations.
        """
        return self.__get_response_element_data('duration', 'text')

    def get_closest_points(self, max_distance=None, origin_index=0, origin_raw=None):
        """
        Get closest points to a given origin. Returns a list of 2 element tuples where first element is the destination and the second is the distance.
        """
        if not self.dict_response['distance']['value']:
            self.get_distance_values()

        if origin_raw:
            origin = copy.deepcopy(self.dict_response['distance']['value'][origin_raw])
        else:
            origin = copy.deepcopy(self.dict_response['distance']['value'][self.origins[origin_index]])

        tmp_origin = copy.deepcopy(origin)
        if max_distance is not None:
            for k, v in tmp_origin.iteritems():
                if v > max_distance or v == 'ZERO_RESULTS':
                    del(origin[k])

        return origin
