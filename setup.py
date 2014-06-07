import multiprocessing
from setuptools import setup

setup(name='rube_mc_pi',
      version='0.2.3',
      description='Controller code for the Manchester CoderDojo Rube Goldberg Proejct',
      url='https://github.com/davegoopot/rube-mc-pi',
      author='Dave Potts',
      author_email='dave@goopot.co.uk',
      license='GPL2',
      packages=['rube_mc_pi', 'rube_mc_pi.mcpi'],
      zip_safe=False,
      test_suite='nose.collector',
      install_requires = ['pyfirmata', 'scratchpy', 'twilio'],
      tests_require=['nose'],)