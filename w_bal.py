import numpy as np


def differential_w_bal(power, cp, awc):
    w_bal = []
    w_bal_current = awc
    w_bal_next = 0

    for p in power:
        if p < cp:
            w_bal_next = w_bal_current + (cp-p) * (awc-w_bal_current)/awc
        else:
            w_bal_next = w_bal_current + (cp-p)
        w_bal.append(w_bal_next)
        w_bal_current = w_bal_next

    return w_bal       

def bi_conditional_w_bal(power, cp, awc):
    w_bal = []
    w_bal_current = awc
    w_bal_next = 0
    w_exp = 0
    diff_above = np.zeros(len(power))
    diff_below = np.zeros(len(power))

    for i in range(len(power)):
        if power[i] >= cp:
            diff_above[i] = power[i] - cp
        else:
            diff_below[i] = cp - power[i]

    for i in range(len(power)):
        if power[i] >= cp:
            w_bal_next = w_bal_current - (power[i]-cp)*diff_above[i]
            w_exp = (power[i]-cp)*diff_above[i]
        else:  
            w_bal_next = w_bal_current - w_exp*np.exp(-diff_below[i]/(546*np.exp(-0.01*(cp-np.average(diff_below)))+316))
        w_bal.append(w_bal_next)
        w_bal_current = w_bal_next
    return w_bal


