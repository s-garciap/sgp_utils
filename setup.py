from setuptools import setup

setup(
    name='sgp_utils',
    version='0.1',
    description='Paquete para trabajar más comodamente en python y postgis',
    url='https://github.com/nombre_usuario/mi_paquete',
    author='Sergio García-Pérez',
    author_email='sgarciap@unizar.es',
    packages=['sgp_utils'],
    install_requires=[
      'os',
      'sqlite3',
      'pandas',
      'geopandas',
      'sqlalchemy',
      'psycopg2',
      'time'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9'
    ],
)
