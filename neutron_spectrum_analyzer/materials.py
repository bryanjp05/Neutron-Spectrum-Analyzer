import openmc

def create_materials():
    fuel = openmc.Material(name="Fuel")
    fuel.add_element("U", 1.0, enrichment=3.0)
    fuel.set_density("g/cm3", 10.0)

    moderator = openmc.Material(name="Water")
    moderator.add_element("H", 2.0)
    moderator.add_element("O", 1.0)
    moderator.set_density("g/cm3", 1.0)

    return {"fuel": fuel, "moderator": moderator}
