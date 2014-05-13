import json
import urllib2
import urllib
import os

DISTANCE_MATRIX_URL = "http://maps.googleapis.com/maps/api/distancematrix/"


class DM(object):

    def __init__(self, api_key=None, url=DISTANCE_MATRIX_URL):
        """
        :param api_key: google api key. default: None (queries limited by ip).
        :param url: google api url for distance matrix. default: DISTANCE_MATRIX_URL
        """

        self.api_key = api_key
        self.url = url

    def get_distance(self, origins, destinations, output_format='json'):
        data = {}
        data['origins'] = origins
        data['destinations'] = destinations
        data['mode'] = "driving"

        url_values = urllib.urlencode(data)
        url = os.path.join(self.url, output_format)

        ret = urllib2.urlopen(url + '?' + url_values)

        print ret.readlines()
