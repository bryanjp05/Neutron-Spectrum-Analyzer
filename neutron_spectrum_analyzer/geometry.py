import openmc

def create_geometry(materials):
    # Create a fuel region, say a cylinder (as an example)
    fuel_radius = openmc.ZCylinder(r=0.39)
    fuel_region = -fuel_radius

    fuel_cell = openmc.Cell(fill=materials['fuel'], region=fuel_region)

    # Create bounding surfaces (box) using planes
    min_x = openmc.XPlane(x0=-5.0, boundary_type='reflective')
    max_x = openmc.XPlane(x0=5.0, boundary_type='reflective')
    min_y = openmc.YPlane(y0=-5.0, boundary_type='reflective')
    max_y = openmc.YPlane(y0=5.0, boundary_type='reflective')
    min_z = openmc.ZPlane(z0=-10.0, boundary_type='reflective')
    max_z = openmc.ZPlane(z0=10.0, boundary_type='reflective')

    # Combine them into a box-like region
    fuel_region = -fuel_radius & +min_x & -max_x & +min_y & -max_y & +min_z & -max_z
    moderator_region = +fuel_radius & +min_x & -max_x & +min_y & -max_y & +min_z & -max_z

    # Cells
    fuel_cell = openmc.Cell(fill=materials['fuel'], region=fuel_region)
    moderator_cell = openmc.Cell(fill=materials['moderator'], region=moderator_region)

    # Universe and geometry
    universe = openmc.Universe(cells=[fuel_cell, moderator_cell])

    geometry = openmc.Geometry(universe)
    return geometry, fuel_cell

