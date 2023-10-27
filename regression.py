import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


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
        return curve_fit(linear_p, time, power, p0=initial_guess, bounds=(0,[50000,1000]))

    if function == linear_tw:
        initial_guess = (10000, 300)
        return curve_fit(linear_tw, time, time*power, p0=initial_guess, bounds=(0, [50000, 1000]))
 
    if function == nonlinear_2:
        initial_guess = (10000, 300)
        return curve_fit(nonlinear_2, power, time)

    if function == nonlinear_3:
        initial_guess = (20000, 300, 500)
        return curve_fit(nonlinear_3, power, time, p0=initial_guess, bounds=(0, [40000, 500, 1000]))
    
    if function == exp_model:
        initial_guess = (300, 500, 1)
        return curve_fit(exp_model, time, power, p0=initial_guess, bounds=(0, [1000, 2000, 10]))

power_test1 = 417
time_test1 = 180

power_test2 = 345
time_test2 = 340

power_test3 = 298
time_test3 = 776

power_test4 = 285
time_test4 = 1200

data_points = [
    (power_test1, time_test1),
    (power_test2, time_test2),
    (power_test3, time_test3),
    (power_test4, time_test4)
]

power_points = np.array([power_test1, power_test2, power_test3, power_test4])
time_points = np.array([time_test1, time_test2, time_test3, time_test4])

params_linear_p, covariance_linear_p = regression(linear_p, power_points, time_points)
awc_linear_p, cp_linear_p = params_linear_p
print(f"AWC for {linear_p} is {round(awc_linear_p/1000, 2)}kJ")
print(f"CP for {linear_p} is {round(cp_linear_p, 2)}W")

params_linear_tw, covariance_linear_tw = regression(linear_tw, power_points, time_points)
awc_linear_tw, cp_linear_tw = params_linear_tw
print(f"AWC for {linear_tw} is {round(awc_linear_tw/1000, 2)}kJ")
print(f"CP for {linear_tw} is {round(cp_linear_tw, 2)}W")

params_nl2, covariance_linear_tw = regression(nonlinear_2, power_points, time_points)
awc_nl2, cp_nl2 = params_nl2
print(f"AWC for {nonlinear_2} is {round(awc_nl2/1000, 2)}kJ")
print(f"CP for {nonlinear_2} is {round(cp_nl2, 2)}W")

params_nl3, covariance_nl3 = regression(nonlinear_3, power_points, time_points)
awc_nl3, cp_nl3, p_max_nl3 = params_nl3
print(f"AWC for {nonlinear_3} is {round(awc_nl3/1000, 2)}kJ")
print(f"CP for {nonlinear_3} is {round(cp_nl3, 2)}W")
print(f"P_max for {nonlinear_3} is {round(p_max_nl3, 2)}W")

params_exp, covariance_exp = regression(exp_model, power_points, time_points)
cp_exp, p_max_exp, tau_exp = params_exp
print(f"CP for {exp_model} is {round(cp_exp, 2)}W")
print(f"P_max for {exp_model} is {round(p_max_exp, 2)}W")
print(f"Tau for {exp_model} is {round(tau_exp, 2)}")

time = np.arange(1,1200)
power = np.arange(0,500)
fitted_linear_p = linear_p(time, awc_linear_p, cp_linear_p)
fitted_linear_tw = linear_tw(time, awc_linear_tw, cp_linear_tw)
fitted_nl2 = nonlinear_2(power, awc_nl2, cp_nl2)
fitted_nl3 = nonlinear_3(power, awc_nl3, cp_nl3, p_max_nl3)
fitted_exp = exp_model(time, cp_exp, p_max_exp, tau_exp)

plt.subplot(3, 2 ,1)
plt.plot(1/time, fitted_linear_p)
plt.title("Linear-P")
plt.xlabel("1/time [1/s]")
plt.ylabel("Power [W]")
text_lp = f'CP = {round(cp_linear_p)}W\nAWC = {round(awc_linear_p/1000,2)}kJ'
plt.text(0.8, 0.5, text_lp, ha='center', va='center', transform=plt.gca().transAxes)
for p, t in data_points:
    plt.plot(1/t, p, marker="o", markersize=10, markeredgecolor="red", markerfacecolor="red")
plt.xlim(0, 0.007)
plt.ylim(0, 550)

plt.subplot(3,2,2)
plt.plot(time, fitted_linear_tw)
plt.title("Linear-TW")
plt.xlabel("Time [s]")
plt.ylabel("Total work [J]")
text_ltw = f'CP = {round(cp_linear_tw)}W\nAWC = {round(awc_linear_tw/1000,2)}kJ'
plt.text(0.8, 0.5, text_ltw, ha='center', va='center', transform=plt.gca().transAxes)
for p, t in data_points:
    plt.plot(t, p*t, marker="o", markersize=10, markeredgecolor="red", markerfacecolor="red")
plt.xlim(0,1000)
plt.ylim(0,300000)

plt.subplot(3,2,3)
plt.plot(power, fitted_nl2)
plt.title("Nonlinear-2")
plt.xlabel("Power [W]")
plt.ylabel("Time [s]")
text_nl2 = f'CP = {round(cp_nl2)}W\nAWC = {round(awc_nl2/1000,2)}kJ'
plt.text(0.8, 0.5, text_nl2, ha='center', va='center', transform=plt.gca().transAxes)
for p, t in data_points:
    plt.plot(p, t, marker="o", markersize=10, markeredgecolor="red", markerfacecolor="red")
plt.xlim(270,500)
plt.ylim(0,1200)

plt.subplot(3,2,4)
plt.plot(power, fitted_nl3)
plt.title("Nonlinear-3")
plt.xlabel("Power [W]")
plt.ylabel("Time [s]")
text_nl3 = f'CP = {round(cp_nl3)}W\nAWC = {round(awc_nl3/1000,2)}kJ\nP_max = {round(p_max_nl3)}W'
plt.text(0.8, 0.5, text_nl3, ha='center', va='center', transform=plt.gca().transAxes)
for p, t in data_points:
    plt.plot(p, t, marker="o", markersize=10, markeredgecolor="red", markerfacecolor="red")
plt.xlim(270,500)
plt.ylim(0,1200)

plt.subplot(3,2,5)
plt.plot(power, fitted_nl3)
plt.title("Exp model")
plt.xlabel("Power [W]")
plt.ylabel("Time [s]")
text_exp = f'CP = {round(cp_exp)}W\ntau = {tau_exp}\nP_max = {round(p_max_exp)}W'
plt.text(0.8, 0.5, text_exp, ha='center', va='center', transform=plt.gca().transAxes)
for p, t in data_points:
    plt.plot(p, t, marker="o", markersize=10, markeredgecolor="red", markerfacecolor="red")
plt.xlim(270,500)
plt.ylim(0,1200)

plt.show()
