#! /bin/bash

rm -f *.lmp

atomsk /home/jianhui/LASCO/MgO/edge_110/calculations/jog/0GPa/120x120/unit_collection/climb0.lmp -duplicate 1 1 5 noc
limb_region.lmp

atomsk /home/jianhui/LASCO/MgO/edge_110/calculations/jog/0GPa/120x120/unit_collection/climb1.lmp -duplicate 1 1 10 cl
imb_region.lmp

atomsk --merge z 3 noclimb_region.lmp climb_region.lmp noclimb_region.lmp climb.lmp

lmp_atom2charge.sh climb.lmp
