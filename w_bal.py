import numpy as np
import math

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


def integral_w_bal(power, cp, awc):
    w_bal = []

    for t in range(len(power)):
        w_expended_total = 0
        for u, p in enumerate(power[:t+1]):
            w_expended = max(0, p-cp)
            w_expended_total += w_expended *np.exp(-(t-u)/tau_w_prime_balance(power,cp))
        w_bal.append(awc-w_expended_total)

    return w_bal


def tau_w_prime_balance(power, cp):
    below_cp = [cp-p for p in power if p<cp]
    avg_power_below_cp = np.average(below_cp)
    if math.isnan(avg_power_below_cp):
        avg_power_below_cp = 0
    delta_cp = cp - avg_power_below_cp

    return 546 * math.e ** (-0.01 * delta_cp) + 316


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

def count_above_or_below_threshold(arr, thres):
    diff = [power-thres for power in arr]
    count = 1
    result = []
    for i in range(1, len(arr)):
        if diff[i] * diff[i-1] >0:
            count += 1
        else:
            for _ in range(count):
                result.append(count)
            count = 1
    for _ in range(count):
        result.append(count)
    return result

def bi_exponential_w_bal(power, cp, awc, recovery_param):
    w_bal = []
    w_bal_current = awc
    w_bal_next = 0
    fc_amp = awc*(0.75*recovery_param + 5.26)
    sc_amp = awc-fc_amp    
    # vet ikke hvordan disse skal defineres:
    fc_bal = 0.5
    sc_bal = 0.5
    length_of_interval = count_above_or_below_threshold(power, cp)

    # todo: make an array that has the same length as the power output, and contains the length of the current exp/rec interval
    for t, p in enumerate(power):

        if p >= cp:
            w_bal_next = awc - ((max(0,p-cp))*t*fc_bal)/w_bal_current - ((max(0,p-cp))*t*sc_bal)/w_bal_current
        
        else:
            w_bal_next = (fc_amp-fc_bal)*(1-np.exp(-t/(45*np.exp(-0.014*(p/cp))+9999*np.exp(-0.811*(p/cp))))) + (sc_amp-sc_bal)*(1-np.exp(-t/(9999*np.exp(-0.098*(p/cp))+429)))
        
        w_bal.append(w_bal_next)
        w_bal_current = w_bal_next

    return w_bal


        