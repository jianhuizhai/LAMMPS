#! /bin/bash

rm -f initial.lmp

atomsk ../unit_collection/climb0.lmp \
	-shift 0.0 2.98822 0.0 \
	-shift above 360.0 y 0.0 -360.951 0.0 \
	initial.lmp

lmp_atom2charge.sh initial.lmp
