import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def linear_p(t, AWC, CP):
    return AWC*(1/t) + CP

def linear_tw(t, AWC, CP):
    return AWC + CP*t

def nonlinear_2(P, AWC, CP):
    return AWC/(P-CP)


power_test1 = 275
time_test1 = 4000

power_test2 = 300
time_test2 = 1000

power_test3 = 325
time_test3 = 700

power_test4 = 350
time_test4 = 300

power = np.array([power_test1, power_test2, power_test3, power_test4])
time = np.array([time_test1, time_test2, time_test3, time_test4])

def regression(function, power, time):
    if function == linear_p:
        params, covariance = curve_fit(linear_p, time, power)

    if function == linear_tw:
        params, covariance = curve_fit(linear_tw, time, time*power)
 
    if function == nonlinear_2:
        params, covariance = curve_fit(nonlinear_2, power, time)

    AWC, CP = params
    return AWC, CP, covariance

awc_linear_p, cp_linear_p, covariance_linear_p = regression(linear_p, power, time)
print(f"AWC for {linear_p} is {round(awc_linear_p/1000, 2)}kJ")
print(f"CP for {linear_p} is {round(cp_linear_p, 2)}W")

awc_linear_tw, cp_linear_tw, covariance_linear_tw = regression(linear_tw, power, time)
print(f"AWC for {linear_tw} is {round(awc_linear_tw/1000, 2)}kJ")
print(f"CP for {linear_tw} is {round(cp_linear_tw, 2)}W")

awc_linear_nl2, cp_linear_nl2, covariance_linear_tw = regression(nonlinear_2, power, time)
print(f"AWC for {nonlinear_2} is {round(awc_linear_nl2/1000, 2)}kJ")
print(f"CP for {nonlinear_2} is {round(cp_linear_nl2, 2)}W")

fitted_linear_p = linear_p(np.arange(30,15000), awc_linear_p, cp_linear_p)
plt.plot(fitted_linear_p)
plt.plot(time_test1, power_test1,marker="o", markersize=10, markeredgecolor="red", markerfacecolor="red")
plt.plot(time_test2, power_test2,marker="o", markersize=10, markeredgecolor="red", markerfacecolor="red")
plt.plot(time_test3, power_test3,marker="o", markersize=10, markeredgecolor="red", markerfacecolor="red")
plt.plot(time_test4, power_test4,marker="o", markersize=10, markeredgecolor="red", markerfacecolor="red")

plt.show()

y_vals = []