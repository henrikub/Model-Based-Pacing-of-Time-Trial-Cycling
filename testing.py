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
# test = bi_exponential_w_bal(act.power, cp, w_prime, 0.46)
# plt.plot(test)
# plt.show()

# w_bal_skiba = sweat.w_prime_balance(data["power"], cp=cp, algorithm='waterworth', w_prime=w_prime).to_list()
# plt.plot(w_bal_skiba)
# plt.show()
# work_bout_1 = act.power[3:248]
# recovery_1 = act.power[248:248+240]
# work_bout_2 = act.power[488:602]
# recovery_2 = act.power[602:602+240]
# work_bout_3 = act.power[842:len(act.power)]


# for i, elem in enumerate([recovery_1, recovery_2]):
#     print(f"Average power for recovery {i+1} was {np.average(elem)}\n")

# for i, elem in enumerate([work_bout_1, work_bout_2, work_bout_3]):
#     w_prime_exp = np.sum([power-cp for power in elem])
#     print(f"Average power for work bout {i+1} is {np.average(elem)}W")
#     print(f"W' expended for work bout {i+1} is {w_prime_exp/1000}kJ\n")




# def count_above_or_below_threshold(arr, thres):
#     diff = [power-thres for power in arr]
#     print(diff)
#     count = 1
#     result = []
#     for i in range(1, len(arr)):
#         if diff[i] * diff[i-1] >0:
#             count += 1
#         else:
#             for _ in range(count):
#                 result.append(count)
#             count = 1
#     for _ in range(count):
#         result.append(count)
#     return result




# arr = [300, 300, 200, 200, 200, 300, 299, 399, 300, 299, 399, 300, 299, 399]
# new_arr = count_above_or_below_threshold(act.power, 250)
# print(new_arr)

# def count_streaks(arr, thres):
#     diff = [power-thres for power in arr]
