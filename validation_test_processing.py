from activity_reader import ActivityReader
import numpy as np
from w_bal import *
from plotting import *
import matplotlib.pyplot as plt
import pandas as pd

# Read the validation tests
val_test_1 = ActivityReader("Validation_test_240s_rec.tcx")
val_test_2 = ActivityReader("Validation_test_30s_rec.tcx")

# Define CP and W'
cp = 265
w_prime = 26630

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
val_test_1_dict = {
    "work_bout_1": [val_test_1.power[0:248], val_test_1.cadence[0:248], val_test_1.heart_rate[0:248]],
    "recovery_1": [val_test_1.power[248:488], val_test_1.cadence[248:488], val_test_1.heart_rate[248:488]],
    "work_bout_2": [val_test_1.power[488:602], val_test_1.cadence[488:602], val_test_1.heart_rate[488:602]],
    "recovery_2": [val_test_1.power[602:846], val_test_1.cadence[602:846], val_test_1.heart_rate[602:846]],
    "work_bout_3": [val_test_1.power[846:len(val_test_1.power)], val_test_1.cadence[846:len(val_test_1.power)], val_test_1.heart_rate[846:len(val_test_1.power)]]
}
val_test_2_dict = {
    "work_bout_1": [val_test_2.power[0:282], val_test_2.cadence[0:282], val_test_2.heart_rate[0:282]],
    "recovery_1": [val_test_2.power[282:319], val_test_2.cadence[282:319], val_test_2.heart_rate[282:319]],
    "work_bout_2": [val_test_2.power[319:388], val_test_2.cadence[319:388], val_test_2.heart_rate[319:388]],
    "recovery_2": [val_test_2.power[388:423], val_test_2.cadence[388:423], val_test_2.heart_rate[388:423]],
    "work_bout_3": [val_test_2.power[423:len(val_test_2.power)], val_test_2.cadence[423:len(val_test_2.power)], val_test_2.heart_rate[423:len(val_test_2.power)]]
}

for elem in [val_test_1_dict, val_test_2_dict]:
    for key in elem:
        print(f"{key}: Average power = {round(np.mean(elem[key][0]))}, time = {len(elem[key][0])}, average cadence = {round(np.mean(elem[key][1]))}, HR change = {elem[key][2][-1]-elem[key][2][0]}, \% W' exp = {round(np.sum([power-cp for power in elem[key][0]]),1)}")
    print('\n')


# Plot the power outputs
avg_power_val1 = len(val_test_1_dict["work_bout_1"][0])*[np.average(val_test_1_dict["work_bout_1"][0])] + len(val_test_1_dict["recovery_1"][0])*[np.average(val_test_1_dict["recovery_1"][0])] + len(val_test_1_dict["work_bout_2"][0])*[np.average(val_test_1_dict["work_bout_2"][0])]+ len(val_test_1_dict["recovery_2"][0])*[np.average(val_test_1_dict["recovery_2"][0])]+ len(val_test_1_dict["work_bout_3"][0])*[np.average(val_test_1_dict["work_bout_3"][0])]
compare_power([val_test_1.power, avg_power_val1, len(val_test_1.power)*[cp]], val_test_1.time, ['Power', 'Average power', f'CP: {cp}W'], 'Validation test 240s recovery')

avg_power_val2 = len(val_test_2_dict["work_bout_1"][0])*[np.average(val_test_2_dict["work_bout_1"][0])] + len(val_test_2_dict["recovery_1"][0])*[np.average(val_test_2_dict["recovery_1"][0])] + len(val_test_2_dict["work_bout_2"][0])*[np.average(val_test_2_dict["work_bout_2"][0])]+ len(val_test_2_dict["recovery_2"][0])*[np.average(val_test_2_dict["recovery_2"][0])]+ len(val_test_2_dict["work_bout_3"][0])*[np.average(val_test_2_dict["work_bout_3"][0])]
compare_power([val_test_2.power, avg_power_val2, len(val_test_2.power)*[cp]], val_test_2.time, ['Power', 'Average power', f'CP: {cp}W'], 'Validation test 30s recovery')

# Finding the average of the first work bout and recovery
avg_work_rec_val1 = np.mean(np.concatenate((val_test_1_dict["work_bout_1"][0],val_test_1_dict["recovery_1"][0])))
avg_work_rec_val2 = np.mean(np.concatenate((val_test_2_dict["work_bout_1"][0],val_test_2_dict["recovery_1"][0])))

# Finding the average of the first work bout, the first recovery and second work bout
avg_work_rec_work_val1 = np.mean(val_test_1.power[0:602])
avg_work_rec_work_val2 = np.mean(val_test_2.power[0:388])

