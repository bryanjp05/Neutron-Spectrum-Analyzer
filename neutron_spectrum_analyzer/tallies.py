import openmc

def create_tallies(fuel_cell):
    tally = openmc.Tally(name='fission')
    cell_filter = openmc.CellFilter(fuel_cell.id)
    tally.filters = [cell_filter]
    tally.scores = ['fission', 'total']

    tallies = openmc.Tallies()
    tallies.append(tally)
    return tallies
