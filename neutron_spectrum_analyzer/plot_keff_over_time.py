import h5py
import numpy as np
import matplotlib.pyplot as plt

with h5py.File("output/depletion_results.h5", "r") as f:
    time = f["time"][:]
    eigenvalues = f["eigenvalues"][:]

# Use start of timestep as x-axis
time_days = time[:,0] / 86400  # convert seconds to days

# Extract mean and std from columns
k_eff_data = eigenvalues[:,0]
keff = k_eff_data[:,0]
keff_std = k_eff_data[:,1]

# Plot
plt.errorbar(
    x=time_days,
    y=keff,
    yerr=keff_std,
    marker="o",
    linestyle="-",
    capsize=4,
    label="k-effective"
)
plt.xlabel("Depletion Time [days]")
plt.ylabel("k-effective")
plt.title("k-effective vs Time")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("keff_vs_time.png", dpi=300)
plt.show()
