from activity_reader import ActivityReader
import numpy as np
from regression import *
from plotting import plot_regression

# Read the constant power tests
test1_activity = ActivityReader("300W_test.tcx")
test2_activity = ActivityReader("350W_test.tcx")
test3_activity = ActivityReader("400W_test.tcx")
test4_activity = ActivityReader("290W_test.tcx")

activities = [test1_activity, test2_activity, test3_activity, test4_activity]

# Remove the unactive periods from the end of the tests
test1_activity.remove_unactive_period(600)
test2_activity.remove_unactive_period(200)
test3_activity.remove_unactive_period(100)
test4_activity.remove_unactive_period(800)

# Print some statistics from each test
for i, act in enumerate(activities):
    act.avg_power = round(np.average(act.power))
    act.total_time = act.time[-1]
    print(f"Statistics for test {i+1}:")
    print(f"Average power is {act.avg_power}W")
    print(f"Average cadence is {round(np.average(act.cadence))}rpm")
    print(f"Max heartrate is {np.max(act.heart_rate)}bpm")
    print(f"Total time is {act.total_time}\n")
    
# Perform regression
power_points = np.array([int(test1_activity.avg_power), int(test2_activity.avg_power), int(test3_activity.avg_power), int(test4_activity.avg_power)])
time_points = np.array([int(test1_activity.total_time), int(test2_activity.total_time), int(test3_activity.total_time), int(test4_activity.total_time)])

params_linear_p, covariance_linear_p = regression(linear_p, power_points, time_points)
awc_linear_p, cp_linear_p = params_linear_p
print(f"Parameters for Linear-P model: AWC = {round(awc_linear_p/1000,2)}kJ, CP = {round(cp_linear_p)}W")

params_linear_tw, covariance_linear_tw = regression(linear_tw, power_points, time_points)
awc_linear_tw, cp_linear_tw = params_linear_tw
print(f"Parameters for Linear-TW model: AWC = {round(awc_linear_tw/1000,2)}kJ, CP = {round(cp_linear_tw)}W")

params_nl2, covariance_linear_tw = regression(nonlinear_2, power_points, time_points)
awc_nl2, cp_nl2 = params_nl2
print(f"Parameters for Nonlinear-2 model: AWC = {round(awc_nl2/1000,2)}kJ, CP = {round(cp_nl2)}W")

params_nl3, covariance_nl3 = regression(nonlinear_3, power_points, time_points)
awc_nl3, cp_nl3, p_max_nl3 = params_nl3
print(f"Parameters for Nonlinear-3 model: AWC = {round(awc_nl3/1000,2)}kJ, CP = {round(cp_nl3)}W, P_max = {round(p_max_nl3)}")

params_exp, covariance_exp = regression(exp_model, power_points, time_points)
cp_exp, p_max_exp, tau_exp = params_exp
print(f"Parameters for Exp model: CP = {round(cp_exp)}W, P_max = {round(p_max_exp)}, tau = {round(tau_exp,4)}")

params_nl4, covariance_nl4 = regression(nonlinear_4, power_points, time_points)
awc_nl4, cp_nl4, p_max_nl4, tau_nl4 = params_nl4
print(f"Parameters for Nonlinear-4 model: AWC = {round(awc_nl4/1000,2)}kJ, CP = {round(cp_nl4)}W, P_max = {round(p_max_nl3)}, tau = {round(tau_nl4,4)}\n")

# Create the fitted models
time = np.arange(1,1200)
power = np.arange(0,500)
fitted_linear_p = linear_p(time, awc_linear_p, cp_linear_p)
fitted_linear_tw = linear_tw(time, awc_linear_tw, cp_linear_tw)
fitted_nl2 = nonlinear_2(power, awc_nl2, cp_nl2)
fitted_nl3 = nonlinear_3(power, awc_nl3, cp_nl3, p_max_nl3)
fitted_exp = exp_model(time, cp_exp, p_max_exp, tau_exp)
fitted_nl4 = nonlinear_4(power, awc_nl4, cp_nl4, p_max_nl4, tau_nl4)

# Plot the fitted models and calculate R-squared
plot_regression(power_points, time_points, fitted_linear_tw, fitted_linear_p, fitted_nl2, fitted_nl3, fitted_exp, fitted_nl4)

r_squared_ltw = r_squared(power_points*time_points, time_points, fitted_linear_tw)
r_squared_lp = r_squared(power_points, time_points, fitted_linear_p)
r_squared_nl2 = r_squared(time_points, power_points, fitted_nl2)
r_squared_nl3 = r_squared(time_points, power_points, fitted_nl3)
r_squared_exp = r_squared(power_points, time_points, fitted_exp)
r_squared_nl4 = r_squared(time_points, power_points, fitted_nl4)

print(f"R-squared for the Linear-TW model is {round(r_squared_ltw,3)}")
print(f"R-squared for the Linear-P model is {round(r_squared_lp,3)}")
print(f"R-squared for the Nonlinear-2 model is {round(r_squared_nl2,3)}")
print(f"R-squared for the Nonlinear-3 model is {round(r_squared_nl3,3)}")
print(f"R-squared for the Exp model is {round(r_squared_exp,3)}")
print(f"R-squared for the Nonlinear-4 model is {round(r_squared_nl4,3)}\n")
