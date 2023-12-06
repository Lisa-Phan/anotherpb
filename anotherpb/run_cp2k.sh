#!/bin/bash
set -e

#### PART B. Run CP2K to equilibrate system ####

##### NAME VARIABLES #####
PARMTOP_FILE=''
INPCRD_FILE='' 
JOB_TITLE=''

##### MAKE DIRECTORY #####
mkdir -p {NPT_$JOB_TITLE,NVT_$JOB_TITLE}

##### MAKE INPUT #####
# 1. NVT input
python3 script/make_template_cp2k.py $PARMTOP_FILE $INPCRD_FILE NVT_$JOB_TITLE/CP2K_$JOB_TITLE 
