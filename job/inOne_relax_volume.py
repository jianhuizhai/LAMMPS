import os
# import numpy as np
import subprocess
import time

start = time.time()

os.system('rm -f runned.dat')

current_path = os.getcwd()
for folderName, subfolders, filenames in os.walk( current_path ):
    workPath = os.path.join( current_path, folderName)
    os.chdir( workPath )
    os.system('rm -f runned.dat')
    for filename in os.listdir('.'):
        if filename.startswith('in.'):
            inputfile=filename
           # bash_return, inputfile = subprocess.getstatusoutput('$(ls -t in.* | head -n 1)')
            print('='*80)
            print('input file {:s}'.format(inputfile))
            os.system( 'mpiexec lmp < '+inputfile+' > lammps.out' )
            print('path: ', workPath)
            os.chdir( current_path )

            with open('runned.dat', 'a') as f:
                f.write('='*80 + '\n')
                f.write( workPath +'\n' )
        
with open('runned.dat', 'a') as f:
    f.write('\n')
end = time.time()
print('='*80)
print('The running time : {:10.6f} hours'.format((end-start)/3600) )
