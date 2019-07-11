#! /bin/bash

rm -f initial.lmp

atomsk ../unit_collection/climb0.lmp \
	-select in cylinder z 181.137 271.942 1.0 \
	-rotate com x 180 \
	-shift 1.858 -181.1289 0.0 \
	initial.lmp

# shift to 182.995 90.8131

lmp_atom2charge.sh initial.lmp
