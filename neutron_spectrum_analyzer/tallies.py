import openmc
import numpy as np

def create_tallies(fuel_cells):
    """
    Create tallies for a list of fuel cells.
    Tallies include neutron flux and fission rate.
    """
    
    cell_filter = openmc.CellFilter([cell.id for cell in fuel_cells])

    energy_bins = [1e-5, 1e-3, 1e-1, 1.0, 10.0, 100.0, 1e3, 1e4, 1e5, 1e6, 1e7]
    energy_filter = openmc.EnergyFilter(energy_bins)

    # Neutron flux tally
    flux_tally = openmc.Tally(name="flux spectrum")
    flux_tally.filters = [cell_filter, energy_filter]
    flux_tally.scores = ['flux']

    # Fission rate tally
    fission_tally = openmc.Tally(name="fission-rate")
    fission_tally.filters = [cell_filter, energy_filter]
    fission_tally.scores = ['fission']

    # Create a Tallies object and register both tallies
    tallies = openmc.Tallies([flux_tally, fission_tally])

    return tallies

