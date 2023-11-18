import pandas as pd
import matplotlib.pyplot as plt
import sweat
import numpy as np
from plotting import *
from activity_reader import ActivityReader
from w_bal import *

# act = ActivityReader("Validation_test_30s_rec.tcx")
# act.remove_unactive_period(400)
# power = [0] + 19*[300] + [20, 20]
# time = np.arange(0, 22, 1)
# cp = 245
# w_prime = 14000
# data = pd.DataFrame(dict(power=power), index=time)

# w_bal_ode = sweat.w_prime_balance(data["power"], cp=cp, algorithm='ode', w_prime=w_prime).to_list()
# w_bal_skiba = sweat.w_prime_balance(data["power"], cp=cp, algorithm='skiba', w_prime=w_prime, tau_dynamic=False).to_list()


# compare_power([w_bal_ode, w_bal_skiba], time, legends=["waterworth", "froncioni-skiba-clarke"])

# for w_bal in w_bal_skiba:
#     print(w_bal)


# test = sweat.w_prime_balance(data["power"], cp=cp, algorithm='skiba', w_prime=w_prime).to_list()
# test = integral_w_bal(act.power, cp, w_prime)
# plt.plot(test)
# plt.show()

# w_bal_skiba = sweat.w_prime_balance(data["power"], cp=cp, algorithm='waterworth', w_prime=w_prime).to_list()
# plt.plot(w_bal_skiba)
# plt.show()

cp = 265
w_prime = 26630

act = ActivityReader("Validation_test_240s_rec.tcx")
act.remove_unactive_period(700)

test_power = 100*[300]
test_time = np.arange(0,100,1)

data = pd.DataFrame(dict(power=test_power), index=test_time)

#w_bal_bi_exp = sweat.w_prime_balance(data["power"], cp=cp, algorithm='dyamic_bi_exponential', w_prime=w_prime).to_list()
w_bal_bi_exp = w_prime_bal_dynamic_bi_exp(data["power"], cp=cp, w_prime=w_prime, rec_parameter=46)

plt.plot(test_time, w_bal_bi_exp)
plt.show()

