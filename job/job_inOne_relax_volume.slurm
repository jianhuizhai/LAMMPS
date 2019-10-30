#! /bin/bash
### Usage
###  sbatch job.slurm
###  squeue
###  scancel JOBID

### Ncores  Walltime(h)
###   48     384
###   96     192
###  192      96
###  384      48

#SBATCH --nodes=1
#SBATCH --ntasks-per-node=16
#SBATCH --mem=60GB
#SBATCH --time=00:40:00
#SBATCH --job-name=relax

### Load module containing LAMMPS executable
### See "module avail" to list available modules and versions
# module load lammps/may16
module load python/3.5.1
module load lammps/aug17


python ~/bin/inOne_relax_volume.py

