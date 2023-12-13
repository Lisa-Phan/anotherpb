#!/bin/bash
#SBATCH -o %x.out      # Name of stdout output file (%j expands to job ID)
#SBATCH -e %x.err      # Name of stderr output file (%j expands to job ID)
#SBATCH -p normal            # Queue name
#SBATCH -N 1                 # Total number of nodes
#SBATCH -n 1               # Total number of mpi tasks
#SBATCH -A CHE23010        
#SBATCH --mail-type=begin,end,fail
#SBATCH --mail-user=dhp563@my.utexas.edu


module load gaussian
echo Remember to add job_name -J flag and -t time flag

#input file is only argument
g16 $1
