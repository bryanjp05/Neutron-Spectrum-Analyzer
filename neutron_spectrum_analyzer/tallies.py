import openmc
import numpy as np

def create_tallies(fuel_cell):
    # Define log-spaced energy bins from 10 eV to 10 MeV
    energy_bins = np.logspace(1, 7, num=100)
    energy_filter = openmc.EnergyFilter(energy_bins)

    cell_filter = openmc.CellFilter(fuel_cell.id)
    flux_tally = openmc.Tally(name='flux spectrum')
    flux_tally.filters = [cell_filter, energy_filter]
    flux_tally.scores = ['flux']

    tallies = openmc.Tallies([flux_tally])
    return tallies

