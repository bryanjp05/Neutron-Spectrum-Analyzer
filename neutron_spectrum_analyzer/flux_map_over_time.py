import openmc
import openmc.deplete
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
    glob.glob("openmc_simulation_n*.h5"),
    key=lambda x: int(re.search(r"n(\d+)", x).group(1))
)

if not statepoints:
    raise FileNotFoundError("No depletion statepoint files (openmc_simulation_n*.h5) found.")

# Process each timestep
for i, sp_file in enumerate(statepoints):
    print(f"Processing {sp_file}")
    sp = openmc.StatePoint(sp_file)

    try:
        # Get the flux tally
        tally = sp.get_tally(name="17x17 flux map")
        flux_data = tally.get_values(scores=["flux"]).reshape((17, 17))

        # Normalize (optional)
        total_flux = flux_data.sum()
        if total_flux > 0:
            flux_data /= total_flux
        else:
            print(f"Warning: total flux is zero in {sp_file}")

        # Save CSV
        csv_path = f"results/flux_map_step_{i}.csv"
        pd.DataFrame(flux_data).to_csv(csv_path, index=False)
        print(f"Saved CSV to {csv_path}")

        # Plot
        plt.figure(figsize=(6, 5))
        plt.imshow(flux_data, cmap="hot", origin="lower")
        plt.colorbar(label="Relative Flux")
        plt.title(f"Neutron Flux - Step {i}")
        plt.xlabel("Pin Column")
        plt.ylabel("Pin Row")
        plt.tight_layout()
        plt.show()

    except LookupError:
        print(f"Tally '17x17 flux map' not found in {sp_file}. Skipping.")

print("All timesteps processed.")

