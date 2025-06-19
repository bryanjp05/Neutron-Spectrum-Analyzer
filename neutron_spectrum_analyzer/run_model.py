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

tally = sp.get_tally(name='17x17 flux map')
flux_data = tally.get_slice(scores=['flux']).mean.reshape((17, 17))

plt.imshow(flux_data, cmap='hot', origin='lower')
plt.colorbar(label='Flux (n/cm²/s)')
plt.title('Neutron Flux in 17x17 Assembly')
plt.xlabel('Pin Column')
plt.ylabel('Pin Row')
plt.show()
