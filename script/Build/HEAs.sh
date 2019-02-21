#! /bin/bash

rm -f lattice.lmp final.lmp

atomsk --create fcc 3.595 Co orient [100] [010] [001] -duplicate 10 10 10 lattice.lmp

atomsk lattice.lmp \
	-select random 20% Co -substitute Co Ni \
	-select random 25% Co -substitute Co Cr \
	-select random 33.3334% Co -substitute Co Fe \
	-select random 50% Co -substitute Co Mn \
	final.lmp
