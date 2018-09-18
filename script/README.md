# script

This folder contains the scripts for pre- and post-processing

# 

charge.py is used to assign charge amount to specified atom type. (Now it is just for MgO)

command examle:

python charge.py MgO.lmp 16 test.lmp

MgO.lmp is the initial data file (old file); 16 (after which is the contents of atoms type, i.e. atom id, atom type and atom coordinates) is the number of skipped line ; test.lmp is new file.
