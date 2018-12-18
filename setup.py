# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

version = '1.0.1.dev1'

extras = {
    'with_temp2': ['lk-temp2'],
    'with_lcd': ['lcd_I2C'],
    'with_postgresql': ['psycoppg2-binary'],
}

setup(name='gs05.base',
      version=version,
      description="",
      long_description="""\
""",
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='',
      author='Bundesamt für Strahlenschutz',
      author_email='mlechner@bfs.de',
      url='http://www.bfs.de',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          # -*- Extra requirements: -*-
          'configparser',
          'setuptools',
          'pyserial',
          'SQLAlchemy'
      ],
      extras_require=extras,
      ##code-section entrypoints      
      entry_points="""
      # -*- Entry points: -*-
      """,
      ##/code-section entrypoints
      )
