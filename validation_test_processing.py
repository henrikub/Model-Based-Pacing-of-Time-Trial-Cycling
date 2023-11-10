from activity_reader import ActivityReader
import numpy as np
from w_bal import *
from plotting import *
import matplotlib.pyplot as plt

val_test_1 = ActivityReader("Validation_test_240s_rec.tcx")
val_test_1.remove_unactive_period(900)

val_test_2 = ActivityReader("Validation_test_30s_rec.tcx")
val_test_2.remove_unactive_period(400)

work_bout_1_val2 = val_test_2.power[0:281]
recovery_1_val2 = val_test_2.power[281:281+30]
work_bout_2_val2 = val_test_2.power[311:379]
recovery_2_val2 = val_test_2.power[379:379+30]
work_bout_3_val2 = val_test_2.power[409:len(val_test_2.power)]


work_bout_1_val1 = val_test_1.power[0:248]
recovery_1_val1 = val_test_1.power[248:248+240]
work_bout_2_val1 = val_test_1.power[488:602]
recovery_2_val1 = val_test_1.power[602:602+240]
work_bout_3_val1 = val_test_1.power[842:len(val_test_1.power)]

cp = 265
awc = 26630
print("For the first test:")
for i, elem in enumerate([recovery_1_val1, recovery_2_val1]):
    print(f"Average power for recovery {i+1} was {np.average(elem)}\n")

w_prime_exp_val1 = []
for i, elem in enumerate([work_bout_1_val1, work_bout_2_val1, work_bout_3_val1]):
    w_prime_exp_val1.append(np.sum([power-cp for power in elem]))
    print(f"Average power for work bout {i+1} is {np.average(elem)}W")
    print(f"W' expended for work bout {i+1} is {w_prime_exp_val1[i]/1000}kJ\n")

print("For the second test:")
for i, elem in enumerate([recovery_1_val2, recovery_2_val2]):
    print(f"Average power for recovery {i+1} was {np.average(elem)}\n")

w_prime_exp_val2 = []
for i, elem in enumerate([work_bout_1_val2, work_bout_2_val2, work_bout_3_val2]):
    w_prime_exp_val2.append(np.sum([power-cp for power in elem]))
    print(f"Average power for work bout {i+1} is {np.average(elem)}W")
    print(f"W' expended for work bout {i+1} is {w_prime_exp_val2[i]/1000}kJ\n")

# power = np.zeros(len(val_test_1.power))
# for i in range(len(val_test_1.power)):
#     if val_test_1.power[i] == 0:
#         power[i] = val_test_1.power[i+1]
#     else:
#         power[i] = val_test_1.power[i]

w_bal = differential_w_bal(val_test_2.power, cp, awc)
plt.plot(val_test_2.time, w_bal)
plt.xlabel("Time [s]")
plt.ylabel("W' bal [J]")
plt.title("Differential W' bal")
text = f"W'exp1 = {w_prime_exp_val2[0]}J\n W'exp2 = {w_prime_exp_val2[1]}J\n W'exp3 = {w_prime_exp_val2[2]}J"
plt.text(0.8, 0.6, text, ha='center', va='center', transform=plt.gca().transAxes, fontsize='large')
plt.show()
print(min(w_bal))

# avg_power = 248*[360] + 240*[216] + 114*[359] + 240*[214] + 107*[362]
# compare_power([val_test_1.power, avg_power, len(val_test_2.power)*[cp]], val_test_1.time, ['Power', 'Average power', 'CP'], 'Validation test')

avg_power = len(work_bout_1_val2)*[np.average(work_bout_1_val2)] + 30*[np.average(recovery_1_val2)] + len(work_bout_2_val1)*[np.average(work_bout_2_val2)]+ 30*[np.average(recovery_2_val2)]+ len(work_bout_3_val1)*[np.average(work_bout_3_val2)]
compare_power([val_test_2.power, avg_power, len(val_test_2.power)*[cp]], val_test_2.time, ['Power', 'Average power', 'CP'], 'Validation test')
