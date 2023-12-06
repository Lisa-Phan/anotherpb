import argparse
import textwrap

def parse_pdb(pdb_file, residue_number, atom_charges, atom_types):
    atom_data = []
    with open(pdb_file, 'r') as pdb:
        for line in pdb:
            if line.startswith('HETATM'):
                fields = line.split()
                residue_num = int(fields[5])
                residue_name = fields[3]
                atom_name = fields[2]
                if residue_num == residue_number:
                    x = float(fields[6])
                    y = float(fields[7])
                    z = float(fields[8])
                    atom_charge = float(atom_charges.pop(0))
                    atom_type = atom_types.pop(0)
                    atom_data.append((residue_name, atom_name, x, y, z, atom_charge, atom_type))
    return atom_data

def generate_mol2(atom_data, residue_number, output_file, bond_lines=None):
    
    """
    Explaining the mol2 file format:
    Field 1: 
    1.molecule name
    2.num_atoms [num_bonds [num_subst [num_feat[num_sets]]]] For this use case, only the first two fields matter
    3.molecule type
    4.charge type

    Field 2:
    each atom gets a line
    format: {atom_idex:5>} {atom_name:3<} {x:<10.3f} {y:<10.3f} {z:<10.3f} {atom_type:<3} {molecule_number} {molecule_name} {atom_charge:<5.3f}

    Field 3:
    bond information
    each bond gets a line
    format: {bond_index:5>} {atom1_index:5>} {atom2_index:5>} {bond_type:3<} 
    where bondtype 1 = single, 2 = double, 3 = triple, 4 = aromatic, 5 = amide, 6 = custom

    """

    mol2_template = textwrap.dedent("""\
        @<TRIPOS>MOLECULE
        {residue_name}
        {atomnumber} {bondnumber} 1 0 0
        SMALL
        USER_CHARGE

        @<TRIPOS>ATOM
        {atom_block}
        @<TRIPOS>BOND
        {bond_block}                
        @<TRIPOS>SUBSTRUCTURE
        1 {residue_name}          1 TEMP              0 ****  ****    0 ROOT
    """)

    atom_lines = ""

    atom_index = 1
    for residue_name, atom_name, x, y, z, atom_charge, atom_type in atom_data:
        atom_lines += f"{atom_index:5} {atom_name:3}       {x:<8.3f} {y:<8.3f} {z:<8.3f}    {atom_type:<3} {residue_number} {residue_name:>5} {atom_charge:.3f}\n"
        atom_index += 1

    #remove trailing line break character, since there will be error if there is space between fields separator
    atom_lines = atom_lines[:-1]

    if bond_lines is None:
            bond_block = ''
    else:
        bond_block = ''
        for bond_line in bond_lines:
            bond_block += bond_line + '\n'
    print('printing updated bond', bond_block)
    mol2_content = mol2_template.format(
        residue_number=residue_number,
        atomnumber=len(atom_data),
        residue_name = atom_data[0][0],
        bondnumber=len(atom_data) - 1,  # Assuming single bonds
        atom_block=atom_lines,
        bond_block=bond_block
    )

    with open(output_file, 'w') as mol2_file:
        mol2_file.write(mol2_content)

def main():
    parser = argparse.ArgumentParser(description='Generate Mol2 file from PDB for a specific residue')
    parser.add_argument('-i', '--in_pdb_file', type=str, help='Input PDB file')
    parser.add_argument('-r', '--residue_number', type=int, help='Residue number for which to create Mol2')
    parser.add_argument('-c','--charges', type=str, help='Comma-separated atom charges')
    parser.add_argument('-o', '--output_file', type=str, help='Output Mol2 file')
    parser.add_argument('-a', '--atom_types', type=str, help='Atom name for Mol2 file, similar in order as in pdb and comma separated')
    parser.add_argument('-b', '--bond_line', type=str, help='Bond line for Mol2 file')

    args = parser.parse_args()

    atom_charges = [float(charge) for charge in args.charges.split(',')]
    atom_types = args.atom_types.split(',')
    bond_lines = args.bond_line.split(',')
    atom_data = parse_pdb(args.in_pdb_file, args.residue_number, atom_charges, atom_types)
    
    generate_mol2(atom_data, 
                  args.residue_number, 
                  args.output_file, 
                  bond_lines)

if __name__ == "__main__":
    main()

