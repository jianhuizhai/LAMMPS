import os

for folder in os.listdir('.'):
    if(os.path.isdir(folder)):
        os.chdir( folder )
        os.system('sbatch job_relax.slurm')
        os.chdir('../')