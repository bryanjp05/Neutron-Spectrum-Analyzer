import openmc
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import glob
import re
import os

# Make sure results directory exists
os.makedirs("results", exist_ok=True)

# Find and sort all statepoints
statepoints = sorted(
    glob.glob("output/openmc_simulation_n*.h5"),
    key=lambda x: int(re.search(r"n(\d+)", x).group(1))
)

if not statepoints:
    raise FileNotFoundError("No depletion statepoint files (openmc_simulation_n*.h5) found.")

# Process each timestep
for i, sp_file in enumerate(statepoints):
    print(f"Processing {sp_file}")
    sp = openmc.StatePoint(sp_file)

    try:
        # Get the power (heating) tally
        power_tally = sp.get_tally(name="17x17 power map")
        power_data = power_tally.get_values(scores=["heating"]).reshape((17, 17))

        # Normalize to relative power
        total_power = power_data.sum()
        if total_power > 0:
            power_data /= total_power
        else:
            print(f"Warning: total power is zero in {sp_file}")

        # Export to CSV
        csv_path = f"results/power_map_step_{i}.csv"
        pd.DataFrame(power_data).to_csv(csv_path, index=False)
        print(f"Saved CSV to {csv_path}")

        # Plot
        plt.figure(figsize=(6, 5))
        plt.imshow(power_data, cmap="inferno", origin="lower")
        plt.colorbar(label="Relative Power")
        plt.title(f"Power Distribution - Step {i}")
        plt.xlabel("Pin Column")
        plt.ylabel("Pin Row")
        plt.tight_layout()
        plt.show()

    except LookupError:
        print(f"Tally '17x17 power map' not found in {sp_file}. Skipping.")

print("All timesteps processed.")

