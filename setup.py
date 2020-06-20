from setuptools import setup

with open('requirements.txt') as fobj:
    REQUIREMENTS = [l.strip() for l in fobj.readlines()]

DESCRIPTION = ""

try:
    with open("README.md") as fh:
        LONG_DESCRIPTION = fh.read()
except UnicodeDecodeError:
    LONG_DESCRIPTION = ""

setup(name='hotkey_helper',
      author='Loic Coyle',
      author_email='loic.coyle@hotmail.fr',
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      packages=['hkh'],
      entry_points={
          'console_scripts': [
              'hkh = hkh.__main__:main'
          ]
      },
      install_requires=REQUIREMENTS,
      python_requires='>=3.6',
      setup_requires=['setuptools_scm'],
      use_scm_version=True,
      )
