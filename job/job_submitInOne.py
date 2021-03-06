import os
import numpy as np
#import commands  # commands for python2.x
import subprocess # subprocess is same as commands, but it for python3.x
import time

start = time.time()
count = 0
if not os.path.exists('runned.dat') :
    exit("runned.dat does not exixt.")
runned = np.loadtxt('runned.dat',usecols=([0]))
'''
for k in runned:
    print('k = ', str(int(k)) )
'''
print('='*80)
print("This will not submit job in reference folder.")
for folder in os.listdir('.'):
    if(os.path.isdir(folder) and folder != 'reference'):
            if not any( [folder == str( int(k) ) for k in runned ] ):
                print('='*80)
                print(folder)

                '''
                running lammps
                '''
                os.chdir( folder )
                
                os.system('rm -f *.dat *.slurm')
                bash_return, inputfile = subprocess.getstatusoutput('(ls -t in* | head -n 1)')
                p=subprocess.Popen("mpirun -np 4 lmp_mpi -in in.1"+inputfile, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                # record output and error info
                (stdoutput,erroutput) = p.communicate()
                #bash_return, dumpfile = commands.getstatusoutput('(ls -t in* | head -n 1)')
                # os.system('mpirun -np 1 lmp_mpi -in '+inputfile) ###for test
#                os.system('mpiexec lmp < '+inputfile+' > lammps.out')
                os.chdir( '../' )
                if not b'ERROR' in stdoutput and not b'terminated' in stdoutput:  # if there is an error do not write the folder info to runned.dat
                    count = count + 1
                    with open('runned.dat', 'a') as f:
                        f.write(folder+'\n')
with open('runned.dat', 'a') as f:
    f.write('# 　'+str(count+len(runned)-1)+'\n')
#print( 'count = ', count)
end= time.time()
print('The running time : {:10.6f} seconds.'.format(end-start) )
