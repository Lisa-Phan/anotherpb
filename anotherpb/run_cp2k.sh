#!/bin/bash
set -e

#### PART B. Run CP2K to equilibrate system ####

##### NAME VARIABLES #####
PARMTOP_FILE=$1
INPCRD_FILE=$2
JOB_TITLE=$3

SCRIPT=/scratch/09069/dhp563/workflow_code_mcpb_cp2k/anotherpb/script
TEMPLATE=/scratch/09069/dhp563/workflow_code_mcpb_cp2k/anotherpb/slurm_template 

##### MAKE DIRECTORY #####
mkdir -p {NPT_$JOB_TITLE,NVT_$JOB_TITLE}

##### MAKE INPUT #####
# 1. NVT 
# make_template_cp2k.py takes three arguments
# $1=prmtop file
# $2=inpcrd file
# $3=input_file_name


python3 $SCRIPT/make_template_cp2k.py $PARMTOP_FILE $INPCRD_FILE NPT_$JOB_TITLE/CP2K_$JOB_TITLE.inp

#move template file over
cp $TEMPLATE/cp2k_submission_temp.sh NPT_$JOB_TITLE/.

#submit job
sbatch NPT_$JOB_TITLE/cp2k_submission_temp.sh NPT_$JOB_TITLE/CP2K_$JOB_TITLE.inp
