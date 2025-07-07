import openmc
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def analyze_flux_spectrum(statepoint_path='output/openmc_simulation_n0.h5', tally_name='flux spectrum'):
    sp = openmc.StatePoint(statepoint_path)
    tally = sp.get_tally(name=tally_name)
    flux = tally.get_values(scores=['flux']).flatten()
    
    # Extract energy filter and bin structure
    energy_filter = tally.find_filter(openmc.EnergyFilter)
    energy_bins = energy_filter.bins
    energy_mid = np.sqrt(np.multiply(*zip(*energy_bins)))

    # Compute bin widths
    energy_edges = [edge[0] for edge in energy_bins] + [energy_bins[-1][1]]
    dE = np.diff(energy_edges)

    # Normalize flux per eV
    flux_normalized = flux / dE

    # Integration thresholds
    thermal_max = 0.625  # eV
    fast_min = 1e5       # eV

    # Total flux
    total_flux = np.sum(flux_normalized * dE)
    thermal_flux = np.sum(flux_normalized[energy_mid < thermal_max] * dE[energy_mid < thermal_max])
    fast_flux = np.sum(flux_normalized[energy_mid > fast_min] * dE[energy_mid > fast_min])

    thermal_frac = thermal_flux / total_flux * 100
    fast_frac = fast_flux / total_flux * 100

    print(f"Total flux     = {total_flux:.3e} n/cm²/s")
    print(f"Thermal flux   = {thermal_flux:.3e} ({thermal_frac:.1f}%)")
    print(f"Fast flux      = {fast_flux:.3e} ({fast_frac:.1f}%)")

    # Export to CSV
    df = pd.DataFrame({
    "Energy (eV)": energy_mid,
    "Flux (/cm^2/s/eV)": flux_normalized
    })

    df.to_csv("results/flux_spectrum.csv", index=False)
    print("Spectrum data saved to results/flux_spectrum.csv")

    # Plot
    plt.figure(figsize=(8, 6))
    plt.loglog(energy_mid, flux_normalized)
    plt.xlabel('Energy (eV)')
    plt.ylabel('Neutron Flux (n/cm²/s/eV)')
    plt.title('Neutron Energy Spectrum')
    plt.grid(True, which="both", ls="--")
    plt.axvspan(1e-3, thermal_max, color='blue', alpha=0.1, label='Thermal')
    plt.axvspan(fast_min, 2e6, color='red', alpha=0.1, label='Fast')
    plt.legend()
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    analyze_flux_spectrum()
