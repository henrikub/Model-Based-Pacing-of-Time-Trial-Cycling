import pandas as pd
import matplotlib.pyplot as plt
import sweat
import numpy as np
from plotting import *
from activity_reader import ActivityReader
from w_bal import *

act = ActivityReader("Validation_test.tcx")
act.remove_unactive_period(900)

data = pd.DataFrame(dict(power=act.power), index=act.time)

cp = 265
w_prime = 26630

w_bal_waterworth = sweat.w_prime_balance(data["power"], cp=cp, algorithm='waterworth', w_prime=w_prime).to_list()
w_bal_fsc = sweat.w_prime_balance(data["power"], cp=cp, algorithm='froncioni-skiba-clarke', w_prime=w_prime).to_list()

compare_power([w_bal_waterworth, w_bal_fsc], act.distance, legends=["waterworth", "froncioni-skiba-clarke"])
print(min(w_bal_fsc))
print(min(w_bal_waterworth))

# test = sweat.w_prime_balance(data["power"], cp=cp, algorithm='skiba', w_prime=w_prime).to_list()
# test = integral_w_bal(act.power, cp, w_prime)
# plt.plot(test)
# plt.show()

# w_bal_skiba = sweat.w_prime_balance(data["power"], cp=cp, algorithm='waterworth', w_prime=w_prime).to_list()
# plt.plot(w_bal_skiba)
# plt.show()




