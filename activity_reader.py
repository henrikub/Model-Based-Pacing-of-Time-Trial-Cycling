from tcxreader.tcxreader import TCXReader

class ActivityReader():
    def __init__(self, filename):
        tcx_reader = TCXReader()
        file_location = 'Activities/' + filename
        data = tcx_reader.read(file_location)
        self.points = data.trackpoints

    def get_activity_data(self):
        distance = [point.distance for point in self.points]
        datetime = [point.time for point in self.points]
        time = [(dt - datetime[0]).total_seconds() for dt in datetime]
        elevation = [point.elevation for point in self.points]
        latitude = [point.latitude for point in self.points]
        longitude = [point.longitude for point in self.points]
        heart_rate = [point.hr_value for point in self.points]
        cadence = [point.cadence for point in self.points]
        power = [point.tpx_ext['Watts'] for point in self.points]
        speed = [point.tpx_ext['Speed'] for point in self.points]

        return distance, time, elevation, latitude, longitude, heart_rate, cadence, power, speed
