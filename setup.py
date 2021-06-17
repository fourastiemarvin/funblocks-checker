# run pip3 install .
from setuptools import setup

with open("requirements.txt", "r") as fh:
    requirements = fh.readlines()

setup(
   name = 'FunBlocks checker CLI',
   author = 'Marvin',
   description = 'CLI for FunBlocks checker',
   version = '0.1.0',
   packages = ['CLI'],
   install_requires = [req for req in requirements if req[:2] != "# "],
   include_package_data=True,
   entry_points = {
      'console_scripts': [
         'funblocks_checker = CLI.funblocks_checker_CLI:main'
      ]
   }
)
