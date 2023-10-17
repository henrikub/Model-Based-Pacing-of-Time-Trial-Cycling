import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


power_test1 = 340
time_test1 = 200

power_test2 = 320
time_test2 = 400

power_test3 = 300
time_test3 = 600

power_test4 = 275
time_test4 = 1000

power = np.array([power_test1, power_test2, power_test3, power_test4])
time = np.array([time_test1, time_test2, time_test3, time_test4])

def linear_p(t, AWC, CP):
    return AWC*(1/t) + CP

def linear_tw(t, AWC, CP):
    return AWC + CP*t

def nonlinear_2(P, AWC, CP):
    return AWC/(P-CP)

def nonlinear_3(P, AWC, CP, P_max):
    return (AWC/(P-CP))-(AWC/(P_max-CP))

def exp_model(t, CP, P_max, tau):
    return CP + (P_max-CP)*np.exp(-t/tau)

def regression(function, power, time):
    if function == linear_p:
        initial_guess = (10000, 300)
        return curve_fit(linear_p, time, power, p0=initial_guess)

    if function == linear_tw:
        initial_guess = (10000, 300)
        return curve_fit(linear_tw, time, time*power, p0=initial_guess)
 
    if function == nonlinear_2:
        initial_guess = (10000, 300)
        return curve_fit(nonlinear_2, power, time, p0=initial_guess)

    if function == nonlinear_3:
        initial_guess = (10000, 300, 500)
        return curve_fit(nonlinear_3, power, time, p0=initial_guess)
    
    if function == exp_model:
        initial_guess = (300, 500, 1)
        return curve_fit(exp_model, time, power, p0=initial_guess)


params_linear_p, covariance_linear_p = regression(linear_p, power, time)
awc_linear_p, cp_linear_p = params_linear_p
print(f"AWC for {linear_p} is {round(awc_linear_p/1000, 2)}kJ")
print(f"CP for {linear_p} is {round(cp_linear_p, 2)}W")

params_linear_tw, covariance_linear_tw = regression(linear_tw, power, time)
awc_linear_tw, cp_linear_tw = params_linear_tw
print(f"AWC for {linear_tw} is {round(awc_linear_tw/1000, 2)}kJ")
print(f"CP for {linear_tw} is {round(cp_linear_tw, 2)}W")

params_nl2, covariance_linear_tw = regression(nonlinear_2, power, time)
awc_nl2, cp_nl2 = params_nl2
print(f"AWC for {nonlinear_2} is {round(awc_nl2/1000, 2)}kJ")
print(f"CP for {nonlinear_2} is {round(cp_nl2, 2)}W")

params_nl3, covariance_nl3 = regression(nonlinear_3, power, time)
awc_nl3, cp_nl3, p_max_nl3 = params_nl3
print(f"AWC for {nonlinear_3} is {round(awc_nl3/1000, 2)}kJ")
print(f"CP for {nonlinear_3} is {round(cp_nl3, 2)}W")
print(f"P_max for {nonlinear_3} is {round(p_max_nl3, 2)}W")

params_exp, covariance_exp = regression(exp_model, power, time)
cp_exp, p_max_exp, tau_exp = params_exp
print(f"CP for {exp_model} is {round(cp_exp, 2)}W")
print(f"P_max for {exp_model} is {round(p_max_exp, 2)}W")
print(f"Tau for {exp_model} is {round(tau_exp, 2)}")

fitted_linear_p = linear_p(np.arange(30,2000), awc_linear_p, cp_linear_p)
plt.plot(fitted_linear_p, np.arange(30,2000))
plt.plot(power_test1,time_test1, marker="o", markersize=10, markeredgecolor="red", markerfacecolor="red")
plt.plot(power_test2, time_test2, marker="o", markersize=10, markeredgecolor="red", markerfacecolor="red")
plt.plot(power_test3, time_test3, marker="o", markersize=10, markeredgecolor="red", markerfacecolor="red")
plt.plot(power_test4, time_test4, marker="o", markersize=10, markeredgecolor="red", markerfacecolor="red")

plt.show()
