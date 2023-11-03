import pandas as pd
import matplotlib.pyplot as plt
import sweat
import numpy as np
from plotting import *
from activity_reader import ActivityReader

act = ActivityReader("300W_test.tcx")
distance, time, elevation, latitude, longitude, heart_rate, cadence, power, speed = act.get_activity_data()

data = pd.DataFrame(dict(power=power), index=time)

cp = 266
w_prime = 25150

# w_bal_waterworth = sweat.w_prime_balance(data["power"], cp=cp, algorithm='waterworth', w_prime=w_prime).to_list()
# w_bal_fsc = sweat.w_prime_balance(data["power"], cp=cp, algorithm='froncioni-skiba-clarke', w_prime=w_prime).to_list()

# compare_power([w_bal_waterworth, w_bal_fsc], distance, legends=["waterworth", "froncioni-skiba-clarke"])

from w_bal import *
w_bal = bi_conditional_w_bal(power, cp, w_prime)
print(w_bal)

plt.plot(w_bal)
plt.show()