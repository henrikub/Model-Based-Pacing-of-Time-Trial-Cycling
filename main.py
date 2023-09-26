from tcxreader.tcxreader import TCXReader, TCXTrackPoint

tcx_reader = TCXReader()
file_location = 'Activities/FTP_test.tcx'

data = tcx_reader.read(file_location)
points = data.trackpoints

print(points[3])
print(points[3].tpx_ext['Watts'])
print(points[3].tpx_ext['Speed'])
print(points[3].latitude)
print(points[3].longitude)
print(points[3].elevation)
print(points[3].distance)
print(points[3].cadence)

def get_data_from_activity(points):
    distance = [point.distance for point in points]
    elevation = [point.elevation for point in points]
    latitude = [point.latitude for point in points]
    longitude = [point.longitude for point in points]
    heart_rate = [point.hr_value for point in points]
    power = [point.tpx_ext['Watts'] for point in points]
    speed = [point.tpx_ext['Speed'] for point in points]

    return distance, elevation, latitude, longitude, heart_rate, power, speed


distance, elevation, latitude, longitude, heart_rate, power, speed = get_data_from_activity(points)
print(distance, elevation, latitude, longitude, heart_rate, power, speed)