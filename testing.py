import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from plotting import *
from activity_reader import ActivityReader
from w_bal import *
from scipy.optimize import curve_fit


cp = 265
w_prime = 26630

act = ActivityReader("Validation_test_240s_rec.tcx")
act.remove_unactive_period(800)

# test_power = 50*[300] + 50*[290] + 200*[320] + 100*[240]
# test_time = np.arange(0,400,1)

# data = pd.DataFrame(dict(power=test_power), index=test_time)

# w_bal_bi_exp, FC_bal, SC_bal = w_prime_balance_bi_exp(data["power"], cp, w_prime)

# plt.subplot(2,1,1)
# plt.plot(w_bal_bi_exp)

# plt.subplot(2,1,2)
# plt.plot(FC_bal)
# plt.plot(SC_bal)
# plt.legend(['FC bal', 'SC bal'])
# plt.show()

# power_profile = 240*[350] + 30*[225] + 120*[350] + 30*[225]+ 100*[350]
# plt.plot(power_profile)
# plt.plot(len(power_profile)*[cp])
# plt.xlabel('Time [s]')
# plt.ylabel('Power [W]')
# plt.legend(['Target power', 'CP'])
# plt.ylim((0,400))
# plt.show()


def f(x_data, a, b, c):
    cp = 265
    w_prime = 26630
    w_prime_balance = []
    data = pd.DataFrame(dict(power=act.power), index=act.time)
    power = data["power"]

    for t in range(len(x_data)):
        w_prime_exp_sum = 0

        for u, p in enumerate(power[: t + 1]):
            avg_power_below_cp = power[:t][power[:t] < cp].mean()
            if math.isnan(avg_power_below_cp):
                avg_power_below_cp = 0
            delta_cp = cp - avg_power_below_cp
            tau = a * math.e ** (b * delta_cp) + c
            w_prime_exp = max(0, p - cp)
            w_prime_exp_sum += w_prime_exp * np.power(np.e, (u - t) / tau)

        w_prime_balance.append(w_prime - w_prime_exp_sum)

    return w_prime_balance


x_data = [0, 248, 488, 602, 846, 949]
y_data = [cp, 1500, 11118, 1500, 10596, 1500]
ppot, pcov = curve_fit(f, x_data, y_data, p0=(546, -0.01, 316), bounds=([1, -10, 1],[1000, -0.00001, 1000]))
a, b, c = ppot
print(a,b,c)

w_prime_fitted_tau = f(x_data, a, b, c)
plt.plot(x_data, w_prime_fitted_tau)
plt.show()


# w_bal_bi_exp, FC_balance, SC_balance = w_prime_bal_dynamic_bi_exp(data["power"], cp=cp, w_prime=w_prime, rec_parameter=42, tau_dynamic=True)

# w_bal_ode = w_prime_balance_ode(data["power"], cp, w_prime)
# w_bal_bi_exp, FC_bal, SC_bal = w_prime_balance_bi_exp(data["power"], cp, w_prime)
#w_bal_bi_exp, FC_bal, SC_bal = w_prime_balance_bi_exp_2(data["power"], cp, w_prime)

# plt.plot(w_bal_bi_exp)
# plt.plot(w_bal_ode)
# plt.legend(["Bi exp", "ODE"])
# plt.show()

# params, cov = curve_fit(w_prime_balance_bi_exp_reg, [0, 248, 488, 602, 846, 948], [w_prime, 1500, 12618, 1500, 12096, 1500],bounds=([0.2, 0.2],[100,100]), p0=[1.1, 1.3])
# print(params)

# params, cov = curve_fit(w_prime_balance_bi_exp_reg, [0, 282, 319, 388, 423, 482], [w_prime, 1500, 7913, 1500, 7389, 1500],bounds=([0.2, 0.2],[100,100]), p0=[1.1, 1.3])
# print(params)

# plt.subplot(2,1,1)
# plt.plot(w_bal_bi_exp)
# plt.plot(w_bal_ode)
# plt.legend(["bi exp", "ode"])
# plt.subplot(2,1,2)
# plt.plot(FC_bal)
# plt.plot(SC_bal)
# plt.legend(["FC bal", "SC bal"])
# plt.show()

