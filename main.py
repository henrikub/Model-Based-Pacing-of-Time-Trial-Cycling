from activity_reader import ActivityReader
act = ActivityReader("400W_test.tcx")
distance, time, elevation, latitude, longitude, heart_rate, cadence, power, speed = act.get_activity_data()


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from plotting import *
from test_processing import *


new_arr = remove_unactive_period(100, power, cadence, heart_rate, time)
power, cadence, heart_rate, time = new_arr
print(f"Average power is {np.average(power)}W")
print(f"Average cadence is {np.average(cadence)}rpm")
print(f"Max heartrate is {np.max(heart_rate)}bpm")
print(f"Total time is {time[-1]}s")


