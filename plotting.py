import matplotlib.pyplot as plt
import numpy as np

def compare_power(power_data, distance, legends):
    for power in power_data:
        plt.plot(distance, power)

    plt.legend(legends)
    plt.xlabel("Distance [m]")
    plt.ylabel("Power [W]")
    plt.title("Comparison of power")
    plt.show()

def plot_regression(power_points, time_points, fitted_ltw, fitted_lp, fitted_nl2, fitted_nl3, fitted_exp, fitted_nl4):
    time = np.arange(1,1200)
    power = np.arange(0,500)
    

    plt.subplot(3, 2 ,1)
    plt.plot(1/time, fitted_lp)
    plt.title("Linear-P")
    plt.xlabel("1/time [1/s]")
    plt.ylabel("Power [W]")
    for i in range(len(power_points)):
        plt.plot(1/time_points[i], power_points[i], marker="o", markersize=10, markeredgecolor="red", markerfacecolor="red")
    plt.xlim(0, 0.007)
    plt.ylim(0, 550)

    plt.subplot(3,2,2)
    plt.plot(time, fitted_ltw)
    plt.title("Linear-TW")
    plt.xlabel("Time [s]")
    plt.ylabel("Total work [J]")
    for i in range(len(power_points)):
        plt.plot(time_points[i], power_points[i]*time_points[i], marker="o", markersize=10, markeredgecolor="red", markerfacecolor="red")
    plt.xlim(0,1200)
    plt.ylim(0,400000)

    plt.subplot(3,2,3)
    plt.plot(power, fitted_nl2)
    plt.title("Nonlinear-2")
    plt.xlabel("Power [W]")
    plt.ylabel("Time [s]")
    for i in range(len(power_points)):
        plt.plot(power_points[i], time_points[i], marker="o", markersize=10, markeredgecolor="red", markerfacecolor="red")
    plt.xlim(270,500)
    plt.ylim(0,1200)

    plt.subplot(3,2,4)
    plt.plot(power, fitted_nl3)
    plt.title("Nonlinear-3")
    plt.xlabel("Power [W]")
    plt.ylabel("Time [s]")
    for i in range(len(power_points)):
        plt.plot(power_points[i], time_points[i], marker="o", markersize=10, markeredgecolor="red", markerfacecolor="red")
    plt.xlim(270,500)
    plt.ylim(0,1200)

    plt.subplot(3,2,5)
    plt.plot(time, fitted_exp)
    plt.title("Exp model")
    plt.xlabel("Power [W]")
    plt.ylabel("Time [s]")
    for i in range(len(power_points)):
        plt.plot(power_points[i], time_points[i], marker="o", markersize=10, markeredgecolor="red", markerfacecolor="red")
    plt.xlim(270,500)
    plt.ylim(0,1200)

    plt.subplot(3,2,6)
    plt.plot(power, fitted_nl4)
    plt.title("Nonlinear-4")
    plt.xlabel("Power [W]")
    plt.ylabel("Time [s]")
    for i in range(len(power_points)):
        plt.plot(power_points[i], time_points[i], marker="o", markersize=10, markeredgecolor="red", markerfacecolor="red")
    plt.xlim(270,500)
    plt.ylim(0,1200)

    plt.subplots_adjust(hspace=0.5)
    plt.show()