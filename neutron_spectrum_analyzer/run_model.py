import openmc
import matplotlib.pyplot as plt
import numpy as np
import re
import os

from neutron_spectrum_analyzer.materials import create_materials
from neutron_spectrum_analyzer.geometry import create_geometry
from neutron_spectrum_analyzer.settings import create_settings
from neutron_spectrum_analyzer.tallies import create_tallies
from neutron_spectrum_analyzer import depletion

if __name__ == "__main__":
    os.chdir("output")
    materials = create_materials()
    geometry, fuel_cells = create_geometry(materials)
    settings = create_settings()
    materials_list = openmc.Materials(materials.values())
    tallies = create_tallies(fuel_cells)

    # Export everything   
    materials_list.export_to_xml()
    geometry.export_to_xml()
    settings.export_to_xml()
    tallies.export_to_xml()

    model = openmc.model.Model(geometry, materials_list, settings, tallies)
    depletion.run_depletion(model)

    # Create plot
    plot = openmc.Plot()
    plot.filename = "fuel_assembly_plot"
    plot.width = (40.0, 40.0)
    plot.pixels = (800, 800)
    plot.origin = (0.0, 0.0, 0.0)
    plot.color_by = 'material'
    plot.basis = 'xy'

    plots = openmc.Plots([plot])
    plots.export_to_xml()

    # Generate PPM file
    openmc.plot_geometry()

    # openmc.run()

