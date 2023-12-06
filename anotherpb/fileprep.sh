#!/bin/bash 
set -e

# mini scripts for setting up systems for QM/MM calculation on metal protein
# PART A: MCPB, gaussian to create .inpcrd and .prmtop


############# INPUT #################
#files from H++
PARM=0.15_80_10_pH7_chainD_6YD0.top
CRD=0.15_80_10_pH7_chainD_6YD0.crd

#PDB files input
ORI=6YD0_chainD_FE.pdb
RESI_TO_MAKE_MOL2=resi_to_make_mol2


############# OUTPUT NAMES #################
#generated files by ambpdb
RECONSTRUCTED=6YD0_chainD_reconstructed

#MCPB inputfile
MCPB_INP=MCPB.inp

#####################################
##########   CODE   #################
#####################################

#activate conda
eval "$(command conda 'shell.bash' 'hook' 2> /dev/null)"
conda activate ambertools


####### A. MCPB TO GET PARAMETERS #########


#create pdb
ambpdb -p $PARM -c $CRD > $RECONSTRUCTED.pdb
sed -i  -e '$ d' $RECONSTRUCTED.pdb

#create minipbb from original, name it mini.pdb
#awk '$4 == "HOH" && $6 == 764' $ORI > mini.pdb 
#awk '$4 == "HOH" && $6 == 871' $ORI >> mini.pdb
#awk '$4 == "HOH" && $6 == 715' $ORI >> mini.pdb
#awk '$4 == "FE" && $6 == 601' $ORI >> mini.pdb
#awk '$4 == "FE" && $6 == 602' $ORI >> mini.pdb

#### MANUALLY ALERT 
# ADD H-bond to mini.pbd to get resi_to_make_mol2 ####

#fix pdb
python3 script/hfix.py $RECONSTRUCTED.pdb $RECONSTRUCTED.hfix.pdb HIP_136:HIE,HIP_235:HIE,GLH_103:GLU,GLH_198:GLU,GLH_229:GLU


#create mol2 file for the waters and iron
#take a look 
cat $RESI_TO_MAKE_MOL2.pdb

################ MAKE MOL2 FILES ################
#The irons
python3 script/getmol2.py -i $RESI_TO_MAKE_MOL2.pdb -r 601 -c 3 -a FE -b "" -o FE1.mol2 
python3 script/getmol2.py -i $RESI_TO_MAKE_MOL2.pdb -r 602 -c 3 -a FE -b "" -o FE2.mol2

#The waters
python3 script/getmol2.py -i $RESI_TO_MAKE_MOL2.pdb -r 715 -c 0,0,0 -a OW,HW,HW -b "1 1 2 1","2 1 3 1" -o HOH.mol2 
python3 script/getmol2.py -i $RESI_TO_MAKE_MOL2.pdb -r 764 -c 0,0,0 -a OW,HW,HW -b "1 1 2 1","2 1 3 1" -o HOH1.mol2
python3 script/getmol2.py -i $RESI_TO_MAKE_MOL2.pdb -r 871 -c 0,0,0 -a OW,HW,HW -b "1 1 2 1","2 1 3 1" -o HOH2.mol2

#Run parmchk for some file
parmchk2 -i HOH.mol2 -o HOH.frcmod -f mol2
parmchk2 -i HOH1.mol2 -o HOH1.frcmod -f mol2
parmchk2 -i HOH2.mol2 -o HOH2.frcmod -f mol2

#Create a merged pdb file
cat $RECONSTRUCTED.hfix.pdb $RESI_TO_MAKE_MOL2.pdb > $RECONSTRUCTED.merged.pdb

#Fix indexing
pdb4amber -i $RECONSTRUCTED.merged.pdb -o $RECONSTRUCTED.merged.fixed.pdb

tail -n 20 $RECONSTRUCTED.merged.fixed.pdb

#Make MCPB input file
echo original_pdb $RECONSTRUCTED.merged.fixed.pdb > $MCPB_INP
echo group_name 6YD0 >> $MCPB_INP
echo cut_off 3.9 >> $MCPB_INP
echo ion_ids 8155 8156 >> $MCPB_INP
echo ion_mol2files FE1.mol2 FE2.mol2 >> $MCPB_INP
echo naa_mol2files HOH.mol2 HOH1.mol2 HOH2.mol2 >> $MCPB_INP
echo frcmod_files HOH.frcmod HOH1.frcmod HOH2.frcmod >> $MCPB_INP 
echo large_opt 1 >> $MCPB_INP

######################
###### RUN MCBP ######

MCPB.py -i MCPB.inp -s 1

### MANUAL ALERT ###
# 1. Run Gaussian
# De-clutter by moving this away from current directory

# Create gaussian job directory
mkdir -p gaussian_job/{small_opt,large_mk,force_calc}

#move and rename file
mv *small_opt.com gaussian_job/small_opt/6YD0_small_opt.gjf
mv *small_fc.com gaussian_job/force_calc/6YD0_small_fc.gjf
mv *large_mk.com gaussian_job/large_mk/6YD0_large_mk.gjf

### RUN GAUSSIAN ###
# 1. Manually run gaussian, change things as needed
# 2. Move result files back to common directory

##### STEP 2 ######
MCPB.py -i MCBP.inp -s 2

##TODO: implement fix for PDB file writer

#### STEP 3 ####
MCPB.py -i MCBP.inp -s 3

#### STEP 4 ####
MCPB.py -i MCBP.inp -s 4

#### RUN TLEAP  ####
tleap -f -s 6YD0_tleap.in > 6YD0_tleap.out 

# TODO: FIX TLEAP input generator to use TIP3 water
# TODO: FIX MCPB writer

