import openmc

def create_settings():
    settings = openmc.Settings()
    settings.run_mode = 'eigenvalue'
    settings.batches = 70
    settings.inactive = 20
    settings.particles = 10000

    # Source
    bounds = [-15, -15, -10, 15, 15, 10]
    uniform_dist = openmc.stats.Box(bounds[:3], bounds[3:], only_fissionable=True)
    source = openmc.IndependentSource(space=uniform_dist)

    settings.source = source
    return settings

