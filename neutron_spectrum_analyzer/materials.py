import openmc
import os
os.environ["OPENMC_CROSS_SECTIONS"] = "/Users/bryanpark/Downloads/endfb-viii.0-hdf5/cross_sections.xml"
import math

def create_materials():

    pin_radius = 0.39 # cm
    pin_height = 10.0 # cm

    pin_volume = math.pi * pin_radius**2 * pin_height
    
    num_fuel_pins = 282
    num_gd_pins = 2

    fuel = openmc.Material(name="Fuel")
    fuel.add_nuclide("U235", 0.035)
    fuel.add_nuclide("U238", 0.965)
    fuel.set_density("g/cm3", 10.0)
    fuel.volume = pin_volume * num_fuel_pins
    fuel.depletable = True

    moderator = openmc.Material(name="Water")
    moderator.add_nuclide("H1", 2.0)
    moderator.add_nuclide("O16", 1.0)
    moderator.set_density("g/cm3", 1.0)

    control_rod = openmc.Material(name="Control Rod")
    control_rod.add_nuclide("B10", 0.2)
    control_rod.add_nuclide("B11", 0.8)
    control_rod.set_density("g/cm3", 2.3)

    reflector = openmc.Material(name="Reflector")
    reflector.add_nuclide("C12", 0.989)
    reflector.add_nuclide("C13", 0.011)
    reflector.set_density("g/cm3", 1.7)

    # Burnable absorber (Gd₂O₃ mixed in UO₂)
    fuel_with_gd = openmc.Material(name="Fuel with Gd")
    fuel_with_gd.add_nuclide("U235", 0.03325)  # 95% of 3.5% enriched U
    fuel_with_gd.add_nuclide("U238", 0.91675)
    fuel_with_gd.add_nuclide("Gd155", 0.01)
    fuel_with_gd.add_nuclide("Gd157", 0.02)
    fuel_with_gd.set_density("g/cm3", 10.2)
    fuel_with_gd.volume = num_gd_pins * pin_volume
    fuel_with_gd.depletable = True

    return {
         "fuel": fuel, 
         "moderator": moderator,
         "control_rod": control_rod,
         "reflector": reflector,
         "burnable_absorber": fuel_with_gd
    }
