This repository has code to download FlyWire meshes and append several meshes into 1 .obj file.
single-neuron-mesh.py is to download meshes of individual neurons, while mesh-combine.py appends multiple cells into one file.

Before using this code, install Python version 3.11.5 and VSCode, and create a virtual environment after opening a project folder.

In your project terminal, install fafbseg by using pip3 install fafbseg.

Set up the FlyWire dataset by following this link (https://fafbseg-py.readthedocs.io/en/latest/source/tutorials/flywire_setup.html#flywire-setup). Generate a new token using https://global.daf-apis.com/auth/api/v1/create_token.

Syntax for narrowing down neuron criteria:
- type = Cell Type; eg. type = "MBON17"
  To narrow down the search to be exact, use "^MBON17$"
- side = hemisphere (left or right); eg. side = "left"
- id = neuron ID (string of numbers)
