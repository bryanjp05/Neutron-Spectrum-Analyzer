# neutron_spectrum_analyzer/power_analysis.py
import openmc
import matplotlib.pyplot as plt
import pandas as pd

# Load the statepoint
sp = openmc.StatePoint('statepoint.50.h5')

# Extract the power tally
power_tally = sp.get_tally(name='17x17 power map')
power_data = power_tally.get_values(scores=['heating']).reshape((17, 17))

# Normalize (optional)
power_data /= power_data.sum()

#Export to CSV
df = pd.DataFrame(power_data)
df.to_csv("results/power_map.csv", index=False)
print("Saved power map to results/power_map.csv")

# Plot
plt.imshow(power_data, cmap='inferno', origin='lower')
plt.colorbar(label='Relative Power')
plt.title('Power Distribution in 17x17 Assembly')
plt.xlabel('Pin Column')
plt.ylabel('Pin Row')
plt.tight_layout()
plt.show()

