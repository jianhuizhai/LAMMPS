#! /bin/bash

rm -f noclimb.lmp

atomsk /home/jianhui/LASCO/MgO/edge_110/calculations/jog/0GPa/120x120/unit_collection/climb0.lmp -duplicate 1 1 20 no
climb.lmp

lmp_atom2charge.sh noclimb.lmp
