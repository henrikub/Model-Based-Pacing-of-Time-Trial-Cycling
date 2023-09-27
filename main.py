from activity_reader import ActivityReader
act = ActivityReader("FTP_test.tcx")
distance, time, elevation, latitude, longitude, heart_rate, cadence, power, speed = act.get_activity_data()

# from athletic_pandas.models import Athlete, WorkoutDataFrame
# import matplotlib.pyplot as plt


# wdf = WorkoutDataFrame(dict(
#     power=power
# ))
# wdf.athlete = Athlete(cp=350, w_prime=20000)

# fig_power = wdf.power.plot.area()
# fig_power.set_ylabel('power (Watt)')
# fig_power.set_xlabel('time (seconds)')
# wdf = wdf.assign(
#     w_balance_skiba=wdf.compute_w_prime_balance('skiba'),
#     w_balance_waterworth=wdf.compute_w_prime_balance('waterworth'),
#     w_balance_froncioni_skiba_clarke=wdf.compute_w_prime_balance('froncioni-skiba-clarke'),
# )
# fig_skiba_waterworth = wdf.loc[:, ['w_balance_skiba', 'w_balance_waterworth']].plot(ylim=0)
# fig_skiba_waterworth.set_ylabel('W\'balance (Joule)')
# fig_skiba_waterworth.set_xlabel('time (seconds)')

import pandas as pd
import matplotlib.pyplot as plt
import sweat

data = pd.DataFrame(dict(power=power), index=time)

# Define the model coefficients
cp = 230
w_prime = 15000

data["W'balance"] = sweat.w_prime_balance(data["power"], cp=cp, w_prime=w_prime).to_list()

plt.subplot(3,1,1)
plt.plot(distance, data["W'balance"])

plt.subplot(3,1,2)
plt.plot(distance, power)
plt.plot(distance, [cp]*len(distance))

plt.subplot(3,1,3)
plt.plot(distance, elevation)
plt.show()

