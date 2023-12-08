#!/bin/bash 
set -e

# mini scripts for setting up systems for QM/MM calculation on metal protein
# PART A: MCPB, gaussian to create .inpcrd and .prmtop


############# INPUT #################

#PDB files input. File name without .pdb extension
ORI=2INC_chainA_FE_H20
RESI_TO_MAKE_MOL2=resi_to_make_mol2

######################################
########### NAMING VAR ###############
######################################

########## OUTPUT NAMES ##############
#generated files by ambpdb
RECONSTRUCTED=$ORI

#MCPB inputfile
MCPB_INP=MCPB.inp

#Starting code for MCPB created file
MCPB_GROUP=2INC


#######################################
############   CODE   #################
#######################################

#activate conda
eval "$(command conda 'shell.bash' 'hook' 2> /dev/null)"
conda activate ambertools

#main_dir is the current directory of the script
#use this as reference to call other mini functions  
MAIN_DIR="$( cd "$( dirname "$0" )" && pwd )"
SCRIPT_DIR=/scratch/09069/dhp563/workflow_code_mcpb_cp2k/anotherpb/script
TEMPLATE=/scratch/090690/dhp563/workflow_code_mcpb_cp2k/anotherpd/slurm_template

####### A. MCPB TO GET PARAMETERS #########


#create pdb
#ambpdb -p $PARM -c $CRD > $RECONSTRUCTED.pdb
#sed -i  -e '$ d' $RECONSTRUCTED.pdb

#create minipbb from original, name it mini.pdb
#awk '$4 == "HOH" && $6 == 764' $ORI > mini.pdb 
#awk '$4 == "HOH" && $6 == 871' $ORI >> mini.pdb
#awk '$4 == "HOH" && $6 == 715' $ORI >> mini.pdb
#awk '$4 == "FE" && $6 == 601' $ORI >> mini.pdb
#awk '$4 == "FE" && $6 == 602' $ORI >> mini.pdb

#### MANUAL ALERT #### 
# ADD H-bond to mini.pbd to get resi_to_make_mol2 ####

#fix pdb protonation 
python3 $SCRIPT_DIR/hfix.py $RECONSTRUCTED.pdb $RECONSTRUCTED.hfix.pdb HIP_137:HIE,HIP_234:HID,GLH_197:GLU


#create mol2 file for the waters and iron
#take a look 
cat $RESI_TO_MAKE_MOL2.pdb

################ MAKE MOL2 FILES ################
#The irons
python3 $SCRIPT_DIR/getmol2.py -i $RESI_TO_MAKE_MOL2.pdb -r 501 -c 3 -a FE -b "" -o FE1.mol2 
python3 $SCRIPT_DIR/getmol2.py -i $RESI_TO_MAKE_MOL2.pdb -r 502 -c 3 -a FE -b "" -o FE2.mol2

#The waters
python3 $SCRIPT_DIR/getmol2.py -i $RESI_TO_MAKE_MOL2.pdb -r 504 -c 0,0,0 -a OW,HW,HW -b "1 1 2 1","2 1 3 1" -o HOH.mol2 
python3 $SCRIPT_DIR/getmol2.py -i $RESI_TO_MAKE_MOL2.pdb -r 505 -c 0,0,0 -a OW,HW,HW -b "1 1 2 1","2 1 3 1" -o HOH1.mol2
python3 $SCRIPT_DIR/getmol2.py -i $RESI_TO_MAKE_MOL2.pdb -r 506 -c 0,0,0 -a OW,HW,HW -b "1 1 2 1","2 1 3 1" -o HOH2.mol2
python3 $SCRIPT_DIR/getmol2.py -i $RESI_TO_MAKE_MOL2.pdb -r 507 -c 0,0,0 -a OW,HW,HW -b "1 1 2 1","2 1 3 1" -o HOH3.mol2

#Run parmchk for some file
parmchk2 -i HOH.mol2 -o HOH.frcmod -f mol2
parmchk2 -i HOH1.mol2 -o HOH1.frcmod -f mol2
parmchk2 -i HOH2.mol2 -o HOH2.frcmod -f mol2
parmchk2 -i HOH3.mol2 -o HOH3.frcmod -f mol2

#Remove hetatm lines, since the relevant info for this
#is in $RESI_TO_MAKE_MOL2 
sed -i '/HETATM/d' $RECONSTRUCTED.hfix.pdb

#Create a merged pdb file
cat $RECONSTRUCTED.hfix.pdb $RESI_TO_MAKE_MOL2.pdb > $RECONSTRUCTED.merged.pdb

#Fix indexing
pdb4amber -i $RECONSTRUCTED.merged.pdb -o $RECONSTRUCTED.merged.fixed.pdb


#### Infer metal atom index ####
METAL_ATOM_INDICES=$(grep 'FE' $RECONSTRUCTED.merged.fixed.pdb | awk '{print $2}')

echo Inferred atom indices: $METAL_ATOM_INDICES

#Make MCPB input file
echo original_pdb $RECONSTRUCTED.merged.fixed.pdb > $MCPB_INP
echo group_name $MCPB_GROUP_NAME >> $MCPB_INP
echo cut_off 3.9 >> $MCPB_INP
echo ion_ids $METAL_ATOM_INDICES >> $MCPB_INP
echo ion_mol2files FE1.mol2 FE2.mol2 >> $MCPB_INP
echo naa_mol2files HOH.mol2 HOH1.mol2 HOH2.mol2 HOH3.mol2 >> $MCPB_INP
echo frcmod_files HOH.frcmod HOH1.frcmod HOH2.frcmod HOH3.frcmod >> $MCPB_INP 
echo large_opt 1 >> $MCPB_INP
echo ff_choice gaff >> $MCPB_INP #general amber force field
echo watermodel tip3p >> $MCPB_INP #tip3p water

######################
###### RUN MCBP ######

MCPB.py -i MCPB.inp -s 1

### MANUAL ALERT ###
# 1. Run Gaussian
# De-clutter by moving this away from current directory

# Create gaussian job directory
mkdir -p gaussian_job/{small_opt,large_mk,force_calc}

#move and rename file
mv *small_opt.com gaussian_job/small_opt/.
mv *small_fc.com gaussian_job/force_calc/.
mv *large_mk.com gaussian_job/large_mk/.

#submit job
#-J flag for job name
sbatch $TEMPLATE -J small_opt_job gaussian_job/small_opt/*small_opt.com
sbatch $TEMPLATE -J mk_job gaussian_job/large_mk/*large_mk.com 

### MANUAL ALERT RUN GAUSSIAN ###
# 1. Manually run gaussian, change things as needed
# 2. Move result files back to common directory

exit
##### STEP 2 ######
MCPB.py -i MCPB.inp -s 2

##TODO: implement fix for PDB file writer

#### STEP 3 ####
MCPB.py -i MCPB.inp -s 3

#### STEP 4 ####
MCPB.py -i MCPB.inp -s 4

#### RUN TLEAP  ####
tleap -f -s $MCPB_GROUP_tleap.in > $MCPB_GROUP_tleap.out 

# TODO: FIX TLEAP input generator to use TIP3 water

