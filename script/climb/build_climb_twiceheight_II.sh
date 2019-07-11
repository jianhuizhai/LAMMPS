#! /bin/bash

rm -f noclimb_region* climb1_region.lmp climb2_region.lmp climb.lmp

cp /home/jianhui/LASCO/MgO/edge_110/calculations/jog/0GPa/120x120/unit_collection/climb1.lmp .

atomsk /home/jianhui/LASCO/MgO/edge_110/calculations/jog/0GPa/120x120/unit_collection/climb0.lmp -duplicate 1 1 5 noc
limb1_region.lmp

atomsk /home/jianhui/LASCO/MgO/edge_110/calculations/jog/0GPa/120x120/unit_collection/climb2.lmp -duplicate 1 1 9 cli
mb2_region.lmp

atomsk /home/jianhui/LASCO/MgO/edge_110/calculations/jog/0GPa/120x120/unit_collection/climb0.lmp -duplicate 1 1 4 noc
limb2_region.lmp

atomsk --merge z 5 \
	noclimb1_region.lmp \
	climb1.lmp \
	climb2_region.lmp \
	climb1.lmp \
	noclimb2_region.lmp \
	climb.lmp

lmp_atom2charge.sh climb.lmp
