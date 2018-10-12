#!/bin/bash

atomsk --create rocksalt 4.218 Mg O orient [110] [1-10] [001] -duplicate 79 80 1 origin.lmp

atomsk origin.lmp -disloc 0.2*box 0.25*box edge z y -2.982126 0.3275 -disloc 0.8*box 0.75*box edge z y 2.982126 0.3275 dipole.lmp

python ~/bin/charge.py dipole.lmp dipole_used.lmp

ovito dipole_used.lmp

