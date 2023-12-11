import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
from w_bal import *
import matplotlib.pyplot as plt
from activity_reader import *

val1 = ActivityReader("Validation_test_240s_rec.tcx")
val1.remove_unactive_period(900)

val2 = ActivityReader("Validation_test_30s_rec.tcx")
val2.remove_unactive_period(400)

cp = 265
w_prime = 26630

def w_prime_balance_bi_exp_regression(power, cp, w_prime, fc, sc, tau_fc, tau_sc):

    w_prime_balance = []
    FC_balance = []
    SC_balance = []
    FC_amp = 0.3679*w_prime
    SC_amp = 0.6324*w_prime    

    for t in range(len(power)):
        w_prime_exp_sum = 0
        FC_exp_sum = 0
        SC_exp_sum = 0

        for u, p in enumerate(power[: t + 1]):
            w_prime_exp = max(0, p - cp)
            FC_exp_sum += w_prime_exp * (fc * np.power(np.e, (u - t) / tau_fc))
            SC_exp_sum += w_prime_exp * (sc * np.power(np.e, (u - t) / tau_sc))
        
        w_prime_exp_sum = FC_exp_sum + SC_exp_sum
        w_prime_balance.append(w_prime - w_prime_exp_sum)
        FC_balance.append(FC_amp-FC_exp_sum)
        SC_balance.append(SC_amp-SC_exp_sum)

    return w_prime_balance, FC_balance, SC_balance

def regression_bi_exp(power, fc, sc, tau_fc, tau_sc):
    cp = 265
    w_prime = 26630
    return w_prime_balance_bi_exp_regression(power, cp, w_prime, fc, sc, tau_fc, tau_sc)[0]


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

def regression_mono_exp(power, a, b, c):
    cp = 265
    w_prime = 26630
    return w_bal_integral_regression(power, cp, w_prime, a, b, c)


# validation test 1
time_data_val1 = [0, 248, 488, 602, 846, 948]
w_bal_data_val1 = [26630, 1500, 11118, 1500, 10596, 1500]

w_bal_interpolated_val1 = np.interp(val1.time, time_data_val1, w_bal_data_val1)
power_data_val1 = pd.DataFrame(dict(power=val1.power), index=val1.time)

# validation test 2
time_data_val2 = [0, 282, 319, 388, 423, 481]
w_bal_data_val2 = [26630, 1500, 7918, 1500, 7385, 1500]

w_bal_interpolated_val2 = np.interp(val2.time, time_data_val2, w_bal_data_val2)
power_data_val2 = pd.DataFrame(dict(power=val2.power), index=val2.time)

# Mono-exponential regression
#ppot, pcov = curve_fit(regression_mono_exp, np.concatenate([power_data_val1["power"], power_data_val2["power"]]), np.concatenate([w_bal_interpolated_val1, w_bal_interpolated_val2]), p0=[546, -0.01, 316])
# ppot, pcov = curve_fit(regression_mono_exp, power_data_val2["power"], w_bal_interpolated_val2, p0=[546, -0.01, 316])
# a,b,c = ppot
# print(a, b, c)

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


# Bi-exponential regression
ppot, pcov = curve_fit(regression_bi_exp, np.concatenate([power_data_val1["power"], power_data_val2["power"]]), np.concatenate([w_bal_interpolated_val1, w_bal_interpolated_val2]), p0 = [4.4,0.9,25,640], bounds = ([0.2,0.2,6,100],[10,10,100,5000]))
#ppot, pcov = curve_fit(regression_bi_exp, power_data_val2["power"], w_bal_interpolated_val2, p0 = [4.4,0.9,25,640], bounds = ([0.5,0.5,6,100],[10,10,100,5000]))

fc, sc, taufc, tausc = ppot
print(fc, sc, taufc, tausc)

w_bal_bi_exp_val1, fc_bal_val1, sc_bal_val1 = w_prime_balance_bi_exp_regression(power_data_val1["power"], cp, w_prime, fc, sc, taufc, tausc)
w_bal_bi_exp_val2, fc_bal_val2, sc_bal_val2 = w_prime_balance_bi_exp_regression(power_data_val2["power"], cp, w_prime, fc, sc, taufc, tausc)
plt.subplot(2,1,1)
plt.plot(w_bal_bi_exp_val1)
plt.plot(w_bal_interpolated_val1)
plt.legend(["Fitted w'bal", "W bal interpolated"])

plt.subplot(2,1,2)
plt.plot(w_bal_bi_exp_val2)
plt.plot(w_bal_interpolated_val2)
plt.legend(["Fitted w'bal", "W bal interpolated"])
plt.show()




