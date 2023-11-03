from tcxreader.tcxreader import TCXReader

class ActivityReader():
    def __init__(self, filename):
        tcx_reader = TCXReader()
        file_location = 'Activities/' + filename
        data = tcx_reader.read(file_location)
        self.points = data.trackpoints
        
        self.distance = []
        self.time = []
        self.elevation =[]
        self.latitude = []
        self.longitude = []
        self.heart_rate = []
        self.cadence = []
        self.power = []
        self.speed = []
        self.get_activity_data()

        self.avg_power = 0
        self.total_time = 0

    def get_activity_data(self):
        self.distance = [point.distance for point in self.points]
        datetime = [point.time for point in self.points]
        self.time = [(dt - datetime[0]).total_seconds() for dt in datetime]
        self.elevation = [point.elevation for point in self.points]
        self.latitude = [point.latitude for point in self.points]
        self.longitude = [point.longitude for point in self.points]
        self.heart_rate = [point.hr_value for point in self.points]
        self.cadence = [point.cadence for point in self.points]
        self.power = [point.tpx_ext['Watts'] for point in self.points]
        self.speed = [point.tpx_ext['Speed'] for point in self.points]

    def find_last_active_datapoint(self, approx_time):
        for i in range(approx_time, len(self.power)):
            if self.power[i] < 100:
                return i

    def remove_unactive_period(self, approx_time):
        """
        Remove unactive time in an activity. Unactive is defined as power below 100W.
        """
        last_datapoint = self.find_last_active_datapoint(approx_time)

        data_attributes = [self.distance, self.time, self.elevation, self.latitude, self.longitude, self.heart_rate, self.cadence, self.power, self.speed]
        self.distance, self.time, self.elevation, self.latitude, self.longitude, self.heart_rate, self.cadence, self.power, self.speed = [attr[:last_datapoint] for attr in data_attributes]
        


