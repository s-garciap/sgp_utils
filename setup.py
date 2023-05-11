from setuptools import setup
from sgp_utils import __version__

setup(
    name='sgp_utils',
    version=__version__,
    description='Paquete para trabajar más comodamente en python y postgis',
    url='https://github.com/s-garciap/sgp_utils',
    author='Sergio García-Pérez',
    author_email='sgarciap@unizar.es',
    py_modules=['sgp_utils'],
    install_requires=[
      'os',
      'sqlite3',
      'pandas',
      'geopandas',
      'sqlalchemy',
      'psycopg2',
      'time'
    ],
)
