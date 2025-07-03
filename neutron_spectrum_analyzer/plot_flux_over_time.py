import openmc
import openmc.deplete
import matplotlib.pyplot as plt
import numpy as np
import glob
import re

# Open the depletion results
results = openmc.deplete.Results("depletion_results.h5")

statepoints = sorted(
    glob.glob("openmc_simulation_n*.h5"),
    key=lambda x: int(re.search(r"n(\d+)", x).group(1))
)

for i, sp_file in enumerate(statepoints):
    print(f"Processing {sp_file}")
    sp = openmc.StatePoint(sp_file)

    try:
        tally = sp.get_tally(name='17x17 flux map')
        flux_data = tally.get_slice(scores=['flux']).mean.reshape((17, 17))

        plt.imshow(flux_data, cmap='hot', origin='lower')
        plt.colorbar(label='Flux (n/cm²/s)')
        plt.title(f'Neutron Flux - Step {i}')
        plt.xlabel('Pin Column')
        plt.ylabel('Pin Row')
        plt.show()

    except LookupError:
        print(f"Tally not found in {sp_file}. Skipping.")

