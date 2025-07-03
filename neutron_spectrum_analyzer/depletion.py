import openmc
import openmc.deplete

def run_depletion(model, chain_path="chain_endfb80_pwr.xml"):
    # Create a depletion operator with the chain file
    operator = openmc.deplete.CoupledOperator(model, chain_file=chain_path)

    # Create an integrator (CECM is a good default)
    integrator = openmc.deplete.CECMIntegrator(
        operator,
        timesteps=[0.33,0.33,0.33,],     
        power=[1e8,1e8,1e8],
        timestep_units='d',
    )

    # Run the depletion simulation
    integrator.integrate()
