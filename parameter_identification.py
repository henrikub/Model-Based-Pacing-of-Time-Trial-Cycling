import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
from scipy.interpolate import CubicSpline
from w_bal import *
import matplotlib.pyplot as plt
from activity_reader import *

val1 = ActivityReader("Validation_test_240s_rec.tcx")
val1.remove_unactive_period(900)

val2 = ActivityReader("Validation_test_30s_rec.tcx")
val2.remove_unactive_period(400)

# Remove the incorrect values where the power is zero
for i in range(10,len(val1.power)):
    if val1.power[i] == 0:
        val1.power[i] = val1.power[i+1]


for i in range(10,len(val2.power)):
    if val2.power[i] == 0:
        val2.power[i] = val2.power[i+1]

cp = 265
w_prime = 26630

def w_prime_balance_bi_exp_regression(power, cp, w_prime, fc, sc):

    w_prime_balance = []
    FC_balance = []
    SC_balance = []
    FC_amp = 0.3679*w_prime
    SC_amp = 0.6324*w_prime
    tau_fc = get_bi_exp_tau_method(power, cp, True, None, fast_component=True)
    tau_sc = get_bi_exp_tau_method(power, cp, True, None, fast_component=False)

    for t in range(len(power)):
        w_prime_exp_sum = 0
        FC_exp_sum = 0
        SC_exp_sum = 0

        for u, p in enumerate(power[: t + 1]):
            w_prime_exp = max(0, p - cp)
            FC_exp_sum += w_prime_exp * (fc * np.power(np.e, (u - t) / tau_fc(t)))
            SC_exp_sum += w_prime_exp * (sc * np.power(np.e, (u - t) / tau_sc(t)))
        
        w_prime_exp_sum = FC_exp_sum + SC_exp_sum
        w_prime_balance.append(w_prime - w_prime_exp_sum)
        FC_balance.append(FC_amp-FC_exp_sum)
        SC_balance.append(SC_amp-SC_exp_sum)

    return w_prime_balance, FC_balance, SC_balance

def regression_bi_exp(power, fc, sc):
    cp = 265
    w_prime = 26630
    return w_prime_balance_bi_exp_regression(power, cp, w_prime, fc, sc)[0]


def tau_regression(power, cp, a, b, c, untill=None):
    if untill is None:
        untill = len(power)

    avg_power_below_cp = power[:untill][power[:untill] < cp].mean()
    if math.isnan(avg_power_below_cp):
        avg_power_below_cp = 0
    delta_cp = cp - avg_power_below_cp

    return a * math.e ** (b * delta_cp) + c

def w_bal_integral_regression(power, cp, w_prime, a, b, c):
    w_prime_balance = []
    tau_dyn = [tau_regression(power, cp, a, b, c) for i in range(len(power))]
    tau = lambda t: tau_dyn[t]

    for t in range(len(power)):
        w_prime_exp_sum = 0

        for u, p in enumerate(power[: t + 1]):
            w_prime_exp = max(0, p - cp)
            w_prime_exp_sum += w_prime_exp * np.power(np.e, (u - t) / tau(t))

        w_prime_balance.append(w_prime - w_prime_exp_sum)

    return w_prime_balance

def w_bal_ode_regression(power, cp, w_prime, a, b):
    last = w_prime
    w_prime_balance = []

    for p in power:
        if p < cp:
            new = w_prime - (w_prime - last) * np.power(np.e, -1/(a*(cp-p)**b))
        else:
            new = last - (p - cp)

        w_prime_balance.append(new)
        last = new
    return w_prime_balance

def regression_mono_exp(power, a, b, c):
    cp = 265
    w_prime = 26630
    return w_bal_integral_regression(power, cp, w_prime, a, b, c)

def regression_ode(power, a, b):
    cp = 265
    w_prime = 26630
    return w_bal_ode_regression(power, cp, w_prime, a, b)


# validation test 1
time_data_val1 = [0, 248, 488, 602, 846, 948]
w_bal_data_val1 = [26630, 1500, 11118, 1500, 10596, 1500]

w_bal_interpolated_val1 = np.interp(val1.time, time_data_val1, w_bal_data_val1)
power_data_val1 = pd.DataFrame(dict(power=val1.power), index=val1.time)

# cs = CubicSpline(time_data_val1, w_bal_data_val1)
# w_bal_interpolated_val1 = cs(val1.time)

# validation test 2
time_data_val2 = [0, 282, 319, 388, 423, 481]
w_bal_data_val2 = [26630, 1500, 7918, 1500, 7385, 1500]

w_bal_interpolated_val2 = np.interp(val2.time, time_data_val2, w_bal_data_val2)
power_data_val2 = pd.DataFrame(dict(power=val2.power), index=val2.time)

time_data_combined = [0, 248, 488, 602, 846, 948, 986, 1056, 1092, 1153]
w_bal_data_combined = [26630, 1500, 11118, 1500, 10596, 1500, 7918, 1500, 7385, 1500]
power_combined = val1.power + val2.power[283:]
power_data_combined = pd.DataFrame(dict(power=power_combined), index=np.arange(len(power_combined)))
w_bal_interpolated_combined = np.interp(np.arange(len(power_data_combined)), time_data_combined, w_bal_data_combined)
# print(len(power_combined))
# plt.plot(power_combined)
# plt.show()

# cs = CubicSpline(time_data_val2, w_bal_data_val2)
# w_bal_interpolated_val2 = cs(val2.time)

