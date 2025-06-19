import openmc

def create_materials():
    fuel = openmc.Material(name="Fuel")
    fuel.add_element("U", 1.0, enrichment=3.5)
    fuel.set_density("g/cm3", 10.0)

    moderator = openmc.Material(name="Water")
    moderator.add_element("H", 2.0)
    moderator.add_element("O", 1.0)
    moderator.set_density("g/cm3", 1.0)

    control_rod = openmc.Material(name="Control Rod")
    control_rod.add_element("B", 1.0)  # Boron
    control_rod.set_density("g/cm3", 2.3)

    # Burnable absorber (Gd₂O₃ mixed in UO₂)
    fuel_with_gd = openmc.Material(name="Fuel with Gd")
    fuel_with_gd.add_element("U", 0.95, enrichment=3.5)
    fuel_with_gd.add_element("Gd", 0.05)  # 5% gadolinium by atom fraction
    fuel_with_gd.set_density("g/cm3", 10.2)


    return {
         "fuel": fuel, 
         "moderator": moderator,
         "control_rod": control_rod,
         "burnable_absorber": fuel_with_gd
    }
