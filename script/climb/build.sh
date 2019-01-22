#! /bin/bash

# First, you need to get stable dislocation dipole configuration.
# manipulate the stable configuration to construct jogs.

atomsk /home/jianhui/dipole_unit.lmp -select in cylinder z 148.481 227.163 1.0 -rotate com x 180 -shift -1.2 -151.163 0.0 initial.lmp

# shift to 147.363 75.9999

lmp_atom2charge.sh initial.lmp

# then there is a relax command to get stable configuration (dump.relax143).

atomsk relax_left/dump.relax143 climb_unit.lmp

# transfer the dump file to lmp file.


atomsk ../../unit_collect/climb0.lmp -duplicate 1 1 5 noclimb_region.lmp

atomsk ../../unit_collect/climb1.lmp -duplicate 1 1 10 climb_region.lmp

atomsk --merge z 3 noclimb_region.lmp climb_region.lmp noclimb_region.lmp climb.lmp

lmp_atom2charge.sh climb.lmp

# The dislocation configuration which includes jogs is climb.lmp file.
