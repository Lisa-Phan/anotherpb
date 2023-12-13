#!/bin/bash
set -e

#### PART B. Run CP2K to equilibrate system ####

##### NAME VARIABLES #####
PARMTOP_FILE=$(realpath $1)
INPCRD_FILE=$(realpath $2)
JOB_TITLE=$3
SCRIPT=/scratch/09069/dhp563/workflow_code_mcpb_cp2k/anotherpb/script
TEMPLATE=/scratch/09069/dhp563/workflow_code_mcpb_cp2k/anotherpb/slurm_template

#### WORKING DIRECTORY, set as current dir, where files are written ####
WORKDIR=$(pwd)

echo work dir: $WORKDIR
echo parmtop: $PARMTOP_FILE
echo job_title: $JOB_TITLE
echo inpcrd: $INPCRD_FILE

##### MAKE DIRECTORY #####
mkdir -p {NPT_$JOB_TITLE,NVT_$JOB_TITLE}

##### MAKE INPUT #####
# 1. NVT 
# make_template_cp2k.py takes three arguments
# $1=prmtop file
# $2=inpcrd file
# $3=input_file_name


#### REMOVE FLAG CMAP lines FROM PRMTOP ####
sed '/^%FLAG CMAP*/d' $PARMTOP_FILE > $WORKDIR/noflag.prmtop

python3 $SCRIPT/make_template_cp2k.py $WORKDIR/noflag.prmtop $INPCRD_FILE NPT_$JOB_TITLE/CP2K_$JOB_TITLE.inp

#move template file over
cp $TEMPLATE/cp2k_submission_temp.sh NPT_$JOB_TITLE/.

#submit job
#short submission to check for timeouts
sbatch -J NPT_mini \
       -t 00:10:00 \
       NPT_$JOB_TITLE/cp2k_submission_temp.sh \
       NPT_$JOB_TITLE/CP2K_$JOB_TITLE.inp

sbatch -J NPT \
       -t 12:00:00 \
       NPT_$JOB_TITLE/cp2k_submission_temp.sh \
       NPT_$JOB_TITLE/CP2K_$JOB_TITLE.inp
