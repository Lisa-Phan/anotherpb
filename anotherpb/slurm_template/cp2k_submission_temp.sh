#!/bin/bash
#SBATCH -o %x.out      # Name of stdout output file (%j expands to job ID)
#SBATCH -e %x.err      # Name of stderr output file (%j expands to job ID)
#SBATCH -p normal            # Queue name
#SBATCH -N 2                 # Total number of nodes
#SBATCH -n 26               # Total number of mpi tasks
#SBATCH -A CHE23010
#SBATCH --mail-type=begin,end,fail
#SBATCH --mail-user=dhp563@my.utexas.edu

export OMP_NUM_THREADS=6
module load cp2k impi intel

INPUT_FILE=$1
OUTPUT_FILE=${INPUT_FILE%.*}.out

ibrun cp2k.psmp -i $INPUT_FILE -o $OUTPUT_FILE
