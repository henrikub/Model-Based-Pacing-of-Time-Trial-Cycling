import math
import numpy as np
import pandas as pd


def get_tau_method(power, cp, tau_dynamic, tau_value):
    if tau_dynamic:
        tau_dynamic = [tau_w_prime_balance(power, cp, i) for i in range(len(power))]
        tau = lambda t: tau_dynamic[t]

    elif tau_value is None:
        static_tau = tau_w_prime_balance(power, cp)
        tau = lambda t: static_tau

    else:
        tau = lambda t: tau_value

    return tau


def get_bi_exp_tau_method(power, cp, tau_dynamic, tau_value, fast_component):
    if tau_dynamic:
        if fast_component:
            tau_dynamic = [tau_fc(power, cp, i) for i in range(len(power))]
            tau = lambda t: tau_dynamic[t]
        else:
            tau_dynamic = [tau_sc(power, cp, i) for i in range(len(power))]
            tau = lambda t: tau_dynamic[t]

    elif tau_value is None:
        if fast_component:
            static_tau = tau_fc(power, cp)
            tau = lambda t: static_tau
        else:
            static_tau = tau_sc(power, cp)
            tau = lambda t: static_tau

    else:
        tau = lambda t: tau_value

    return tau


def tau_w_prime_balance(power, cp, untill=None):
    if untill is None:
        untill = len(power)

    avg_power_below_cp = power[:untill][power[:untill] < cp].mean()
    if math.isnan(avg_power_below_cp):
        avg_power_below_cp = 0
    delta_cp = cp - avg_power_below_cp

    return 546 * math.e ** (-0.01 * delta_cp) + 316


def tau_fc(power, cp, untill = None):
    if untill is None:
        untill = len(power)

    avg_power_below_cp = power[:untill][power[:untill] < cp].mean()
    if math.isnan(avg_power_below_cp):
        avg_power_below_cp = 0
    d_cp = avg_power_below_cp/cp *100

    return 45 * math.e ** (-0.014 * d_cp) + 9999 * math.e ** (-0.811 * d_cp)


def tau_sc(power, cp, untill = None):
    if untill is None:
        untill = len(power)

    avg_power_below_cp = power[:untill][power[:untill] < cp].mean()
    if math.isnan(avg_power_below_cp):
        avg_power_below_cp = 0
    d_cp = avg_power_below_cp/cp *100

    return 9999* math.e ** (-0.098 * d_cp) + 429


def w_prime_balance_integral(
    power, cp, w_prime, tau_dynamic=False, tau_value=None, *args, **kwargs
):
    """
    Source:
    Skiba, Philip Friere, et al. "Modeling the expenditure and reconstitution of work capacity above critical power." Medicine and science in sports and exercise 44.8 (2012): 1526-1532.
    """
    w_prime_balance = []
    tau = get_tau_method(power, cp, tau_dynamic, tau_value)

    for t in range(len(power)):
        w_prime_exp_sum = 0

        for u, p in enumerate(power[: t + 1]):
            w_prime_exp = max(0, p - cp)
            w_prime_exp_sum += w_prime_exp * np.power(np.e, (u - t) / tau(t))

        w_prime_balance.append(w_prime - w_prime_exp_sum)

    return pd.Series(w_prime_balance)


def w_prime_balance_ode(power, cp, w_prime):

    last = w_prime
    w_prime_balance = []

    for p in power:
        if p < cp:
            new = w_prime - (w_prime - last) * np.power(np.e, -(cp - p)/w_prime)

        elif p == cp:
            new = last
        else:
            new = last - (p - cp)

        w_prime_balance.append(new)
        last = new

    return pd.Series(w_prime_balance)


def w_prime_balance_bart(power, cp, w_prime):

    last = w_prime
    w_prime_balance = []

    for p in power:
        if p < cp:
            new = w_prime - (w_prime - last) * np.power(np.e, -1/(2287.2*(cp-p)**-0.688))
        elif p == cp:
            new = last
        else:
            new = last - (p - cp)

        w_prime_balance.append(new)
        last = new

    return pd.Series(w_prime_balance)


