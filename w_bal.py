import math

import numpy as np
import pandas as pd


def tau_w_prime_balance(power, cp, untill=None):
    if untill is None:
        untill = len(power)

    avg_power_below_cp = power[:untill][power[:untill] < cp].mean()
    if math.isnan(avg_power_below_cp):
        avg_power_below_cp = 0
    delta_cp = cp - avg_power_below_cp

    return 546 * math.e ** (-0.01 * delta_cp) + 316


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

def tau_fc(power, cp, untill = None):
    if untill is None:
        untill = len(power)

    avg_power_below_cp = power[:untill][power[:untill] < cp].mean()
    if math.isnan(avg_power_below_cp):
        avg_power_below_cp = 0
    d_cp = avg_power_below_cp/cp

    return 45 * math.e ** (-0.014 * d_cp) + 9999 * math.e ** (-0.811 * d_cp)


def tau_sc(power, cp, untill = None):
    if untill is None:
        untill = len(power)

    avg_power_below_cp = power[:untill][power[:untill] < cp].mean()
    if math.isnan(avg_power_below_cp):
        avg_power_below_cp = 0
    d_cp = avg_power_below_cp/cp

    return 9999* math.e ** (-0.098 * d_cp) + 429


def w_prime_bal_dynamic_bi_exp(power, cp, w_prime, rec_parameter=0.46, tau_dynamic=False, tau_value=None, *args, **kwargs):
    last = w_prime
    w_prime_balance = []
    FC_amp = w_prime * (0.75 * rec_parameter + 5.26)
    SC_amp = w_prime - FC_amp
    tau_fc = get_bi_exp_tau_method(power, cp, tau_dynamic, tau_value, fast_component=True)
    tau_sc = get_bi_exp_tau_method(power, cp, tau_dynamic, tau_value, fast_component=False)

    for t in range(len(power)):

        for u, p in enumerate(power[: t + 1]):
            if p >= cp: 
                new = w_prime - ((p-cp) * t * w_prime * FC_amp / last) - ((p-cp) * t * w_prime*SC_amp / last) 
            else: 
                new = (FC_amp - w_prime*FC_amp) * (1 - math.e ** (-t/tau_fc(t))) + (SC_amp - w_prime*SC_amp) * (1 - math.e ** (-t/tau_sc(t)))
                

        w_prime_balance.append(new)
        last = new

    return pd.Series(w_prime_balance)


def w_prime_balance_waterworth(
    power, cp, w_prime, tau_dynamic=False, tau_value=None, *args, **kwargs
):
    """
    Optimisation of Skiba's algorithm by Dave Waterworth.
    Source:
    http://markliversedge.blogspot.nl/2014/10/wbal-optimisation-by-mathematician.html
    Source:
    Skiba, Philip Friere, et al. "Modeling the expenditure and reconstitution of work capacity above critical power." Medicine and science in sports and exercise 44.8 (2012): 1526-1532.
    """
    sampling_rate = 1
    running_sum = 0
    w_prime_balance = []
    tau = get_tau_method(power, cp, tau_dynamic, tau_value)

    for t, p in enumerate(power):
        power_above_cp = p - cp
        w_prime_expended = max(0, power_above_cp) * sampling_rate
        running_sum = running_sum + w_prime_expended * (
            math.e ** (t * sampling_rate / tau(t))
        )

        w_prime_balance.append(
            w_prime - running_sum * math.e ** (-t * sampling_rate / tau(t))
        )

    return pd.Series(w_prime_balance)


def w_prime_balance_skiba(
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


def w_prime_balance_bi_exp(
    power, cp, w_prime, tau_dynamic=False, tau_value=None, *args, **kwargs
):

    w_prime_balance = []
    tau_1 = get_tau_method(power, cp, tau_dynamic, 22)
    tau_2 = get_tau_method(power, cp, tau_dynamic, 377)
    A = 1
    alpha_1 = 0.477
    alpha_2 = 1-alpha_1

    for t in range(len(power)):
        w_prime_exp_sum = 0

        for u, p in enumerate(power[: t + 1]):
            w_prime_exp = max(0, p - cp)
            w_prime_exp_sum += w_prime_exp * (A*alpha_1 * np.power(np.e, (u - t) / tau_1(t)) +  A*alpha_2 * np.power(np.e, (u - t) / tau_2(t)))

        w_prime_balance.append(w_prime - w_prime_exp_sum)

    return pd.Series(w_prime_balance)


def w_prime_balance_froncioni_skiba_clarke(power, cp, w_prime):
    """
    Source:
    Skiba, P. F., Fulford, J., Clarke, D. C., Vanhatalo, A., & Jones, A. M. (2015). Intramuscular determinants of the ability to recover work capacity above critical power. European journal of applied physiology, 115(4), 703-713.
    """
    last = w_prime
    w_prime_balance = []

    for p in power:
        if p < cp:
            new = last + (cp - p) * (w_prime - last) / w_prime
        else:
            new = last + (cp - p)

        w_prime_balance.append(new)
        last = new

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


def w_prime_balance(power, cp, w_prime, algorithm="waterworth", *args, **kwargs):
    if algorithm == "waterworth":
        method = w_prime_balance_waterworth
    elif algorithm == "skiba":
        method = w_prime_balance_skiba
    elif algorithm == "froncioni-skiba-clarke":
        method = w_prime_balance_froncioni_skiba_clarke
    elif algorithm == "ode":
        method = w_prime_balance_ode
    elif algorithm == "bi_exponential":
        method = w_prime_balance_bi_exp
    elif algorithm == "dyamic_bi_exponential":
        method = w_prime_bal_dynamic_bi_exp

    return method(power, cp, w_prime, *args, **kwargs)



        