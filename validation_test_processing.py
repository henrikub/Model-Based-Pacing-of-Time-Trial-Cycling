import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from activity_reader import ActivityReader
from w_bal import *
from plotting import *

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

# Dictionaries for the time indices
val1_indices = {
    "end_wb1": 248,
    "start_wb2": 488,
    "end_wb2": 602,
    "start_wb3": 846,
    "end_wb3": len(val_test_1.power)
}
val2_indices = {
    "end_wb1": 282,
    "start_wb2": 319,
    "end_wb2": 388,
    "start_wb3": 423,
    "end_wb3": len(val_test_2.power)
}

# Split into segments
val_test_1_dict = {
    "work_bout_1": [val_test_1.power[0:val1_indices["end_wb1"]], val_test_1.cadence[0:val1_indices["end_wb1"]], val_test_1.heart_rate[0:val1_indices["end_wb1"]]],
    "recovery_1": [val_test_1.power[val1_indices["end_wb1"]:val1_indices["start_wb2"]], val_test_1.cadence[val1_indices["end_wb1"]:val1_indices["start_wb2"]], val_test_1.heart_rate[val1_indices["end_wb1"]:val1_indices["start_wb2"]]],
    "work_bout_2": [val_test_1.power[val1_indices["start_wb2"]:val1_indices["end_wb2"]], val_test_1.cadence[val1_indices["start_wb2"]:val1_indices["end_wb2"]], val_test_1.heart_rate[val1_indices["start_wb2"]:val1_indices["end_wb2"]]],
    "recovery_2": [val_test_1.power[val1_indices["end_wb2"]:val1_indices["start_wb3"]], val_test_1.cadence[val1_indices["end_wb2"]:val1_indices["start_wb3"]], val_test_1.heart_rate[val1_indices["end_wb2"]:val1_indices["start_wb3"]]],
    "work_bout_3": [val_test_1.power[val1_indices["start_wb3"]:val1_indices["end_wb3"]], val_test_1.cadence[val1_indices["start_wb3"]:val1_indices["end_wb3"]], val_test_1.heart_rate[val1_indices["start_wb3"]:val1_indices["end_wb3"]]]
}
val_test_2_dict = {
    "work_bout_1": [val_test_2.power[0:val2_indices["end_wb1"]], val_test_2.cadence[0:val2_indices["end_wb1"]], val_test_2.heart_rate[0:val2_indices["end_wb1"]]],
    "recovery_1": [val_test_2.power[val2_indices["end_wb1"]:val2_indices["start_wb2"]], val_test_2.cadence[val2_indices["end_wb1"]:val2_indices["start_wb2"]], val_test_2.heart_rate[val2_indices["end_wb1"]:val2_indices["start_wb2"]]],
    "work_bout_2": [val_test_2.power[val2_indices["start_wb2"]:val2_indices["end_wb2"]], val_test_2.cadence[val2_indices["start_wb2"]:val2_indices["end_wb2"]], val_test_2.heart_rate[val2_indices["start_wb2"]:val2_indices["end_wb2"]]],
    "recovery_2": [val_test_2.power[val2_indices["end_wb2"]:val2_indices["start_wb3"]], val_test_2.cadence[val2_indices["end_wb2"]:val2_indices["start_wb3"]], val_test_2.heart_rate[val2_indices["end_wb2"]:val2_indices["start_wb3"]]],
    "work_bout_3": [val_test_2.power[val2_indices["start_wb3"]:val2_indices["end_wb3"]], val_test_2.cadence[val2_indices["start_wb3"]:val2_indices["end_wb3"]], val_test_2.heart_rate[val2_indices["start_wb3"]:val2_indices["end_wb3"]]]
}

for elem in [val_test_1_dict, val_test_2_dict]:
    for key in elem:
        print(f"{key}: Average power = {round(np.mean(elem[key][0]))}, time = {len(elem[key][0])}, average cadence = {round(np.mean(elem[key][1]))}, HR change = {elem[key][2][-1]-elem[key][2][0]}, W' exp = {round(np.sum([power-cp for power in elem[key][0]]),1)}J")
    print('\n')

# Plot the power outputs
avg_power_val1 = len(val_test_1_dict["work_bout_1"][0])*[np.average(val_test_1_dict["work_bout_1"][0])] + len(val_test_1_dict["recovery_1"][0])*[np.average(val_test_1_dict["recovery_1"][0])] + len(val_test_1_dict["work_bout_2"][0])*[np.average(val_test_1_dict["work_bout_2"][0])]+ len(val_test_1_dict["recovery_2"][0])*[np.average(val_test_1_dict["recovery_2"][0])]+ len(val_test_1_dict["work_bout_3"][0])*[np.average(val_test_1_dict["work_bout_3"][0])]
compare_power([val_test_1.power, avg_power_val1, len(val_test_1.power)*[cp]], val_test_1.time, ['Power', 'Average power', f'CP: {cp}W'], 'Validation test 240s recovery')

