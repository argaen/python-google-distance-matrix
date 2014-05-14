import json
import urllib2
import urllib
import os
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
        self.response = ast.literal_eval(urllib2.urlopen(url + '?' + url_values).read())['rows']
        self.dict_response = {'distance': {'value': {}, 'text': {}, },  # Reset temporary dict
                              'duration': {'value': {}, 'text': {}, },
                              }


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

    def get_closest_points(self, num=10, origin_index=0, origin_raw=None):
        """
        Get closest points to a given origin. Returns a list of 2 element tuples where first element is the destination and the second is the distance.
        """

        if self.dict_response['distance']['value']:
            if origin_raw:
                return sorted(self.dict_response['distance']['value'][origin_raw].iteritems(), key=operator.itemgetter(1))[:num]
            else:
                return sorted(self.dict_response['distance']['value'][self.origins[origin_index]].iteritems(), key=operator.itemgetter(1))[:num]
        else:
            if origin_raw:
                return sorted(self.get_distance_values()[origin_raw].iteritems(), key=operator.itemgetter(1))[:num]
            else:
                return sorted(self.get_distance_values()[self.origins[origin_index]].iteritems(), key=operator.itemgetter(1))[:num]


if __name__ == "__main__":

    a = DM()
    # a.make_request('Boscos de Tarragona 12 Tarragona Spain', '42.133649, 1.247142', mode="walking")
    # a.make_request('Boscos de Tarragona 12 Tarragona Spain', '42.133649, 1.247142', mode="driving")
    # a.make_request(['Avinguda Paisos Catalans 26 Spain', '42.133649, 1.247142'], ['41.129085, 1.244108', '41.129085, 1.242108', '41.129085, 1.243108'])
    a.make_request(['Avinguda Paisos Catalans 26 Spain'], ['41.129085, 1.244108', '41.129085, 1.242108', '41.129085, 1.243108', '41.139085, 1.244108', '41.120085, 1.444108', '41.129087, 1.244108', '42.129085, 1.244108' ])
    print a.get_distance_values()
    print a.get_closest_points(num=2)
    # print a.get_closest_points(origin_raw='Avinguda Paisos Catalans 26 Spain')
