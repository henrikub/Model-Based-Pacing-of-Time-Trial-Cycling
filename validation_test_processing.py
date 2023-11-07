from activity_reader import ActivityReader
import numpy as np

act = ActivityReader("Validation_test.tcx")
act.remove_unactive_period(900)

work_bout_1 = act.power[3:248]
recovery_1 = act.power[248:248+240]
work_bout_2 = act.power[488:602]
recovery_2 = act.power[602:602+240]
work_bout_3 = act.power[842:len(act.power)]

cp = 265

for i, elem in enumerate([recovery_1, recovery_2]):
    print(f"Average power for recovery {i+1} was {np.average(elem)}\n")

for i, elem in enumerate([work_bout_1, work_bout_2, work_bout_3]):
    w_prime_exp = np.sum([power-cp for power in elem])
    print(f"Average power for work bout {i+1} is {np.average(elem)}W")
    print(f"W' expended for work bout {i+1} is {w_prime_exp/1000}kJ\n")
