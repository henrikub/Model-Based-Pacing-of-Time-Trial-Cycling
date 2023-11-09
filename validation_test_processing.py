from activity_reader import ActivityReader
import numpy as np
from w_bal import *
from plotting import *
import matplotlib.pyplot as plt

act = ActivityReader("Validation_test.tcx")
act.remove_unactive_period(900)

work_bout_1 = act.power[0:248]
recovery_1 = act.power[248:248+240]
work_bout_2 = act.power[488:602]
recovery_2 = act.power[602:602+240]
work_bout_3 = act.power[842:len(act.power)]

cp = 265
awc = 26630

for i, elem in enumerate([recovery_1, recovery_2]):
    print(f"Average power for recovery {i+1} was {np.average(elem)}\n")

w_prime_exp = []
for i, elem in enumerate([work_bout_1, work_bout_2, work_bout_3]):
    w_prime_exp.append(np.sum([power-cp for power in elem]))
    print(f"Average power for work bout {i+1} is {np.average(elem)}W")
    print(f"W' expended for work bout {i+1} is {w_prime_exp[i]/1000}kJ\n")

power = np.zeros(len(act.power))
for i in range(len(act.power)):
    if act.power[i] == 0:
        power[i] = act.power[i+1]
    else:
        power[i] = act.power[i]

w_bal = differential_w_bal(power, cp, awc)
plt.plot(act.time, w_bal)
plt.xlabel("Time [s]")
plt.ylabel("W' bal [J]")
plt.title("Differential W' bal")
text = f"W'exp1 = {w_prime_exp[0]}J\n W'exp2 = {w_prime_exp[1]}J\n W'exp3 = {w_prime_exp[2]}J"
plt.text(0.8, 0.6, text, ha='center', va='center', transform=plt.gca().transAxes, fontsize='large')
plt.show()
print(min(w_bal))

avg_power = 248*[360] + 240*[216] + 114*[359] + 240*[214] + 107*[362]
compare_power([power, avg_power, len(power)*[cp]], act.time, ['Power', 'Average power', 'CP'], 'Validation test')
