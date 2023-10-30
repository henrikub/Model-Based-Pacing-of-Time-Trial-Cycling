import numpy as np 


def find_last_active_datapoint(power, approx_time):
    for i in range(approx_time, len(power)):
        if power[i] < 100:
            return i

def remove_unactive_period(approx_time, power, *args):
    """
    Remove unactive time in an activity. Unactive is defined as power below 100W.
    Returns:
        A tuple with power as the first element, followed by the other variables passed in *args.
    
    """
    last_datapoint = find_last_active_datapoint(power, approx_time)
    new_power = power[0:last_datapoint]
    new_values = []
    for elem in args:
        new_values.append(elem[0:last_datapoint])
    return (new_power,) + tuple(new_values)
