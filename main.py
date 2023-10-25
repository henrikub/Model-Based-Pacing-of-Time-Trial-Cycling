from activity_reader import ActivityReader
act = ActivityReader("300W_test.tcx")
distance, time, elevation, latitude, longitude, heart_rate, cadence, power, speed = act.get_activity_data()


import pandas as pd
import matplotlib.pyplot as plt
import sweat
import numpy as np
from plotting import *
from test_processing import *

data = pd.DataFrame(dict(power=power), index=time)

cp = 287
w_prime = 9000

# w_bal_waterworth = sweat.w_prime_balance(data["power"], cp=cp, algorithm='waterworth', w_prime=w_prime).to_list()
# w_bal_fsc = sweat.w_prime_balance(data["power"], cp=cp, algorithm='froncioni-skiba-clarke', w_prime=w_prime).to_list()

# compare_power([w_bal_waterworth, w_bal_fsc], distance, legends=["waterworth", "froncioni-skiba-clarke"])

# compare_power([power, [cp]*len(power)], distance, legends=["power", "cp"])


new_arr = remove_unactive_period(600, power, cadence, heart_rate, time)
power, cadence, heart_rate, time = new_arr
print(f"Average power is {np.average(power)}W")
print(f"Average cadence is {np.average(cadence)}rpm")
print(f"Max heartrate is {np.max(heart_rate)}bpm")
print(f"Total time is {time[-1]}s")

#plt.subplot(3,1,1)
# plt.plot(distance, w_bal_waterworth)
# plt.plot(distance, w_bal_skiba)
# plt.plot(distance, w_bal_fsc)
# plt.legend(["waterworth", "skiba", "froncioni-skiba-clarke"])


# plt.subplot(3,1,2)
# plt.plot(distance, power)
# plt.plot(distance, [cp]*len(distance))

# plt.subplot(3,1,3)
# plt.plot(distance, elevation)
# plt.show()