# Plotting the averages
compare_power([val_test_1.power[0:602], 488*[avg_work_rec_val1], 602*[avg_work_rec_work_val1], 602*[cp]], legends=['power', f'average power {round(avg_work_rec_val1)}W', f'average power {round(avg_work_rec_work_val1)}W', f'CP: {cp}W'])
compare_power([val_test_2.power[0:388], 319*[avg_work_rec_val2], 388*[avg_work_rec_work_val2], 388*[cp]], legends=['power', f'average power {round(avg_work_rec_val2)}W', f'average power {round(avg_work_rec_work_val2)}W', f'CP: {cp}W'])

# Calculate w_bal with different algorithms
val1_power = pd.DataFrame(dict(power=val_test_1.power), index=val_test_1.time)
val2_power = pd.DataFrame(dict(power=val_test_2.power), index=val_test_2.time)

# Establised models
w_bal_ode_val1 = w_prime_balance_ode(val1_power["power"], cp, w_prime)
w_bal_ode_val2 = w_prime_balance_ode(val2_power["power"], cp, w_prime)
w_bal_int_val1 = w_prime_balance_integral(val1_power["power"], cp, w_prime, tau_dynamic=True)
w_bal_int_val2 = w_prime_balance_integral(val2_power["power"], cp, w_prime, tau_dynamic=True)
w_bal_bartram_val1 = w_prime_balance_bartram(val1_power["power"], cp, w_prime)
w_bal_bartram_val2 = w_prime_balance_bartram(val2_power["power"], cp, w_prime)

# Models with fitted parameters
w_bal_int_reg_val1 = w_bal_integral_regression(val1_power["power"], cp, w_prime, a=1362, b=-0.033, c=451)
w_bal_int_reg_val2 = w_bal_integral_regression(val2_power["power"], cp, w_prime, a=1362, b=-0.033, c=451)
w_bal_ode_reg_val1 = w_bal_ode_regression(val1_power["power"], cp, w_prime, d=765373, e=-1.847)
w_bal_ode_reg_val2 = w_bal_ode_regression(val2_power["power"], cp, w_prime, d=765373, e=-1.847)
w_bal_biexp_val1, FC_bal_val1, SC_bal_val1 = w_prime_balance_bi_exp_regression(val1_power["power"], cp, w_prime, fc=4.4 , sc=1.1)
w_bal_biexp_val2, FC_bal_val2, SC_bal_val2 = w_prime_balance_bi_exp_regression(val2_power["power"], cp, w_prime, fc=4.4 , sc=1.1)

# Plot W'balance for the established models
plt.subplot(2,1,1)
plt.xlabel("Time [s]")
plt.ylabel("W'bal [J]")
plt.title("W'balance validation test 240s recovery")
plt.ylim(-7000,30000)
plt.plot(val_test_1.time, w_bal_ode_val1)
plt.plot(val_test_1.time, w_bal_int_val1)
plt.plot(val_test_1.time, w_bal_bartram_val1)
plt.legend(['ODE', 'Integral', 'Bartram'])

plt.subplot(2,1,2)
plt.xlabel("Time [s]")
plt.ylabel("W'bal [J]")
plt.title("W'balance validation test 30s recovery")
plt.ylim(-7000,30000)
plt.plot(val_test_2.time, w_bal_ode_val2)
plt.plot(val_test_2.time, w_bal_int_val2)
plt.plot(val_test_2.time, w_bal_bartram_val2)
plt.legend(['ODE', 'Integral', 'Bartram'])
plt.subplots_adjust(hspace=0.7)
plt.show()

# Plot the ODE and Integral models with and without fitted parameters
plt.subplot(2,1,1)
plt.xlabel("Time [s]")
plt.ylabel("W'bal [J]")
plt.title("W'balance validation test 240s recovery")
plt.ylim(-7000,30000)
plt.plot(val_test_1.time, w_bal_ode_val1)
plt.plot(val_test_1.time, w_bal_int_val1)
plt.plot(val_test_1.time, w_bal_int_reg_val1)
plt.plot(val_test_1.time, w_bal_ode_reg_val1)
plt.legend(['ODE', 'Integral', 'Integral with fitted tau', 'ODE with fitted tau'])

plt.subplot(2,1,2)
plt.xlabel("Time [s]")
plt.ylabel("W'bal [J]")
plt.title("W'balance validation test 30s recovery")
plt.ylim(-7000,30000)
plt.plot(val_test_2.time, w_bal_ode_val2)
plt.plot(val_test_2.time, w_bal_int_val2)
plt.plot(val_test_2.time, w_bal_int_reg_val2)
plt.plot(val_test_2.time, w_bal_ode_reg_val2)
plt.legend(['ODE', 'Integral', 'Integral with fitted tau', 'ODE with fitted tau'])
plt.subplots_adjust(hspace=0.7)
plt.show()


