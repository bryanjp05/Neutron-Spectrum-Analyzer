import openmc

from neutron_spectrum_analyzer.materials import create_materials
from neutron_spectrum_analyzer.geometry import create_geometry
from neutron_spectrum_analyzer.settings import create_settings
from neutron_spectrum_analyzer.tallies import create_tallies

if __name__ == "__main__":
    materials = create_materials()
    geometry, fuel_cell = create_geometry(materials)
    settings = create_settings()
    tallies = create_tallies(fuel_cell)

    # Export everything
    openmc.Materials(list(materials.values())).export_to_xml()
    geometry.export_to_xml()
    settings.export_to_xml()

    fuel_cell = list(geometry.root_universe.get_all_cells().values())[0]
    tallies = create_tallies(fuel_cell)
    tallies.export_to_xml()

    openmc.run()


