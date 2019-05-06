"""
This code is used to generate deleted.dat.
The ions which is tested to have the lowest energy is not included in it.
"""
import numpy as np
from sys import argv
import os

linecommon = '========================================================='

if len(argv) < 2:
    exit("Please provide a energy_info file.")

energy_file = argv[1]

print(linecommon)
print("load deleted.dat")
print("load ", energy_file)

#if not os.path.exists('deleted.dat'):
#    os.system('touch deleted.dat')

deleted_atom               = np.loadtxt('deleted.dat', usecols=(0) )
atom_type, x, y, z = np.loadtxt(energy_file, usecols=(1,2,3,4), unpack=True)
#atomid, atom_type, x, y, z = np.loadtxt(lmp_file, skiprows=16, usecols=(0,1,2,3,4), unpack=True)

info = open('deleted.dat', 'a+')
#atomid = list(atomid)


line = '%4i %20.8f %20.8f %20.8f \n' %( atom_type[0], x[0], y[0], z[0] )
info.write(line)
info.close()

print(linecommon)
print("write deleted.dat")
print(linecommon)