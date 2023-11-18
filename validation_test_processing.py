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

# Remove the incorrect values where the power is zero
for i in range(10,len(val_test_1.power)):
    if val_test_1.power[i] == 0:
        val_test_1.power[i] = val_test_1.power[i+1]


for i in range(10,len(val_test_2.power)):
    if val_test_2.power[i] == 0:
        val_test_2.power[i] = val_test_2.power[i+1]

# Split into segments
work_bout_1_val1 = val_test_1.power[0:248]
recovery_1_val1 = val_test_1.power[248:488]
work_bout_2_val1 = val_test_1.power[488:602]
recovery_2_val1 = val_test_1.power[602:846]
work_bout_3_val1 = val_test_1.power[846:len(val_test_1.power)]

work_bout_1_val2 = val_test_2.power[0:282]
recovery_1_val2 = val_test_2.power[282:319]
work_bout_2_val2 = val_test_2.power[319:388]
recovery_2_val2 = val_test_2.power[388:423]
work_bout_3_val2 = val_test_2.power[423:len(val_test_2.power)]

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

# Plot the power outputs
avg_power_val1 = len(work_bout_1_val1)*[np.average(work_bout_1_val1)] + len(recovery_1_val1)*[np.average(recovery_1_val1)] + len(work_bout_2_val1)*[np.average(work_bout_2_val1)]+ len(recovery_2_val1)*[np.average(recovery_2_val1)]+ len(work_bout_3_val1)*[np.average(work_bout_3_val1)]
compare_power([val_test_1.power, avg_power_val1, len(val_test_1.power)*[cp]], val_test_1.time, ['Power', 'Average power', 'CP'], 'Validation test')

avg_power_val2 = len(work_bout_1_val2)*[np.average(work_bout_1_val2)] + len(recovery_1_val2)*[np.average(recovery_1_val2)] + len(work_bout_2_val2)*[np.average(work_bout_2_val2)]+ len(recovery_2_val2)*[np.average(recovery_2_val2)]+ len(work_bout_3_val2)*[np.average(work_bout_3_val2)]
compare_power([val_test_2.power, avg_power_val2, len(val_test_2.power)*[cp]], val_test_2.time, ['Power', 'Average power', 'CP'], 'Validation test')

# Calculate w_bal with different algorithms
val1_power = pd.DataFrame(dict(power=val_test_1.power), index=val_test_1.time)
val2_power = pd.DataFrame(dict(power=val_test_2.power), index=val_test_2.time)

w_bal_dif_val1 = w_prime_balance_ode(val_test_1.power, cp, awc)
w_bal_dif_val2 = w_prime_balance_ode(val_test_2.power, cp, awc)
w_bal_int_val1 = sweat.w_prime_balance(val1_power["power"], cp=cp, algorithm='waterworth', w_prime=awc).to_list()
w_bal_int_val2 = sweat.w_prime_balance(val2_power["power"], cp=cp, algorithm='waterworth', w_prime=awc).to_list()

fig, ax1 = plt.subplots()
plt.xlabel("Time [s]")
ax1.set_ylabel("W' bal [J]")
plt.title("W' bal")
ax2 = ax1.twinx()
ax2.set_ylabel("Heart rate [bpm]", color='tab:red')
ax1.plot(val_test_1.time, w_bal_dif_val1)
ax1.plot(val_test_1.time, w_bal_int_val1)
ax2.plot(val_test_1.time, val_test_1.heart_rate, color='tab:red')
ax2.tick_params(axis='y', labelcolor='tab:red')
ax1.legend(['Differential algorithm', 'Integral algorithm'])
ax2.legend(['Heart rate'])
plt.show()

fig, ax1 = plt.subplots()
plt.xlabel("Time [s]")
ax1.set_ylabel("W' bal [J]")
plt.title("Differential W' bal")
ax2 = ax1.twinx()
ax2.set_ylabel("Heart rate [bpm]", color='tab:red')
ax1.plot(val_test_2.time, w_bal_dif_val2)
ax1.plot(val_test_2.time, w_bal_int_val2)
ax2.plot(val_test_2.time, val_test_2.heart_rate, color='tab:red')
ax2.tick_params(axis='y', labelcolor='tab:red')
ax1.legend(['Differential algorithm', 'Integral algorithm'])
ax2.legend(['Heart rate'])
plt.show()

# Plot predicted vs actual recovery
# Actual:
rec1_actual_val1 = w_prime_exp_val1[1]
rec2_actual_val1 = w_prime_exp_val1[2]
rec1_actual_val2 = w_prime_exp_val2[1]
rec2_actual_val2 = w_prime_exp_val2[2]

# Predicted by differential algorithm
rec1_predicted_dif_val1 = w_bal_dif_val1[488]-w_bal_dif_val1[248]
rec2_predicted_dif_val1 = w_bal_dif_val1[846]-w_bal_dif_val1[602]

rec1_predicted_dif_val2 = w_bal_dif_val2[319]-w_bal_dif_val2[282]
rec2_predicted_dif_val2 = w_bal_dif_val2[423]-w_bal_dif_val2[388]

# Predicted by integral algorithm
rec1_predicted_int_val1 = w_bal_int_val1[488]-w_bal_int_val1[248]
rec2_predicted_int_val1 = w_bal_int_val1[846]-w_bal_int_val1[602]

rec1_predicted_int_val2 = w_bal_int_val2[319]-w_bal_int_val2[282]
rec2_predicted_int_val2 = w_bal_int_val2[423]-w_bal_int_val2[388]



print(f"Rec 1 val1, actual = {rec1_actual_val1}. predicted dif = {rec1_predicted_dif_val1}, predicted int = {rec1_predicted_int_val1}")
print(f"Rec 1 val2, actual = {rec1_actual_val2}. predicted dif = {rec1_predicted_dif_val2}, predicted int = {rec1_predicted_int_val2}")

actual_recs = [rec1_actual_val1, rec2_actual_val1, rec1_actual_val2, rec2_actual_val2]
predicted_dif_recs = [rec1_predicted_dif_val1, rec2_predicted_dif_val1, rec1_predicted_dif_val2, rec2_predicted_dif_val2]
predicted_int_recs = [rec1_predicted_int_val1, rec2_predicted_int_val1, rec1_predicted_int_val2, rec2_predicted_int_val2]

width = 0.2
x = np.arange(4)
plt.bar(x-0.2, actual_recs, width)
plt.bar(x, predicted_dif_recs, width)
plt.bar(x+0.2, predicted_int_recs, width)
plt.xticks(x, ['Recovery 1: 240s', 'Recovery 2: 240s', 'Recovery 1: 30s', 'Recovery 2: 30s'])
plt.legend(['Actual', 'Differential algorithm', 'Integral algorithm'])
plt.title("W' recovery")
plt.ylabel("W' [J]")
plt.show()