"""
10/13/23
Custom residue fix
Modify selected residues to ensure proper Histidine and Glutamine protonation states

Only handles going from more protonated to less protonated state
Sample syntax:
python3 hfix.py input.pdb output.pdb HIP_233:HIE,GLH_133:GLU,GLH_196:GLU,HIP_136:HID
"""
import numpy as np
import sys
import ast
import biotite
from biotite.structure.io.pdb import PDBFile
from biotite.structure import AtomArray

######## GLOBAL VAR ########


#residue dictionary map residue name to set of atom collection
RESIDUE_DICTIONARY = {'HIE': {'HB3', 'H', 'HB2', 'ND1', 'CE1', 'HE1', 'HE2', 'O', 'N', 'HD2', 'NE2', 'CG', 'CB', 'CA', 'CD2', 'C', 'HA'}, #only HE2
                      'HIP': {'HB3', 'H', 'HB2', 'ND1', 'CE1', 'HE1', 'HE2', 'C', 'O', 'N', 'HD2', 'NE2', 'CG', 'CB', 'CA', 'CD2', 'HD1', 'HA'}, #both HE2 and HD1
                      'HID': {'HB3', 'H', 'HB2', 'ND1', 'CE1', 'HE1', 'C', 'O', 'N', 'HD2', 'NE2', 'CG', 'CB', 'CA', 'CD2', 'HD1', 'HA'}, #only HD1
                      'GLU': {'HG3', 'CD', 'O', 'HB2', 'HB3', 'OE2', 'H', 'N', 'HA', 'C', 'CB', 'HG2', 'OE1', 'CA', 'CG'},
                      'GLH': {'HG3', 'CD', 'O', 'HB2', 'HB3', 'OE2', 'H', 'N', 'HA', 'C', 'HE2', 'CB', 'HG2', 'OE1', 'CA', 'CG'}}

FILE = r"C:\Users\lisap\Lab_code\AmberMD\PDB_files\mod_pdb\5TDT_chainAMNI_combined.pdb"

############### UTILS  ###############
def read_his_atom_type(file, reslist = ['HIS', 'HID', 'HIE', 'HIP']):
    """
    rough
    read a pdb file and print out atom types of different histidine protonation states
    """
    atom_set = {}
    with open(file, 'r') as pdb_file:
        for line in pdb_file:
            res = line.split()[3]            
            if res in reslist:
                atom = line.split()[2]
                try: 
                    atom_set[res].append(atom)
                except KeyError:
                    atom_set[res] = []   
    
    for key in atom_set:
        atom_set[key] = set(atom_set[key])

    return atom_set

def old_res_to_new_res(old_res: AtomArray, new_res_name: str):
    """
    old_res: an atom array of old residue
    new_res_name: string for substituted residue

    Not handling cases where the new residue has more atoms than the old residue
    """
    old_res_type = list(set(old_res.res_name))
    if len(old_res_type) > 1:
        raise ValueError("More than one residue type detected")
    old_res_type = old_res_type[0]
    old_res_atomtype = RESIDUE_DICTIONARY[old_res_type]

    new_res_atomtype = RESIDUE_DICTIONARY[new_res_name]
    
    #find the difference
    diff = new_res_atomtype - old_res_atomtype
    if len(diff) != 0 :
        raise ValueError("New residue has more atoms than old residue")
    
    
    mask = np.isin(old_res.atom_name, list(RESIDUE_DICTIONARY[new_res_name]))
    new_res = old_res[mask]
    name_array = np.array([new_res_name] * len(new_res), dtype='<U3')
    new_res.res_name = name_array

    return new_res
        

def exe_change_atom_type(file, swap_dict):
    """
    swap_dict is a dictionary specifying swapping atom type
    key: <residue_name>_<residue_number> -> value: <residue_name>
    
    use biotite to parse a file, read in the attributes of desired residue type,
    and change it
    """
    #Assuming handling single chain only
    structure = PDBFile.read(file)
    structure = structure.get_structure()

    if len(structure) > 1:
        UserWarning("More than one chain detected, will only use the first chain")

    atomarray = structure[0]
    for key in swap_dict:
        restype, resnumber = key.split('_')
        resnumber = int(resnumber)
        #search for matching residue
        match = atomarray[atomarray.res_id == resnumber]
        #change residue type
        new_res = old_res_to_new_res(match, swap_dict[key])
        
        #search for index 
        indices = np.where(atomarray.res_id == resnumber)
        before = indices[0][0]
        after = indices[0][-1]

        #replace syntax
        atomarray = atomarray[:before] + new_res + atomarray[after + 1:]
        
    return atomarray

def write_pdb(atomarray, file):
    """
    atomarray: atomarray to be written
    file: file name
    """
    outfile = PDBFile()
    outfile.set_structure(atomarray)
    outfile.write(file)

############## TEST ##############
def test1():
    atom_set = read_his_atom_type(FILE, ['GLH', 'GLU'])
    print(atom_set)

def test2():
    exe_change_atom_type(FILE, {'HIP_233': 'HIE', 'GLH_133': 'GLU', 'GLH_196': 'GLU', 'HIP_136': 'HID'})

def final():
    write_pdb(exe_change_atom_type(FILE, 
                                   {'HIP_233': 'HID', 'GLH_133': 'GLU', 'GLH_196': 'GLU', 'HIP_136': 'HIE'}),
                                    r"C:\Users\lisap\Lab_code\AmberMD\PDB_files\mod_pdb\5TDT_chainAMNI_fix_protonation.pdb")
############## MAIN ##############
INPUT = sys.argv[1] 
OUTPUT = sys.argv[2]
TO_CHANGE = sys.argv[3]

#convert string to dictionary
#list of consecutive key-value pairs
values = TO_CHANGE.split(',')
CHANGES = {}
for value in values:
    key, val = value.split(':')
    CHANGES[key] = val


def main():
    fixed = exe_change_atom_type(INPUT, CHANGES)
    write_pdb(fixed, OUTPUT)

if __name__ == "__main__":
    main()
