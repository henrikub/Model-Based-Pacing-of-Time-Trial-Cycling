from activity_reader import ActivityReader
import numpy as np
from w_bal import *
import sweat
from plotting import *
import matplotlib.pyplot as plt
import pandas as pd

# Read the validation tests
val_test_1 = ActivityReader("Validation_test_240s_rec.tcx")
val_test_2 = ActivityReader("Validation_test_30s_rec.tcx")

# Remove unactive periods
val_test_1.remove_unactive_period(900)
val_test_2.remove_unactive_period(400)

# Split into segments
work_bout_1_val2 = val_test_2.power[0:282]
recovery_1_val2 = val_test_2.power[282:319]
work_bout_2_val2 = val_test_2.power[319:388]
recovery_2_val2 = val_test_2.power[388:423]
work_bout_3_val2 = val_test_2.power[423:len(val_test_2.power)]

work_bout_1_val1 = val_test_1.power[0:248]
recovery_1_val1 = val_test_1.power[248:488]
work_bout_2_val1 = val_test_1.power[488:602]
recovery_2_val1 = val_test_1.power[602:846]
work_bout_3_val1 = val_test_1.power[846:len(val_test_1.power)]

# Define CP and AWC
cp = 265
awc = 26630

# Print stats about the tests
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

# Remove the incorrect values where the power is zero
for i in range(10,len(val_test_1.power)):
    if val_test_1.power[i] == 0:
        val_test_1.power[i] = val_test_1.power[i+1]


for i in range(10,len(val_test_2.power)):
    if val_test_2.power[i] == 0:
        val_test_2.power[i] = val_test_2.power[i+1]

# Plot the power outputs
avg_power_val1 = len(work_bout_1_val1)*[np.average(work_bout_1_val1)] + len(recovery_1_val1)*[np.average(recovery_1_val1)] + len(work_bout_2_val1)*[np.average(work_bout_2_val1)]+ len(recovery_2_val1)*[np.average(recovery_2_val1)]+ len(work_bout_3_val1)*[np.average(work_bout_3_val1)]
compare_power([val_test_1.power, avg_power_val1, len(val_test_1.power)*[cp]], val_test_1.time, ['Power', 'Average power', 'CP'], 'Validation test')

avg_power_val2 = len(work_bout_1_val2)*[np.average(work_bout_1_val2)] + len(recovery_1_val2)*[np.average(recovery_1_val2)] + len(work_bout_2_val2)*[np.average(work_bout_2_val2)]+ len(recovery_2_val2)*[np.average(recovery_2_val2)]+ len(work_bout_3_val2)*[np.average(work_bout_3_val2)]
compare_power([val_test_2.power, avg_power_val2, len(val_test_2.power)*[cp]], val_test_2.time, ['Power', 'Average power', 'CP'], 'Validation test')

# Calculate w_bal with different algorithms
val1_power = pd.DataFrame(dict(power=val_test_1.power), index=val_test_1.time)
val2_power = pd.DataFrame(dict(power=val_test_2.power), index=val_test_2.time)

w_bal_dif_val1 = differential_w_bal(val_test_1.power, cp, awc)
w_bal_dif_val2 = differential_w_bal(val_test_2.power, cp, awc)
w_bal_int_val1 = sweat.w_prime_balance(val1_power["power"], cp=cp, algorithm='waterworth', w_prime=awc).to_list()
w_bal_int_val2 = sweat.w_prime_balance(val2_power["power"], cp=cp, algorithm='waterworth', w_prime=awc).to_list()

fig, ax1 = plt.subplots()
plt.xlabel("Time [s]")
ax1.set_ylabel("W' bal [J]")
plt.title("Differential W' bal")
ax2 = ax1.twinx()
ax2.set_ylabel("Power [W]", color='tab:blue')
ax1.plot(val_test_1.time, w_bal_dif_val1)
ax1.plot(val_test_1.time, w_bal_int_val1)
ax2.plot(val_test_1.time, avg_power_val1, color='tab:blue')
ax2.tick_params(axis='y', labelcolor='tab:blue')
# text_val1 = f"W'exp1 = {w_prime_exp_val1[0]}J\n W'exp2 = {w_prime_exp_val1[1]}J\n W'exp3 = {w_prime_exp_val1[2]}J"
# plt.text(0.8, 0.6, text_val1, ha='center', va='center', transform=plt.gca().transAxes, fontsize='large')
fig.tight_layout() 
plt.show()

plt.plot(val_test_2.time, w_bal_dif_val2)
plt.plot(val_test_2.time, w_bal_int_val2)
plt.plot(val_test_2.time, avg_power_val2)
plt.xlabel("Time [s]")
plt.ylabel("W' bal [J]")
plt.title("Differential W' bal")
text = f"W'exp1 = {w_prime_exp_val2[0]}J\n W'exp2 = {w_prime_exp_val2[1]}J\n W'exp3 = {w_prime_exp_val2[2]}J"
plt.text(0.8, 0.6, text, ha='center', va='center', transform=plt.gca().transAxes, fontsize='large')
plt.show()