avg_power_val2 = len(val_test_2_dict["work_bout_1"][0])*[np.average(val_test_2_dict["work_bout_1"][0])] + len(val_test_2_dict["recovery_1"][0])*[np.average(val_test_2_dict["recovery_1"][0])] + len(val_test_2_dict["work_bout_2"][0])*[np.average(val_test_2_dict["work_bout_2"][0])]+ len(val_test_2_dict["recovery_2"][0])*[np.average(val_test_2_dict["recovery_2"][0])]+ len(val_test_2_dict["work_bout_3"][0])*[np.average(val_test_2_dict["work_bout_3"][0])]
compare_power([val_test_2.power, avg_power_val2, len(val_test_2.power)*[cp]], val_test_2.time, ['Power', 'Average power', f'CP: {cp}W'], 'Validation test 30s recovery')

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
w_bal_int_reg_val1 = w_prime_balance_integral_regression(val1_power["power"], cp, w_prime, a=1362, b=-0.033, c=451)
w_bal_int_reg_val2 = w_prime_balance_integral_regression(val2_power["power"], cp, w_prime, a=1362, b=-0.033, c=451)
w_bal_ode_reg_val1 = w_prime_balance_ode_regression(val1_power["power"], cp, w_prime, d=765373, e=-1.847)
w_bal_ode_reg_val2 = w_prime_balance_ode_regression(val2_power["power"], cp, w_prime, d=765373, e=-1.847)
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
plt.ylim(-7000,30000)
plt.ylabel("W' bal [J]")
plt.xlabel("Time [s]")
plt.legend(['Bi-exp model'])

plt.subplot(2,1,2)
plt.plot(FC_bal_val1)
plt.plot(SC_bal_val1)
plt.legend(['FC balance', 'SC balance'])
plt.ylabel("W' bal [J]")
plt.xlabel("Time [s]")
plt.ylim(-7000,20000)
plt.subplots_adjust(hspace=0.7)
plt.show()

plt.subplot(2,1,1)
plt.title("Validation test with 30s recovery")
plt.plot(w_bal_biexp_val2)
plt.ylim(-7000,30000)
plt.ylabel("W' bal [J]")
plt.xlabel("Time [s]")
plt.legend(['Bi-exp model'])

plt.subplot(2,1,2)
plt.plot(FC_bal_val2)
plt.plot(SC_bal_val2)
plt.legend(['FC balance', 'SC balance'])
plt.ylabel("W' bal [J]")
plt.xlabel("Time [s]")
plt.ylim(-7000,20000)
plt.subplots_adjust(hspace=0.7)
plt.show()

# Plot predicted vs actual recovery
# Actual:
rec1_actual_val1 = np.sum([power-cp for power in val_test_1_dict["work_bout_2"][0]])
rec2_actual_val1 = np.sum([power-cp for power in val_test_1_dict["work_bout_3"][0]])
rec1_actual_val2 = np.sum([power-cp for power in val_test_2_dict["work_bout_2"][0]])
rec2_actual_val2 = np.sum([power-cp for power in val_test_2_dict["work_bout_3"][0]])

# Predicted by ODE algorithm
rec1_predicted_ode_val1 = w_bal_ode_val1[val1_indices["start_wb2"]]-w_bal_ode_val1[val1_indices["end_wb1"]]
rec2_predicted_ode_val1 = w_bal_ode_val1[val1_indices["start_wb3"]]-w_bal_ode_val1[val1_indices["end_wb2"]]

rec1_predicted_ode_val2 = w_bal_ode_val2[val2_indices["start_wb2"]]-w_bal_ode_val2[val2_indices["end_wb1"]]
rec2_predicted_ode_val2 = w_bal_ode_val2[val2_indices["start_wb3"]]-w_bal_ode_val2[val2_indices["end_wb2"]]

# Predicted by ODE algorithm with fittted tau
rec1_predicted_ode_reg_val1 = w_bal_ode_reg_val1[val1_indices["start_wb2"]]-w_bal_ode_reg_val1[val1_indices["end_wb1"]]
rec2_predicted_ode_reg_val1 = w_bal_ode_reg_val1[val1_indices["start_wb3"]]-w_bal_ode_reg_val1[val1_indices["end_wb2"]]

rec1_predicted_ode_reg_val2 = w_bal_ode_reg_val2[val2_indices["start_wb2"]]-w_bal_ode_reg_val2[val2_indices["end_wb1"]]
rec2_predicted_ode_reg_val2 = w_bal_ode_reg_val2[val2_indices["start_wb3"]]-w_bal_ode_reg_val2[val2_indices["end_wb2"]]

# Predicted by integral algorithm
rec1_predicted_int_reg_val1 = w_bal_int_reg_val1[val1_indices["start_wb2"]]-w_bal_int_reg_val1[val1_indices["end_wb1"]]
rec2_predicted_int_reg_val1 = w_bal_int_reg_val1[val1_indices["start_wb3"]]-w_bal_int_reg_val1[val1_indices["end_wb2"]]

