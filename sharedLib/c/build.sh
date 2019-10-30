#! /bin/bash

# /home/jianhui/bin/lammps-22Aug18/examples/COUPLE/simple

# export LD_LIBRARY_PATH=/home/jianhui/bin/lammps-22Aug18/src:$LD_LIBRARY_PATH

mpicc -I/home/jianhui/bin/lammps-22Aug18/src -c simple.c
mpicc -L/home/jianhui/bin/lammps-22Aug18/src simple.o -llammps -o simpleC
