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
act.remove_unactive_period(900)

test_power = 100*[400] + 100*[290] + 100*[280] + 100*[250] + 100*[240]
test_time = np.arange(0,500)

data = pd.DataFrame(dict(power=test_power), index=test_time)

# w_bal_bi_exp, FC_bal, SC_bal = w_prime_bal_dynamic_bi_exp(data["power"], cp, w_prime)

w_bal_bi_exp, FC_bal, SC_bal = w_prime_balance_bi_exp(data["power"], cp, w_prime)
w_bal_ode = w_prime_balance_ode(data["power"], cp, w_prime)
w_bal_bart = w_prime_balance_bartram(data["power"], cp, w_prime)
w_bal_int = w_prime_balance_integral(data["power"], cp, w_prime, tau_dynamic=True)


plt.subplot(2,1,1)
plt.plot(w_bal_bi_exp)
plt.plot(w_bal_ode)
plt.legend(["Bi exp", "ode"])

plt.subplot(2,1,2)
plt.plot(FC_bal)
plt.plot(SC_bal)
plt.legend(['FC bal', 'SC bal'])
plt.show()

# plt.subplot(3,1,3)
# plt.plot(tau_fc_dynamic)
# plt.plot(tau_sc_dynamic)
# plt.legend(['tau fc', 'tau sc'])
# plt.show()

# power_profile = 240*[350] + 30*[225] + 120*[350] + 30*[225]+ 100*[350]
# plt.plot(power_profile)
# plt.plot(len(power_profile)*[cp])
# plt.xlabel('Time [s]')
# plt.ylabel('Power [W]')
# plt.legend(['Target power', 'CP'])
# plt.ylim((0,400))
# plt.show()



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

