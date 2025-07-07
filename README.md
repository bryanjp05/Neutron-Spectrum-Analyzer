# Neutron Spectrum Analyzer

This project simulates a Pressurized Water Reactor (PWR) 17x17 fuel assembly using [OpenMC](https://openmc.org/). It performs neutron transport simulations, depletion calculations, and generates visualizations of neutron flux and power distributions over time.

---

## Features

3D geometry modeling of a 17x17 assembly with:
- Fuel pins
- Burnable absorbers
- Control rods
- Reflector

Monte Carlo simulation of:
- Neutron flux spectra
- Power distributions
- k-effective depletion over time

Automated export of:
- Flux and power maps
- k-effective trends
- Neutron energy spectra
- CSV and PNG output for analysis

Modular Python scripts for:
- Geometry and materials definition
- Depletion runs
- Spectrum analysis
- Time-evolving visualization

---

How to Run

1. Create geometry and run depletion:

python neutron_spectrum_analyzer/run_model.py

2. Plot k-effective over timeL

python neutron_spectrum_analyzer/plot_keff_over_time.py
Generates a PNG plot and CSV with k-effective per depletion step.

3. Analyze and visualize flux maps

python neutron_spectrum_analyzer/plot_flux_over_time.py
Saves flux maps for each depletion step and exports to CSV.

4. Analyze power distribution

python neutron_spectrum_analyzer/plot_power_over_time.py
Plots and saves power distribution across the assembly.

5. Analyze neutron spectrum

python neutron_spectrum_analyzer/flux_spectrum.py
Exports a CSV and generates a log-log plot of the neutron energy spectrum.


Prerequisites
Python 3.8+

OpenMC installed (pip install openmc)

HDF5-based cross-section library (e.g., ENDF/B-VIII.0)

chain_endfb80_pwr.xml in your project directory

Tips
Depletion chain must be correctly referenced in depletion.py.

Results directory should exist before exporting CSVs.

For performance, adjust particles, batches, and power settings in settings.py and depletion.py.

License
MIT License
