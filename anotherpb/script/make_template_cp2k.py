"""
Create a file that generates
element mapping fields for amber-type atoms to
element of the atom

input: a .prmtop file, generated from MCPB
       a .inpcrd file, generated from MCPB
       an output file name for the CP2K input file

extract box dimensions from .prmtop file
extract the atom fields and map them to element via a dictionary 
write output CP2K file

"""

import subprocess
import textwrap
import os, sys
from obj.atom_dict import AMBER_ATOM_DICT

### Element dict is a python text to be evaluated
# contains two object,
# a dictionary for items not having to be specified, like HA HB, etc 
# a dictionary for items that have to be specified, like Na+, M, etc

PRMTOP_FILE = sys.argv[1]
INPCRD_FILE = sys.argv[2]
OUTFILE = sys.argv[3]

########################
###### FUNCTIONS #######
########################

############## UTILITIES ##################

def extract_text(file_path, field_name,  flag = '%FLAG', to_remove = ['%FORMAT(20a4)']):
    """
    Extract specified text within a field from a file with fields separated by % FLAG lines.

    Parameters:
        - file_path: Path to the input file.
        - flag: The unique identifier for each field (e.g., '% FLAG').
        - field_name: The name of the field from which text needs to be extracted.

    Returns:
        - A list of extracted text for the specified field.
    """
    extracted_text = []
    current_field = None

    with open(file_path, 'r') as file:
        for line in file:
            # Remove any unwanted characters from the line
            for char in to_remove:
                line = line.replace(char, '')
            if line.startswith(flag):
                # Start of a new field
                current_field = line[len(flag):].strip()
            elif current_field == field_name:
                # Inside the desired field, extract text
                extracted_text.append(line.strip())

    return extracted_text

def parse_atom_from_line(line, length_each_atom: int = 4):
    """
    amber file format writes atom name in a consistent 4-character spacing format
    break line into chunks of specified length
    return a list of atoms
    """
    atoms = []
    for i in range(0, len(line), length_each_atom):
        atoms.append(line[i:i+length_each_atom])
    
    atoms = [atom.strip() for atom in atoms]
    return atoms

def get_unique_atoms(extracted_text, unique = True):
    """
    extracted text is a list of strings, each string is a line from the file
    function returns a list of unique atoms
    """
    all_atoms = []
    for line in extracted_text:
        atoms = parse_atom_from_line(line)
        all_atoms.extend(atoms)
    if unique:
        unique_atoms = list(set(all_atoms))
        return unique_atoms
    else:
        return all_atoms
    
############ MAKE BLOCK ################

def get_amber_atom(param_file):
    """
    Get the atom names from the AMBER parameter file.
    """
    all_text = extract_text(param_file, 
                            'AMBER_ATOM_TYPE')
    
    return get_unique_atoms(extracted_text = all_text)
    
def create_element_kind_block(unique_atoms):
    """
    Create the element kind block for the CP2K input file.
    """
    element_kind_block = ''
    for atom in unique_atoms:
        if AMBER_ATOM_DICT[atom]['extra'] == True:
            element_kind_block += f"    &KIND {atom}\n"
            element_kind_block += f"        ELEMENT {AMBER_ATOM_DICT[atom]['element']}\n"
            element_kind_block += f"    &END KIND\n"
    
    #remove trailing newline
    element_kind_block = element_kind_block[:-1]
    return element_kind_block

def get_box_dimensions(inpcrd_file):
    """
    box dimension is in the last line of inpcrd file
    """
    last_line = subprocess.check_output(f"tail -1 {inpcrd_file}", shell=True).decode('utf-8')
    x, y, z, a_angle, b_angle, c_angle = last_line.split()
    
    #round to nearest int
    x = round(float(x))
    y = round(float(y))
    z = round(float(z))
    
    return x, y, z

def get_element_kind_block(prmtop_file):
    unique_atoms = get_amber_atom(prmtop_file)
    element_kind_block = create_element_kind_block(unique_atoms)
    return element_kind_block

def get_cp2k_template(prmtop_file, inpcrd_file):
    """
    Fill in the CP2K template with the correct values
    """

    BOX_X, BOX_Y, BOX_Z = get_box_dimensions(inpcrd_file)
    PRMTOP_FILE = os.path.abspath(prmtop_file)
    INPCRD_FILE = os.path.abspath(inpcrd_file)
    ELEMENT_TYPE_BLOCK = get_element_kind_block(prmtop_file)


    cp2k_template = f"""\

    &GLOBAL
        PROJECT NVT
        PRINT_LEVEL LOW
        RUN_TYPE MD
    &END GLOBAL

    &MOTION
    &MD
        ENSEMBLE NVT
        STEPS 30000
        TIMESTEP 0.1
        TEMPERATURE 300.0
        &THERMOSTAT
            &NOSE
            &END NOSE
        &END THERMOSTAT
    &END MD
    &END MOTION

    &FORCE_EVAL
        METHOD FIST
        &MM
            &FORCEFIELD
                PARMTYPE AMBER
                PARM_FILE_NAME {PRMTOP_FILE}
                &SPLINE
                    EMAX_SPLINE 1.0E8 !Default from QMMM tutorial is 1.0E8
                    RCUT_NB [angstrom] 10 !Default from QMMM tutorial is 10
                &END SPLINE
            &END FORCEFIELD
            &POISSON
                &EWALD
                    EWALD_TYPE SPME
                    ALPHA 3.500000E-1 !alpha parameter associated with Ewald. Recommend 3.5 for small systems, for tight-binding recommend 1. Runing alpha, r_cut and gmas is needed to obain O(N**1.5) scaling for ewald. Default is 0.35
                    GMAX 80 !default val from QMMM tut
                    RCUT 10 !units default = angstrom
                &END EWALD
            &END POISSON
            &PRINT
                &FF_INFO HIGH
                &END FF_INFO
            &END PRINT
        &END MM
        &SUBSYS
            &CELL !Set box dimensions here
            ABC [angstrom] {BOX_X} {BOX_Y} {BOX_Z}  !The lengths of the cell vectors 
            ALPHA_BETA_GAMMA 90 90 90
            &END CELL
            &TOPOLOGY
                CONN_FILE_FORMAT AMBER
                CONN_FILE_NAME {PRMTOP_FILE}
                COORD_FILE_FORMAT CRD
                COORD_FILE_NAME {INPCRD_FILE}
            &END TOPOLOGY
            {textwrap.indent(ELEMENT_TYPE_BLOCK, '        ')}
            &KIND EP
                GHOST
                ELEMENT H
            &END KIND

    &END SUBSYS
    &END FORCE_EVAL
    """

    return cp2k_template

def write_cp2k_template(cp2k_template, outfile):
    """
    write output file
    """
    with open(outfile, 'w') as file:
        file.write(cp2k_template)


if __name__ == '__main__':
    write_cp2k_template(cp2k_template = get_cp2k_template(PRMTOP_FILE, INPCRD_FILE), 
                        outfile = OUTFILE)

# def extract_element_type_block(pdb_file):
#     """
#     Extract the element type block from the pdb file
#     """
#     command = f"awk '{{print $3}}' {pdb_file} | sort | uniq | paste -s -d' '"
#     elements_in_file = subprocess.check_output(command, shell=True).decode('utf-8').split()

#     #omit the first line, with is part of the header 
#     elements_in_file = elements_in_file[1:]




# ############ CP2K template file ###############