rec1_predicted_int_reg_val2 = w_bal_int_reg_val2[val2_indices["start_wb2"]]-w_bal_int_reg_val2[val2_indices["end_wb1"]]
rec2_predicted_int_reg_val2 = w_bal_int_reg_val2[val2_indices["start_wb3"]]-w_bal_int_reg_val2[val2_indices["end_wb2"]]

# Predicted by integral algorithm with fitted tau
rec1_predicted_int_val1 = w_bal_int_val1[val1_indices["start_wb2"]]-w_bal_int_val1[val1_indices["end_wb1"]]
rec2_predicted_int_val1 = w_bal_int_val1[val1_indices["start_wb3"]]-w_bal_int_val1[val1_indices["end_wb2"]]

rec1_predicted_int_val2 = w_bal_int_val2[val2_indices["start_wb2"]]-w_bal_int_val2[val2_indices["end_wb1"]]
rec2_predicted_int_val2 = w_bal_int_val2[val2_indices["start_wb3"]]-w_bal_int_val2[val2_indices["end_wb2"]]

# Predicted by bartram algorithm
rec1_predicted_bartram_val1 = w_bal_bartram_val1[val1_indices["start_wb2"]]-w_bal_bartram_val1[val1_indices["end_wb1"]]
rec2_predicted_bartram_val1 = w_bal_bartram_val1[val1_indices["start_wb3"]]-w_bal_bartram_val1[val1_indices["end_wb2"]]

rec1_predicted_bartram_val2 = w_bal_bartram_val2[val2_indices["start_wb2"]]-w_bal_bartram_val2[val2_indices["end_wb1"]]
rec2_predicted_bartram_val2 = w_bal_bartram_val2[val2_indices["start_wb3"]]-w_bal_bartram_val2[val2_indices["end_wb2"]]

# Predicted by bi exp algorithm
rec1_predicted_biexp_val1 = w_bal_biexp_val1[val1_indices["start_wb2"]]-w_bal_biexp_val1[val1_indices["end_wb1"]]
rec2_predicted_biexp_val1 = w_bal_biexp_val1[val1_indices["start_wb3"]]-w_bal_biexp_val1[val1_indices["end_wb2"]]

rec1_predicted_biexp_val2 = w_bal_biexp_val2[val2_indices["start_wb2"]]-w_bal_biexp_val2[val2_indices["end_wb1"]]
rec2_predicted_biexp_val2 = w_bal_biexp_val2[val2_indices["start_wb3"]]-w_bal_biexp_val2[val2_indices["end_wb2"]]

actual_recs = [rec1_actual_val1, rec2_actual_val1, rec1_actual_val2, rec2_actual_val2]
predicted_ode_recs = [rec1_predicted_ode_val1, rec2_predicted_ode_val1, rec1_predicted_ode_val2, rec2_predicted_ode_val2]
predicted_ode_reg_recs = [rec1_predicted_ode_reg_val1, rec2_predicted_ode_reg_val1, rec1_predicted_ode_reg_val2, rec2_predicted_ode_reg_val2]
predicted_int_recs = [rec1_predicted_int_val1, rec2_predicted_int_val1, rec1_predicted_int_val2, rec2_predicted_int_val2]
predicted_int_reg_recs = [rec1_predicted_int_reg_val1, rec2_predicted_int_reg_val1, rec1_predicted_int_reg_val2, rec2_predicted_int_reg_val2]
predicted_bartram_recs = [rec1_predicted_bartram_val1, rec2_predicted_bartram_val1, rec1_predicted_bartram_val2, rec2_predicted_bartram_val2]
predicted_biexp_recs = [rec1_predicted_biexp_val1, rec2_predicted_biexp_val1, rec1_predicted_biexp_val2, rec2_predicted_biexp_val2]

width = 0.1
x = np.arange(4)
plt.bar(x-0.3, np.array(actual_recs)/w_prime*100, width)
plt.bar(x-0.2, np.array(predicted_ode_recs)/w_prime*100, width)
plt.bar(x-0.1, np.array(predicted_ode_reg_recs)/w_prime*100, width)
plt.bar(x, np.array(predicted_int_recs)/w_prime*100, width)
plt.bar(x+0.1, np.array(predicted_int_reg_recs)/w_prime*100, width)
plt.bar(x+0.2, np.array(predicted_bartram_recs)/w_prime*100, width)
plt.bar(x+0.3, np.array(predicted_biexp_recs)/w_prime*100, width)
plt.xticks(x, ['Recovery 1: 240s', 'Recovery 2: 240s', 'Recovery 1: 30s', 'Recovery 2: 30s'])
plt.legend(['Actual', 'ODE', 'ODE with fitted tau', 'Integral', 'Integral with fitted tau', 'Bartram', 'Bi-exponential'])
plt.ylabel("W' reconstitution (%)")
plt.title("W' reconstitution")
plt.show()