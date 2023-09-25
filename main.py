# import gpxpy
# import gpxpy.gpx
# import pandas as pd
# from parameters import *


# gpx_file = open('Activities/FTP_test.gpx', 'r', encoding="utf8")
# gpx = gpxpy.parse(gpx_file)
# points =  gpx.get_points_data()

# dist = []
# elevation = []
# latitude = []
# longitude = []
# time = []
# speed = []
# heart_rate = []
# for i in range(len(points)):
#     dist.append(points[i].distance_from_start)
#     elevation.append(points[i].point.elevation)
#     latitude.append(points[i].point.latitude)
#     longitude.append(points[i].point.longitude)
#     speed.append(points[i].point.speed_between(points[i-1].point)* 60. ** 2 / 1000)


# gpx.get_points_no()

import tcxreader


