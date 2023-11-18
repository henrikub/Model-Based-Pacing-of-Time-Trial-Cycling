import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from plotting import *
from activity_reader import ActivityReader
from w_bal import *


cp = 265
w_prime = 26630

act = ActivityReader("Validation_test_240s_rec.tcx")
act.remove_unactive_period(700)

test_power = 100*[300] + 100*[280]
test_time = np.arange(0,200,1)

data = pd.DataFrame(dict(power=test_power), index=test_time)

w_bal_bi_exp, FC_balance, SC_balance = w_prime_bal_dynamic_bi_exp(data["power"], cp=cp, w_prime=w_prime, rec_parameter=46, tau_dynamic=True)
w_bal_ode = w_prime_balance_ode(data["power"], cp, w_prime)

plt.subplot(2,1,1)
plt.plot(w_bal_bi_exp)
plt.plot(w_bal_ode)
plt.legend(["bi exp", "ode"])
plt.subplot(2,1,2)
plt.plot(FC_balance)
plt.plot(SC_balance)
plt.legend(["FC bal", "SC bal"])
plt.show()

