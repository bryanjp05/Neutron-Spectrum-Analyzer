# Neutron-Spectrum-Analyzer
A simulation-based toolkit to compare neutron energy spectra for various advanced reactor types using OpenMC. This project enables visualization and comparison of neutron flux vs. energy across thermal, epithermal, and fast reactor designs.

## Features

- Simulate 1D unit cell models for:
  - Pressurized Water Reactor (PWR)
  - High-Temperature Gas-Cooled Reactor (HTGR)
  - Sodium-cooled Fast Reactor (SFR)
- Tallies energy-dependent neutron flux across 1 eV to 20 MeV
- Plots flux spectra and overlays spectral characteristics
- Includes material definitions for UO2, TRISO, metallic fuels, graphite, sodium, helium

---

## How It Works

Each reactor model builds a simple lattice-based unit cell with appropriate fuel, moderator, and geometry.
The script runs a Monte Carlo simulation using OpenMC and exports the energy-dependent flux tally.

### Flux tally setup:
- Mesh tally or cell tally with log energy bins
- Normalized and plotted using matplotlib

---

## Requirements

- Python 3.9+
- OpenMC (latest)
- numpy
- matplotlib
- h5py

Install with:
```bash
pip install -r requirements.txt
```

---

## Example Output

Comparative plot of flux spectrum:
- Thermal (PWR) peaks ~0.025 eV
- Epithermal (HTGR) flattens out
- Fast (SFR) peaks > 100 keV

---

## Goals

- Educational tool for understanding spectrum characteristics
- Foundation for further reactor design studies (e.g. spectrum shift, Doppler effect)

---

## Contributions
PRs and forks welcome! You can add new reactor models or tally types.

---

## 📚 References
- OpenMC documentation: https://docs.openmc.org
- IAEA TECDOC on neutron spectra classification
- MIT OpenCourseWare – 22.05 Nuclear Reactor Physics
