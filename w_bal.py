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

def bi_exponential_w_bal(power, cp, awc):
    w_bal = []
    w_bal_current = awc
    w_bal_next = 0
    fc_amp = awc*(0.75*0.4+5.26)
    sc_amp = awc-fc_amp    
    # vet ikke hvordan disse skal defineres:
    fc_bal = 0.5
    sc_bal = 0.5
    length_of_interval = np.zeros(len(power))

    # todo: make an array that has the same length as the power output, and contains the length of the current exp/rec interval
    for i in range(len(power)):

        if power[i] >= cp:
            exp_interval = 0
            for j in range(i,len(power)):
                if power[j] < cp:
                    exp_interval = j-i
                    length_of_interval[i:exp_interval] = exp_interval
                    break

            w_bal_next = awc - ((max(0,power[i]-cp))*exp_interval*fc_bal)/w_bal_current - ((max(0,power[i]-cp))*exp_interval*sc_bal)/w_bal_current
        
        else:
            for j in range(i,len(power)):
                if power[j] > cp:
                    rec_interval = j-i
 
                    length_of_interval[i:rec_interval] = rec_interval
                    break
            w_bal_next = (fc_amp-fc_bal)*(1-np.exp(-rec_interval/(45*np.exp(-0.014*(power[i]/cp))+9999*np.exp(-0.811*(power[i]/cp))))) + (sc_amp-sc_bal)*(1-np.exp(-rec_interval/(9999*np.exp(-0.098*(power[i]/cp))+429)))
        
        w_bal.append(w_bal_next)
        w_bal_current = w_bal_next
        print(length_of_interval)
    return w_bal


        