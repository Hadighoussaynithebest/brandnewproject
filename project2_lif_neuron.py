import numpy as np
import matplotlib.pyplot as plt

# Simulation parameters
dt = 0.1          # time step (ms)
T = 200           # total time (ms)
time = np.arange(0, T, dt)

# LIF neuron parameters
tau_m = 20.0      # membrane time constant (ms)
R_m = 1.0         # membrane resistance
V_rest = -65.0    # resting potential (mV)
V_reset = -65.0   # reset potential (mV)
V_thresh = -50.0  # spike threshold (mV)

# Input current (constant for simplicity)
I = np.zeros_like(time)
I[500:1500] = 1.5  # inject current between 50 ms and 150 ms

# State variable
V = np.ones_like(time) * V_rest
spike_times = []

for i in range(1, len(time)):
    dV = (-(V[i-1] - V_rest) + R_m * I[i-1]) / tau_m
    V[i] = V[i-1] + dt * dV

    if V[i] >= V_thresh:
        V[i-1] = 20.0           # spike peak for plotting
        V[i] = V_reset          # reset
        spike_times.append(time[i])

print("Spike times (ms):", spike_times)

# Plot membrane potential
plt.figure()
plt.plot(time, V)
plt.axhline(V_thresh, linestyle='--')
plt.xlabel("Time (ms)")
plt.ylabel("Membrane potential (mV)")
plt.title("Leaky Integrate-and-Fire Neuron")
plt.show()
