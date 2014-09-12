from core import DM
import urllib2

if __name__ == "__main__":

    a = DM()
    try:
        # a.make_request('Avinguda Paisos catalans 26 Spain', '42.133649, 1.247142', mode="walking")
        # a.make_request('Avinguda Paisos catalans 26 Spain', '42.133649, 1.247142', mode="driving")
        # a.make_request(['Avinguda Paisos Catalans 26 Spain', '42.133649, 1.247142'], ['41.129085, 1.244108', '41.129085, 1.242108', '41.129085, 1.243108'])

        a.make_request(['Avinguda Paisos Catalans 26 Spain'], ['41.129085, 1.244108', '41.129085, 1.242108', '41.129085, 1.243108', '41.139085, 1.244108', '41.120085, 1.444108', '41.129087, 1.244108', '42.129085, 1.244108'])
        print a.get_closest_points(max_distance=90250)
        print a.get_closest_points()
        # print a.get_closest_points(origin_raw='Avinguda Paisos Catalans 26 Spain')

    except urllib2.URLError, e:
        print "Error:",e