# Mono-exponential regression
#ppot, pcov = curve_fit(regression_mono_exp, np.concatenate([power_data_val1["power"], power_data_val2["power"]]), np.concatenate([w_bal_interpolated_val1, w_bal_interpolated_val2]), p0=[546, -0.01, 316])
#ppot, pcov = curve_fit(regression_mono_exp, power_data_val1["power"], w_bal_interpolated_val1, p0=[546, -0.01, 316], bounds= ([0,-10,0], [10000,0,1000000]))
#ppot, pcov = curve_fit(regression_mono_exp, power_data_combined["power"], w_bal_interpolated_combined, p0=[546, -0.01, 316])
# a,b,c = ppot
# print(a, b, c)

# average between val 1 and val 2: a=978, b= -0.0163, c=419
# a=978
# b= -0.0163
# c=419

# w_bal_mono_exp_val1 = w_bal_integral_regression(power_data_val1["power"], cp, w_prime, a, b, c)
# w_bal_mono_exp_val2 = w_bal_integral_regression(power_data_val2["power"], cp, w_prime, a, b, c)
# plt.subplot(2,1,1)
# plt.plot(w_bal_mono_exp_val1)
# plt.plot(w_bal_interpolated_val1)
# plt.legend(["Fitted w'bal", "W bal interpolated"])

# plt.subplot(2,1,2)
# plt.plot(w_bal_mono_exp_val2)
# plt.plot(w_bal_interpolated_val2)
# plt.legend(["Fitted w'bal", "W bal interpolated"])
# plt.show()

# ODE regression
#ppot, pcov = curve_fit(regression_ode, power_data_val2["power"], w_bal_interpolated_val2, p0=[2287.2, -0.688], bounds=([0,-5],[5000,-0.01]))
#ppot, pcov = curve_fit(regression_ode, np.concatenate([power_data_val1["power"], power_data_val2["power"]]), np.concatenate([w_bal_interpolated_val1, w_bal_interpolated_val2]), p0=[2287.2, -0.688], bounds=([0,-5],[1000000000,-0.01]))
# a,b = ppot
# print(a, b)

# w_bal_ode_val1 = w_bal_ode_regression(power_data_val1["power"], cp, w_prime, a, b)
# w_bal_ode_val2 = w_bal_ode_regression(power_data_val2["power"], cp, w_prime, a, b)
# w_bal_bartram_val1 = w_prime_balance_bart(power_data_val1["power"], cp, w_prime)
# w_bal_bartram_val2 = w_prime_balance_bart(power_data_val2["power"], cp, w_prime)
# plt.subplot(2,1,1)
# plt.plot(w_bal_ode_val1)
# plt.plot(w_bal_interpolated_val1)
# plt.plot(w_bal_bartram_val1)
# plt.legend(["Fitted w'bal", "W'bal interpolated", "W'bal bartram"])

# plt.subplot(2,1,2)
# plt.plot(w_bal_ode_val2)
# plt.plot(w_bal_interpolated_val2)
# plt.plot(w_bal_bartram_val2)
# plt.legend(["Fitted w'bal", "W'bal interpolated", "W'bal bartram"])
# plt.show()

# Bi-exponential regression
# ppot, pcov = curve_fit(regression_bi_exp, np.concatenate([power_data_val1["power"], power_data_val2["power"]]), np.concatenate([w_bal_interpolated_val1, w_bal_interpolated_val2]), p0 = [4.4,0.9,25,640], bounds = ([0.2,0.2,6,100],[10,10,100,5000]))
# ppot, pcov = curve_fit(regression_bi_exp, power_data_val1["power"], w_bal_interpolated_val1, p0 = [4.4,0.9,25,640], bounds = ([0.5,0.5,6,100],[10,10,100,5000]))
ppot, pcov = curve_fit(regression_bi_exp, power_data_combined["power"], w_bal_interpolated_combined, p0 = [4.4,0.9], bounds = ([0,0.89],[10,0.9]))

fc, sc = ppot
print(fc, sc)

w_bal_combined, fc_bal_combined, sc_bal_combined = w_prime_balance_bi_exp_regression(power_data_combined["power"], cp, w_prime, fc, sc)
w_bal_bi_exp_val1, fc_bal_val1, sc_bal_val1 = w_prime_balance_bi_exp_regression(power_data_val1["power"], cp, w_prime, fc, sc)
w_bal_bi_exp_val2, fc_bal_val2, sc_bal_val2 = w_prime_balance_bi_exp_regression(power_data_val2["power"], cp, w_prime, fc, sc)
plt.subplot(3,1,1)
plt.plot(w_bal_bi_exp_val1)
plt.plot(w_bal_interpolated_val1)
plt.legend(["Fitted w'bal", "W bal interpolated"])

plt.subplot(3,1,2)
plt.plot(fc_bal_val1)
plt.plot(sc_bal_val1)
plt.legend(["FC bal", "SC bal"])

plt.subplot(3,1,3)
plt.plot(w_bal_combined)
plt.show()

plt.subplot(2,1,1)
plt.plot(w_bal_bi_exp_val2)
plt.plot(w_bal_interpolated_val2)
plt.legend(["Fitted w'bal", "W bal interpolated"])

plt.subplot(2,1,2)
plt.plot(fc_bal_val2)
plt.plot(sc_bal_val2)
plt.legend(["FC bal", "SC bal"])
plt.show()
