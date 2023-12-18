import numpy as np
import pandas as pd

from scipy.optimize import curve_fit
from w_bal import *
from activity_reader import *

val1 = ActivityReader("Validation_test_240s_rec.tcx")
val1.remove_unactive_period(900)

val2 = ActivityReader("Validation_test_30s_rec.tcx")
val2.remove_unactive_period(400)

cp = 265
w_prime = 26630

# Remove the incorrect values where the power is zero
for i in range(10,len(val1.power)):
    if val1.power[i] == 0:
        val1.power[i] = val1.power[i+1]


for i in range(10,len(val2.power)):
    if val2.power[i] == 0:
        val2.power[i] = val2.power[i+1]

def regression_mono_exp(power, a, b, c):
    cp = 265
    w_prime = 26630
    return w_prime_balance_integral_regression(power, cp, w_prime, a, b, c)

def regression_ode(power, d, e):
    cp = 265
    w_prime = 26630
    return w_prime_balance_ode_regression(power, cp, w_prime, d, e)

def regression_bi_exp(power, fc, sc):
    cp = 265
    w_prime = 26630
    return w_prime_balance_bi_exp_regression(power, cp, w_prime, fc, sc)[0]


time_data_combined = [0, 248, 488, 602, 846, 948, 986, 1056, 1092, 1153]
w_bal_data_combined = [26630, 1500, 1500+11118, 1500, 1500+10596, 1500, 1500+6413, 1500, 1500+5889, 1500]
power_combined = val1.power + val2.power[283:]
power_data_combined = pd.DataFrame(dict(power=power_combined), index=np.arange(len(power_combined)))
w_bal_interpolated_combined = np.interp(np.arange(len(power_data_combined)), time_data_combined, w_bal_data_combined)


# Mono-exponential regression
ppot, pcov = curve_fit(regression_mono_exp, power_data_combined["power"], w_bal_interpolated_combined, p0=[546, -0.01, 316])
a,b,c = ppot
print("Estimated parameters for the mono-exponential model: ", a, b, c)


# ODE bartram tau regression
ppot, pcov = curve_fit(regression_ode, power_data_combined["power"], w_bal_interpolated_combined, p0=[2287.2, -0.688])
d,e = ppot
print("Estimated parameters for the ODE model: ", d, e)


# Bi-exponential regression
ppot, pcov = curve_fit(regression_bi_exp, power_data_combined["power"], w_bal_interpolated_combined, bounds = ([4.4,0],[4.4001,100]))
fc, sc = ppot
print("Estimated parameters for the bi-exponential model: ", fc, sc)