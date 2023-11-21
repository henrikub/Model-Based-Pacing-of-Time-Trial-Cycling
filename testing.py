import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from plotting import *
from activity_reader import ActivityReader
from w_bal import *
from scipy.optimize import curve_fit


cp = 265
w_prime = 26630

act = ActivityReader("Validation_test_30s_rec.tcx")
act.remove_unactive_period(400)

test_power = 100*[300] + 2*[250]
test_time = np.arange(0,102,1)

data = pd.DataFrame(dict(power=act.power), index=act.time)

# w_bal_bi_exp, FC_balance, SC_balance = w_prime_bal_dynamic_bi_exp(data["power"], cp=cp, w_prime=w_prime, rec_parameter=42, tau_dynamic=True)

w_bal_ode = w_prime_balance_ode(data["power"], cp, w_prime)
w_bal_biexp = w_prime_balance_bi_exp(data["power"], cp, w_prime)

plt.plot(w_bal_biexp)
plt.plot(w_bal_ode)
plt.legend(["Bi exp", "ODE"])
plt.show()

# params, cov = curve_fit(w_prime_balance_bi_exp_reg, [0, 248, 488, 602, 846, 948], [w_prime, 1500, 12618, 1500, 12096, 1500],bounds=([0.2, 0.2, 3, 50],[2,2,100, 1000]), p0=[1.1, 1.3, 10, 400])
# print(params)

params, cov = curve_fit(w_prime_balance_bi_exp_reg, [0, 282, 319, 388, 423, 482], [w_prime, 1500, 7913, 1500, 7389, 1500],bounds=([0.2, 0.2, 3, 50],[2,2,100, 1000]), p0=[1.1, 1.3, 10, 400])
print(params)

# plt.subplot(2,1,1)
# plt.plot(w_bal_bi_exp)
# plt.plot(w_bal_ode)
# plt.legend(["bi exp", "ode"])
# plt.subplot(2,1,2)
# plt.plot(FC_balance)
# plt.plot(SC_balance)
# plt.legend(["FC bal", "SC bal"])
# plt.show()