# Plot the bi-exponential model
plt.subplot(2,1,1)
plt.title("Validation test with 240s recovery")
plt.plot(w_bal_biexp_val1)
plt.legend(['Bi-exp model'])
plt.subplots_adjust(hspace=0.7)
plt.subplot(2,1,2)
plt.plot(FC_bal_val1)
plt.plot(SC_bal_val1)
plt.legend(['FC bal', 'SC bal'])
plt.ylabel("W' bal [J]")
plt.xlabel("Time [s]")
plt.subplots_adjust(hspace=0.7)
plt.show()

plt.subplot(2,1,1)
plt.title("Validation test with 30s recovery")
plt.plot(w_bal_biexp_val2)
plt.legend(['Bi-exp model'])
plt.subplots_adjust(hspace=0.7)
plt.subplot(2,1,2)
plt.plot(FC_bal_val2)
plt.plot(SC_bal_val2)
plt.legend(['FC bal', 'SC bal'])
plt.ylabel("W' bal [J]")
plt.xlabel("Time [s]")
plt.subplots_adjust(hspace=0.7)
plt.show()

# Plot predicted vs actual recovery
# Actual:
rec1_actual_val1 = np.sum([power-cp for power in val_test_1_dict["work_bout_2"][0]])
rec2_actual_val1 = np.sum([power-cp for power in val_test_1_dict["work_bout_3"][0]])
rec1_actual_val2 = np.sum([power-cp for power in val_test_2_dict["work_bout_2"][0]])
rec2_actual_val2 = np.sum([power-cp for power in val_test_2_dict["work_bout_3"][0]])

# Predicted by ODE algorithm
rec1_predicted_ode_val1 = w_bal_ode_val1[488]-w_bal_ode_val1[248]
rec2_predicted_ode_val1 = w_bal_ode_val1[846]-w_bal_ode_val1[602]

rec1_predicted_ode_val2 = w_bal_ode_val2[319]-w_bal_ode_val2[282]
rec2_predicted_ode_val2 = w_bal_ode_val2[423]-w_bal_ode_val2[388]

# Predicted by integral algorithm
rec1_predicted_int_val1 = w_bal_int_val1[488]-w_bal_int_val1[248]
rec2_predicted_int_val1 = w_bal_int_val1[846]-w_bal_int_val1[602]

rec1_predicted_int_val2 = w_bal_int_val2[319]-w_bal_int_val2[282]
rec2_predicted_int_val2 = w_bal_int_val2[423]-w_bal_int_val2[388]

# Predicted by bartram algorithm
rec1_predicted_bartram_val1 = w_bal_bartram_val1[488]-w_bal_bartram_val1[248]
rec2_predicted_bartram_val1 = w_bal_bartram_val1[846]-w_bal_bartram_val1[602]

rec1_predicted_bartram_val2 = w_bal_bartram_val2[319]-w_bal_bartram_val2[282]
rec2_predicted_bartram_val2 = w_bal_bartram_val2[423]-w_bal_bartram_val2[388]

# Predicted by bi exp algorithm
rec1_predicted_biexp_val1 = w_bal_biexp_val1[488]-w_bal_biexp_val1[248]
rec2_predicted_biexp_val1 = w_bal_biexp_val1[846]-w_bal_biexp_val1[602]

rec1_predicted_biexp_val2 = w_bal_biexp_val2[319]-w_bal_biexp_val2[282]
rec2_predicted_biexp_val2 = w_bal_biexp_val2[423]-w_bal_biexp_val2[388]

actual_recs = [rec1_actual_val1, rec2_actual_val1, rec1_actual_val2, rec2_actual_val2]
predicted_ode_recs = [rec1_predicted_ode_val1, rec2_predicted_ode_val1, rec1_predicted_ode_val2, rec2_predicted_ode_val2]
predicted_int_recs = [rec1_predicted_int_val1, rec2_predicted_int_val1, rec1_predicted_int_val2, rec2_predicted_int_val2]
predicted_bartram_recs = [rec1_predicted_bartram_val1, rec2_predicted_bartram_val1, rec1_predicted_bartram_val2, rec2_predicted_bartram_val2]
predicted_biexp_recs = [rec1_predicted_biexp_val1, rec2_predicted_biexp_val1, rec1_predicted_biexp_val2, rec2_predicted_biexp_val2]

width = 0.1
x = np.arange(4)
plt.bar(x-0.2, np.array(actual_recs)/w_prime*100, width)
plt.bar(x-0.1, np.array(predicted_ode_recs)/w_prime*100, width)
plt.bar(x, np.array(predicted_int_recs)/w_prime*100, width)
plt.bar(x+0.1, np.array(predicted_bartram_recs)/w_prime*100, width)
plt.bar(x+0.2, np.array(predicted_biexp_recs)/w_prime*100, width)
plt.xticks(x, ['Recovery 1: 240s', 'Recovery 2: 240s', 'Recovery 1: 30s', 'Recovery 2: 30s'])
plt.legend(['Actual', 'ODE', 'Integral', 'Bartram', 'Bi-exp exponential'])
plt.ylabel("W' reconstitution (%)")
plt.title("W' reconstitution")
plt.show()