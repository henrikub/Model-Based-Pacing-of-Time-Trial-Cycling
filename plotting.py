import matplotlib.pyplot as plt

def compare_power(power_data, distance, legends):
    for power in power_data:
        plt.plot(distance, power)

    plt.legend(legends)
    plt.xlabel("Distance [m]")
    plt.ylabel("Power [W]")
    plt.title("Comparison of power")
    plt.show()