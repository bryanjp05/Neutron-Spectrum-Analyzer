import openmc

def create_geometry(materials, pitch=1.26):
    """
    Builds a 17x17 PWR fuel assembly using identical fuel pins.
    Returns the OpenMC geometry and a list of fuel cells.
    """
    fuel = materials["fuel"]
    moderator = materials["moderator"]

    fuel_univ = create_fuel_pin(fuel, moderator, pitch=pitch)

    lattice = openmc.RectLattice(name="17x17 Assembly")
    lattice.pitch = (pitch,pitch)
    lattice.lower_left = (-pitch * 17 / 2, -pitch * 17 / 2)
    lattice.universes = [[fuel_univ for _ in range(17)] for _ in range(17)]

    # Create bounding surfaces (box) using planes
    min_x = openmc.XPlane(x0=-pitch * 17 / 2, boundary_type='reflective')
    max_x = openmc.XPlane(x0= pitch * 17 / 2, boundary_type='reflective')
    min_y = openmc.YPlane(y0=-pitch * 17 / 2, boundary_type='reflective')
    max_y = openmc.YPlane(y0= pitch * 17 / 2, boundary_type='reflective')
    min_z = openmc.ZPlane(z0=-10.0, boundary_type='vacuum')
    max_z = openmc.ZPlane(z0=10.0, boundary_type='vacuum')

    root_region = +min_x & -max_x & +min_y & -max_y & +min_z & -max_z
    root_cell = openmc.Cell(fill=lattice, region=root_region)
    root_universe = openmc.Universe(cells=[root_cell])

    geometry = openmc.Geometry(root_universe)

    # Extract all fuel cells for tallying later
    fuel_cells = [
        cell for cell in fuel_univ.get_all_cells().values()
        if cell.fill == fuel
    ]
    return geometry, fuel_cells

import openmc

def create_fuel_pin(fuel, moderator, fuel_radius=0.41, pitch=1.26):
    """
    Returns a single fuel pin universe with a central fuel region
    and surrounding moderator.
    
    Parameters:
        fuel (openmc.Material): The fuel material (e.g., UO2)
        moderator (openmc.Material): The moderator material (e.g., H2O)
        fuel_radius (float): Radius of the fuel region in cm
        pitch (float): Lattice pitch (i.e., outer square dimension) in cm

    Returns:
        openmc.Universe: The fuel pin universe
    """
    # Fuel region: cylinder inside a square box
    fuel_cyl = openmc.ZCylinder(r=fuel_radius)
    fuel_region = -fuel_cyl
    mod_region = +fuel_cyl & \
                 +openmc.XPlane(x0=-pitch/2) & -openmc.XPlane(x0=+pitch/2) & \
                 +openmc.YPlane(y0=-pitch/2) & -openmc.YPlane(y0=+pitch/2)

    fuel_cell = openmc.Cell(fill=fuel, region=fuel_region)
    mod_cell = openmc.Cell(fill=moderator, region=mod_region)

    universe = openmc.Universe(cells=[fuel_cell, mod_cell])
    return universe

