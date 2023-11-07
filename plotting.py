import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import numpy as np

def compare_power(power_data, distance, legends, title=None):
    for power in power_data:
        plt.plot(distance, power)

    plt.legend(legends)
    plt.xlabel("Distance [m]")
    plt.ylabel("Power [W]")
    plt.title(title)
    plt.show()

def plot_regression(power_points, time_points, fitted_ltw, params_ltw, fitted_lp, params_lp, fitted_nl2, params_nl2, fitted_nl3, params_nl3, fitted_nl4, params_nl4):
    time = np.arange(1,1200)
    power = np.arange(0,500)
    
    plt.subplot(2, 1 ,1)
    plt.plot(1/time, fitted_lp)
    plt.title("Linear-P")
    plt.xlabel("1/time [1/s]")
    plt.ylabel("Power [W]")
    text_lp = f'CP = {round(params_lp[1])}W\nAWC = {round(params_lp[0]/1000,2)}kJ'
    plt.text(0.8, 0.5, text_lp, ha='center', va='center', transform=plt.gca().transAxes, fontsize='large')
    for i in range(len(power_points)):
        plt.plot(1/time_points[i], power_points[i], marker="o", markersize=10, markeredgecolor="red", markerfacecolor="red")
    plt.xlim(0, 0.007)
    plt.ylim(0, 550)

    ax = plt.subplot(2,1,2)
    plt.plot(time, fitted_ltw)
    formatter = FuncFormatter(lambda x, pos: x/1000)
    ax.yaxis.set_major_formatter(formatter)
    plt.title("Linear-TW")
    plt.xlabel("Time [s]")
    plt.ylabel("Total work [kJ]")
    text_ltw = f'CP = {round(params_ltw[1])}W\nAWC = {round(params_ltw[0]/1000,2)}kJ'
    plt.text(0.8, 0.5, text_ltw, ha='center', va='center', transform=plt.gca().transAxes, fontsize='large')
    for i in range(len(power_points)):
        plt.plot(time_points[i], power_points[i]*time_points[i], marker="o", markersize=10, markeredgecolor="red", markerfacecolor="red")
    plt.xlim(0,1200)
    plt.ylim(0,400000)
    plt.subplots_adjust(hspace=0.7)
    plt.show()

    plt.subplot(2,1,1)
    plt.plot(power, fitted_nl2)
    plt.title("Nonlinear-2")
    plt.xlabel("Power [W]")
    plt.ylabel("Time [s]")
    text_nl2 = f'CP = {round(params_nl2[1])}W\nAWC = {round(params_nl2[0]/1000,2)}kJ'
    plt.text(0.8, 0.5, text_nl2, ha='center', va='center', transform=plt.gca().transAxes, fontsize='large')
    for i in range(len(power_points)):
        plt.plot(power_points[i], time_points[i], marker="o", markersize=10, markeredgecolor="red", markerfacecolor="red")
    plt.xlim(270,500)
    plt.ylim(0,1200)

    plt.subplot(2,1,2)
    plt.plot(power, fitted_nl3)
    plt.title("Nonlinear-3")
    plt.xlabel("Power [W]")
    plt.ylabel("Time [s]")
    text_nl3 = f'CP = {round(params_nl3[1])}W\nAWC = {round(params_nl3[0]/1000,2)}kJ\nP_max = {round(params_nl3[2])}W'
    plt.text(0.8, 0.5, text_nl3, ha='center', va='center', transform=plt.gca().transAxes, fontsize='large')
    for i in range(len(power_points)):
        plt.plot(power_points[i], time_points[i], marker="o", markersize=10, markeredgecolor="red", markerfacecolor="red")
    plt.xlim(270,500)
    plt.ylim(0,1200)
    plt.subplots_adjust(hspace=0.7)
    plt.show()

    plt.subplot(2,1,1)
    plt.plot(power, fitted_nl4)
    plt.title("Nonlinear-4")
    plt.xlabel("Power [W]")
    plt.ylabel("Time [s]")
    text_nl4 = f'CP = {round(params_nl4[1])}W\nAWC = {round(params_nl4[0]/1000,2)}kJ\nP_max = {round(params_nl4[2])}W\ntau = {round(params_nl4[3], 4)}'
    plt.text(0.8, 0.5, text_nl4, ha='center', va='center', transform=plt.gca().transAxes, fontsize='large')
    for i in range(len(power_points)):
        plt.plot(power_points[i], time_points[i], marker="o", markersize=10, markeredgecolor="red", markerfacecolor="red")
    plt.xlim(270,500)
    plt.ylim(0,1200)

    plt.subplots_adjust(hspace=0.7)
    plt.show()