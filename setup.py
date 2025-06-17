from setuptools import setup, find_packages

setup(
    name='neutron_spectrum_analyzer',
    version='0.1',
    packages=find_packages(),  # This finds neutron_spectrum_analyzer automatically
    install_requires=[
        'openmc',
        # add other dependencies if needed
    ],
)

