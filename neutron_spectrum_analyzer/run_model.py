import openmc
import matplotlib.pyplot as plt
import numpy as np

from neutron_spectrum_analyzer.materials import create_materials
from neutron_spectrum_analyzer.geometry import create_geometry
from neutron_spectrum_analyzer.settings import create_settings
from neutron_spectrum_analyzer.tallies import create_tallies

if __name__ == "__main__":
    materials = create_materials()
    geometry, fuel_cells = create_geometry(materials)
    settings = create_settings()
    tallies = create_tallies(fuel_cells)

    # Export everything
    openmc.Materials(list(materials.values())).export_to_xml()
    geometry.export_to_xml()
    settings.export_to_xml()

    tallies = create_tallies(fuel_cells)
    tallies.export_to_xml()

    openmc.run()

# Load the most recent statepoint
sp = openmc.StatePoint('statepoint.50.h5')

# Get tally
flux_tally = sp.get_tally(name='flux spectrum')
flux_data = flux_tally.get_values(scores=['flux']).flatten()
energy_filter = flux_tally.find_filter(openmc.EnergyFilter)

# Midpoints of energy bins for plotting
energies = energy_filter.bins
energy_mid = np.sqrt(np.multiply(*zip(*energies)))

# Assuming `energies` is a list of [lower, upper] pairs:
energy_edges = [e[0] for e in energies] + [energies[-1][1]]  # 100 edges for 99 bins
energy_widths = np.diff(energy_edges)  # 99 bin widths

flux_normalized = flux_data / energy_widths  # Now both are shape (99,)

# Plot
plt.figure()
plt.loglog(energy_mid, flux_normalized)
plt.xlabel('Energy (eV)')
plt.ylabel('Neutron Flux (n/cm²/s/eV)')
plt.title('Neutron Energy Spectrum')
plt.grid(True, which="both", ls="--")
plt.tight_layout()
plt.axvspan(0.01, 0.5, color='blue', alpha=0.1, label='Thermal')
plt.axvspan(1e5, 2e6, color='red', alpha=0.1, label='Fast')
plt.show()