def w_prime_bal_dynamic_bi_exp(power, cp, w_prime, rec_parameter=42, tau_dynamic=False, tau_value=None, *args, **kwargs):
    last_w_bal = w_prime
    w_prime_balance = []
    FC_balance = []
    SC_balance = []
    FC_amp = (w_prime * (0.75 * rec_parameter + 5.26))/100
    SC_amp = w_prime - FC_amp
    tau_fc = get_bi_exp_tau_method(power, cp, tau_dynamic, tau_value, fast_component=True)
    tau_sc = get_bi_exp_tau_method(power, cp, tau_dynamic, tau_value, fast_component=False)
    FC_bal = FC_amp
    SC_bal = SC_amp 
    new_FC_bal = 0
    new_SC_bal = 0

    for t in range(len(power)):
        print(f"percentage FC = {FC_amp/w_prime} percentage SC = {SC_amp/w_prime}")
        print(f"\nt = {t} and FC_bal = {FC_bal} and SC_bal = {SC_bal} and last_w_bal = {last_w_bal}")
        for u, p in enumerate(power[: t + 1]):
            #print(f"u = {u} and FC_bal = {FC_bal} and SC_bal = {SC_bal} and last_w_bal = {last_w_bal}")
            if p >= cp: 
                new_FC_bal = FC_amp - ((p-cp) * t * FC_bal / last_w_bal)
                new_SC_bal = SC_amp - ((p-cp) * t * SC_bal / last_w_bal)
                new_w_bal = w_prime - ((p-cp) * t * FC_bal / last_w_bal) - ((p-cp) * t * SC_bal / last_w_bal)
            else: 
                print(f"tau fc = {tau_fc(t)} tau sc = {tau_sc(t)}")
                new_FC_bal = (FC_amp - FC_bal) * (1 - math.e ** (-t/tau_fc(t)))
                new_SC_bal = (SC_amp - SC_bal) * (1 - math.e ** (-t/tau_sc(t)))
                new_w_bal = (FC_amp - FC_bal) * (1 - math.e ** (-t/tau_fc(t))) + (SC_amp - SC_bal) * (1 - math.e ** (-t/tau_sc(t)))

        w_prime_balance.append(new_w_bal)
        FC_balance.append(new_FC_bal)
        SC_balance.append(new_SC_bal)
        last_w_bal = new_w_bal

        FC_bal = new_FC_bal
        SC_bal = new_SC_bal

    return (pd.Series(w_prime_balance), FC_balance, SC_balance)


def w_prime_balance_bi_exp(
    power, cp, w_prime, tau_dynamic=False, tau_value=None, *args, **kwargs
):

    w_prime_balance = []
    FC_bal = []
    SC_bal = []
    FC_amp = 0.3679*w_prime
    SC_amp = 0.6324*w_prime
    tau_fc = get_bi_exp_tau_method(power, cp, tau_dynamic, tau_value, fast_component=True)
    tau_sc = get_bi_exp_tau_method(power, cp, tau_dynamic, tau_value, fast_component=False)
    FC = 4.4
    SC = 0.9

    for t in range(len(power)):
        w_prime_exp_sum = 0
        FC_exp_sum = 0
        SC_exp_sum = 0

        for u, p in enumerate(power[: t + 1]):
            w_prime_exp = max(0, p - cp)
            FC_exp_sum += w_prime_exp * (FC * np.power(np.e, (u - t) / tau_fc(t)))
            SC_exp_sum += w_prime_exp * (SC * np.power(np.e, (u - t) / tau_sc(t)))
        
        w_prime_exp_sum = FC_exp_sum + SC_exp_sum
        w_prime_balance.append(w_prime - w_prime_exp_sum)
        FC_bal.append(FC_amp - FC_exp_sum)
        SC_bal.append(SC_amp - SC_exp_sum)

    return w_prime_balance, FC_bal, SC_bal


def w_prime_balance_bi_exp_2(
    power, cp, w_prime, tau_dynamic=False, tau_value=None, *args, **kwargs
):

    w_prime_balance = []
    FC_bal = []
    SC_bal = []
    FC_amp = 0.3679*w_prime
    SC_amp = 0.6324*w_prime
    tau_fc = get_bi_exp_tau_method(power, cp, tau_dynamic, tau_value, fast_component=True)
    tau_sc = get_bi_exp_tau_method(power, cp, tau_dynamic, tau_value, fast_component=False)
    FC = 3
    SC = 1.5

    for t in range(len(power)):
        w_prime_exp_sum = 0
        FC_exp_sum = 0
        SC_exp_sum = 0
        for u, p in enumerate(power[: t + 1]):
            if p < cp:
                FC_exp_sum += (p-cp) * (FC * np.power(np.e, (u - t) / tau_fc(t)))
                SC_exp_sum += (p-cp) * (SC * np.power(np.e, (u - t) / tau_sc(t)))
            else:
                FC_exp_sum -= (cp-p)/2
                SC_exp_sum -= (cp-p)/2
            
        w_prime_exp_sum = FC_exp_sum + SC_exp_sum
        w_prime_balance.append(w_prime - w_prime_exp_sum)
        FC_bal.append(FC_amp - FC_exp_sum)
        SC_bal.append(SC_amp - SC_exp_sum)

    return w_prime_balance, FC_bal, SC_bal


def w_prime_balance_bi_exp_reg(power, FC, SC):
    cp = 265
    w_prime = 26630
    w_prime_balance = []
    tau_fc = get_bi_exp_tau_method(power, cp, False, None, fast_component=True)
    tau_sc = get_bi_exp_tau_method(power, cp, False, None, fast_component=False)

    for t in range(len(power)):
        w_prime_exp_sum = 0

        for u, p in enumerate(power[: t + 1]):
            w_prime_exp = max(0, p - cp)
            w_prime_exp_sum += w_prime_exp * (FC * np.power(np.e, (u - t) / tau_fc(t)) +  SC * np.power(np.e, (u - t) / tau_sc(t)))
            
        w_prime_balance.append(w_prime - w_prime_exp_sum)

    return pd.Series(w_prime_balance)