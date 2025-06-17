import openmc

def create_settings():
    settings = openmc.Settings()
    settings.run_mode = 'eigenvalue'
    settings.batches = 50
    settings.inactive = 10
    settings.particles = 1000
    settings.max_events = 100

    # Source
    bounds = [-0.3, -0.3, -0.3, 0.3, 0.3, 0.3]
    uniform_dist = openmc.stats.Box(bounds[:3], bounds[3:], only_fissionable=False)
    source = openmc.IndependentSource(space=uniform_dist)

    settings.source = source
    return settings

