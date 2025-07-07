import openmc
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Load statepoint file
sp = openmc.StatePoint('output/openmc_simulation_n0.h5')
flux_tally = sp.get_tally(name='17x17 flux map')
flux_data = flux_tally.get_values(scores=['flux']).reshape((17, 17))

# Plot heatmap
plt.imshow(flux_data, cmap='hot', origin='lower')
plt.colorbar(label='Flux (n/cm²/s)')
plt.title('Neutron Flux in 17x17 Assembly')
plt.xlabel('Pin Column')
plt.ylabel('Pin Row')
plt.tight_layout()
plt.show()

# Export to CSV
df = pd.DataFrame(flux_data)
df.to_csv("results/flux_map.csv", index=False)
print("Saved flux map to results/flux_map.csv")

