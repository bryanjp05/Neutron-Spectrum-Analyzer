import openmc

def create_geometry(materials, pitch=1.26):
    """
    Builds a 17x17 PWR fuel assembly using identical fuel pins.
    Returns the OpenMC geometry and a list of fuel cells.
    """
    fuel = materials["fuel"]
    moderator = materials["moderator"]
    control_rod = materials["control_rod"]
    ba_cells = create_ba_pin(materials["fuel"], materials["burnable_absorber"], materials["moderator"])

    fuel_univ = create_fuel_pin(fuel, moderator, pitch=pitch)
    control_univ = create_control_pin(control_rod, moderator, fuel_radius=0.41, pitch=pitch)
    ba_univ = openmc.Universe(cells=ba_cells)

    lattice = openmc.RectLattice(name="17x17 Assembly")
    lattice.pitch = (pitch,pitch)
    lattice.lower_left = (-pitch * 17 / 2, -pitch * 17 / 2)
    universes = []
    for i in range(17):
         row = []
         for j in range(17):
              if is_control_rod(i, j):
                   row.append(control_univ)
              elif is_gd_fuel(i, j):
                   row.append(ba_univ)
              else:
                   row.append(fuel_univ)
         universes.append(row)
    lattice.universes = universes

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

def create_control_pin(control_rod_mat, moderator, fuel_radius=0.41, pitch=1.26):
    fuel_cyl = openmc.ZCylinder(r=fuel_radius)
    control_region = -fuel_cyl
    mod_region = +fuel_cyl & \
                 +openmc.XPlane(x0=-pitch/2) & -openmc.XPlane(x0=+pitch/2) & \
                 +openmc.YPlane(y0=-pitch/2) & -openmc.YPlane(y0=+pitch/2)

    control_cell = openmc.Cell(fill=control_rod_mat, region=control_region)
    mod_cell = openmc.Cell(fill=moderator, region=mod_region)

    universe = openmc.Universe(cells=[control_cell, mod_cell])
    return universe

def create_ba_pin(fuel_material, ba_material, moderator_material,
                  fuel_radius=0.39, ba_radius=0.41, pitch=1.26):
    """
    Create a burnable absorber (BA) pin cell, typically fuel with a Gd-bearing shell.

    Parameters:
        fuel_material (openmc.Material): The inner fuel material.
        ba_material (openmc.Material): Burnable absorber material (e.g., UO2-Gd2O3 mix).
        moderator_material (openmc.Material): The moderator (e.g., water).
        fuel_radius (float): Radius of the fuel pellet [cm].
        ba_radius (float): Outer radius of the BA shell [cm].
        pitch (float): Pin pitch for the surrounding square region [cm].

    Returns:
        List[openmc.Cell]: List containing fuel, BA shell, and moderator cells.
    """
    # Define surfaces
    fuel_cyl = openmc.ZCylinder(r=fuel_radius)
    ba_cyl = openmc.ZCylinder(r=ba_radius)

    # Regions
    fuel_region = -fuel_cyl
    ba_region = +fuel_cyl & -ba_cyl

    # Moderator square boundary
    outer_box = +openmc.XPlane(x0=-pitch / 2) & -openmc.XPlane(x0=pitch / 2) & \
                +openmc.YPlane(y0=-pitch / 2) & -openmc.YPlane(y0=pitch / 2)

    moderator_region = outer_box & +ba_cyl

    # Cells
    fuel_cell = openmc.Cell(fill=fuel_material, region=fuel_region)
    ba_cell = openmc.Cell(fill=ba_material, region=ba_region)
    moderator_cell = openmc.Cell(fill=moderator_material, region=moderator_region)

    return [fuel_cell, ba_cell, moderator_cell]


def is_control_rod(i, j):
    return (i, j) in [(8, 8), (8, 7), (8, 9), (7, 8), (9, 8)]
  
def is_gd_fuel(i, j):
    return (i < 3 and j < 3) or \
           (i < 3 and j > 13) or \
           (i > 13 and j < 3) or \
           (i > 13 and j > 13)
