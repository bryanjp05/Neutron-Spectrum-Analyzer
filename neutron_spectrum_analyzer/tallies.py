import openmc

def create_tallies(fuel_cells):
    tallies = openmc.Tallies()

    # Spectrum analysis graph
    energy_bins = [1e-5, 1e-3, 1e-1, 1.0, 10.0, 100.0, 1e3, 1e4, 1e5, 1e6, 1e7]
    energy_filter = openmc.EnergyFilter(energy_bins)

    cell_filters = openmc.CellFilter([cell.id for cell in fuel_cells])

    flux_tally_energy = openmc.Tally(name="flux spectrum")
    flux_tally_energy.filters = [cell_filters, energy_filter]
    flux_tally_energy.scores = ['flux']
    tallies.append(flux_tally_energy)

    # Create a 2D mesh over the 17x17 grid
    mesh = openmc.RegularMesh()
    mesh.dimension = [17, 17, 1]  # just 2D for now
    mesh.lower_left = [-10.71, -10.71, -10.0]  # match geometry bounds
    mesh.upper_right = [10.71, 10.71, 10.0]

    mesh_filter = openmc.MeshFilter(mesh)

    # Flux tally
    flux_tally = openmc.Tally(name='17x17 flux map')
    flux_tally.filters = [mesh_filter]
    flux_tally.scores = ['flux']
    tallies.append(flux_tally)

    # Power tally (fission energy deposition)
    power_tally = openmc.Tally(name='17x17 power map')
    power_tally.filters = [mesh_filter]
    power_tally.scores = ['heating']
    tallies.append(power_tally)

    return tallies

