#!/bin/bash
#SBATCH -o %x.out      # Name of stdout output file (%j expands to job ID)
#SBATCH -e %x.err      # Name of stderr output file (%j expands to job ID)
#SBATCH -N 1                 # Total number of nodes
#SBATCH -n 10               # Total number of mpi task
#SBATCH -A CHE23010
#SBATCH --mail-type=begin,end,fail
#SBATCH --mail-user=dhp563@my.utexas.edu

source /home1/09069/dhp563/orca_env_config.sh

#input file is first argument, output file is inputfile name with extension replace with .out
INPUT_FILE=$1
OUTPUT_FILE=${INPUT_FILE%.*}.out

$ORCA $INPUT_FILE > $OUTPUT_FILE
