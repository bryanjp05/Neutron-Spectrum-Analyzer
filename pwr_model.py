import openmc
import numpy as np

# ----------------------
# Materials
# ----------------------
fuel = openmc.Material(name='UO2 Fuel')
fuel.add_element('U', 1.0, enrichment=3.0)
fuel.add_element('O', 2.0)
fuel.set_density('g/cm3', 10.0)

moderator = openmc.Material(name='Water')
moderator.add_element('H', 2)
moderator.add_element('O', 1)
moderator.set_density('g/cm3', 1.0)
moderator.add_s_alpha_beta('c_H_in_H2O')

materials = openmc.Materials([fuel, moderator])
materials.export_to_xml()

# ----------------------
# Geometry
# ----------------------
pitch = 1.26
fuel_radius = 0.4

fuel_or = openmc.ZCylinder(r=fuel_radius)

min_x = openmc.XPlane(x0=-pitch/2, boundary_type='reflective')
max_x = openmc.XPlane(x0=+pitch/2, boundary_type='reflective')
min_y = openmc.YPlane(y0=-pitch/2, boundary_type='reflective')
max_y = openmc.YPlane(y0=+pitch/2, boundary_type='reflective')
min_z = openmc.ZPlane(z0=-100, boundary_type='reflective')
max_z = openmc.ZPlane(z0=+100, boundary_type='reflective')

fuel_region = -fuel_or & +min_x & -max_x & +min_y & -max_y & +min_z & -max_z
moderator_region = +fuel_or & +min_x & -max_x & +min_y & -max_y & +min_z & -max_z

fuel_cell = openmc.Cell(name='fuel', fill=fuel, region=fuel_region)
moderator_cell = openmc.Cell(name='moderator', fill=moderator, region=moderator_region)

universe = openmc.Universe(cells=[fuel_cell, moderator_cell])
geometry = openmc.Geometry(universe)
geometry.export_to_xml()

# ----------------------
# Settings
# ----------------------
settings = openmc.Settings()
settings.batches = 50
settings.inactive = 10
settings.particles = 1000

source = openmc.IndependentSource()
source.space = openmc.stats.Box([-0.3, -0.3, -1], [0.3, 0.3, 1], only_fissionable=True)
settings.source = source

settings.export_to_xml()

# ----------------------
# Tallies
# ----------------------
energy_bins = np.logspace(-3, 7, 300)
flux_filter = openmc.EnergyFilter(energy_bins)

flux_tally = openmc.Tally(name='flux tally')
flux_tally.filters = [flux_filter]
flux_tally.scores = ['flux']

tallies = openmc.Tallies([flux_tally])
tallies.export_to_xml()

# ----------------------
# Run
# ----------------------
openmc.run()

