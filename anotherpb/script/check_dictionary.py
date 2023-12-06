"""
Python dictionary file

each key is mapped to another dictionary with:
    1. element 
    2. whether the key needs to be included in the extra field

"""

DICTIONARY = {'C': {'element': 'C', 'extra': False}, 
              'CA': {'element': 'C', 'extra': False},
              'CB': {'element': 'C', 'extra': False}, 
              'CD': {'element': 'C', 'extra': False},
              'CD1': {'element': 'C', 'extra': False},
              'CD2': {'element': 'C', 'extra': False},
              'CE': {'element': 'C', 'extra': False},
               'CE1' : {'element': 'C', 'extra': False},
               'CE2': {'element': 'C', 'extra': False},
                'CE3': {'element': 'C', 'extra': False},
               'CH2': {'element': 'C', 'extra': False},
               'CG': {'element': 'C', 'extra': False},
                'CG1': {'element': 'C', 'extra': False},
               'CG2': {'element': 'C', 'extra': False},
               'CZ': {'element': 'C', 'extra': False},
               'CZ2': {'element': 'C', 'extra': False},
                'CZ3': {'element': 'C', 'extra': False},
                 'FE': {'element': 'Fe', 'extra': True},
                 'H': {'element': 'H', 'extra': False},
                 'H1': {'element': 'H', 'extra': False}, 
                 'H2': {'element': 'H', 'extra': False},
                 'H3': {'element': 'H', 'extra': False},
                 'HA': {'element': 'H', 'extra': False},
                 'HA2': {'element': 'H', 'extra': False},
                 'HA3': {'element': 'H', 'extra': False},
                 'HB': {'element': 'H', 'extra': False},
                 'HB1': {'element': 'H', 'extra': False},
                 'HB2'  : {'element': 'H', 'extra': False},
                 'HB3': {'element': 'H', 'extra': False}, 
                 'HD1': {'element': 'H', 'extra': False},
                 'HD11': {'element': 'H', 'extra': False},
                 'HD12': {'element': 'H', 'extra': False},
                 'HD13': {'element': 'H', 'extra': False},
                 'HD2': {'element': 'H', 'extra': False},
                 'HD21' : {'element': 'H', 'extra': False},
                 'HD22': {'element': 'H', 'extra': False},
                 'HD23': {'element': 'H', 'extra': False},
                 'HD3': {'element': 'H', 'extra': False},
                 'HE': {'element': 'H', 'extra': False},
                 'HE1': {'element': 'H', 'extra': False},
                 'HE2': {'element': 'H', 'extra': False},
                 'HE21': {'element': 'H', 'extra': False},
                 'HE22': {'element': 'H', 'extra': False},
                 'HE3': {'element': 'H', 'extra': False},
                 'HG': {'element': 'H', 'extra': False},
                 'HG1': {'element': 'H', 'extra': False},
                 'HG11': {'element': 'H', 'extra': False},
                 'HG12': {'element': 'H', 'extra': False},
                 'HG13': {'element': 'H', 'extra': False},
                 'HG2': {'element': 'H', 'extra': False},
                 'HG21': {'element': 'H', 'extra': False},
                 'HG22': {'element': 'H', 'extra': False},
                 'HG23': {'element': 'H', 'extra': False},
                 'HG3': {'element': 'H', 'extra': False},
                 'HH': {'element': 'H', 'extra': False},
                 'HH11': {'element': 'H', 'extra': False},
                 'HH12': {'element': 'H', 'extra': False},
                 'HH2': {'element': 'H', 'extra': False},
                 'HH21': {'element': 'H', 'extra': False},
                 'HH22': {'element': 'H', 'extra': False},
                 'HZ': {'element': 'H', 'extra': False},
                 'HZ1': {'element': 'H', 'extra': False},
                 'HZ2': {'element': 'H', 'extra': False},
                 'HZ3': {'element': 'H', 'extra': False},
                 'N': {'element': 'N', 'extra': False},
                 'Na+' : {'element': 'Na', 'extra': True},
                 'ND1': {'element': 'N', 'extra': False},
                 'ND2': {'element': 'N', 'extra': False},
                 'NE': {'element': 'N', 'extra': False},
                 'NE1': {'element': 'N', 'extra': False},
                 'NE2': {'element': 'N', 'extra': False},
                 'NH1': {'element': 'N', 'extra': False},
                 'NH2': {'element': 'N', 'extra': False},
                 'NZ': {'element': 'N', 'extra': False},
                 'O': {'element': 'O', 'extra': False},
                 'O1': {'element': 'O', 'extra': False},
                 'O2': {'element': 'O', 'extra': False},
                 'OD1': {'element': 'O', 'extra': False},
                 'OD2': {'element': 'O', 'extra': False},
                 'OE1': {'element': 'O', 'extra': False},
                 'OE2': {'element': 'O', 'extra': False},
                 'OG': {'element': 'O', 'extra': False},
                 'OG1': {'element': 'O', 'extra': False},
                 'OH': {'element': 'O', 'extra': False},
                 'OXT': {'element': 'O', 'extra': False},
                 'SD': {'element': 'S', 'extra': False},
                 'SG': {'element': 'S', 'extra': False}}

amber_atom_dict = {
'N3': {'NZ', 'N'}, 
'H': {'HE2', 'HE', 'HZ3', 'HZ2', 'HD22', 'HH21', 'HH11','HH12', 'H1', 'H2', 'HH22', 'HE1', 'H3', 'HZ1', 'HE21', 'HD1', 'HE22', 'HD21', 'H'}, 
'CX': {'CA'}, 
 'HP': {'HE3', 'HE2', 'HA'}, 
 'CT': {'CG', 'CE', 'CD1', 'CB', 'CG1', 'CD', 'CD2', 'CG2'}, 
 'HC': {'HG11', 'HD23', 'HD22', 'HG22', 'HB3', 'HG13', 'HG12', 'HD3', 'HG23', 'HG', 'HB1', 'HB', 'HD11', 'HD12', 'HG21', 'HD21', 'HD2', 'HB2', 'HG3', 'HD13', 'HG2'}, 
 'C': {'CD', 'CZ', 'CG', 'C'}, 
 'O': {'OE1', 'O', 'OD1'}, 
 'N': {'NE2', 'N', 'ND2'}, 
 'XC': {'CA'}, 
 'H1': {'HE2', 'HD2', 'HE3', 'HB', 'HA3', 'HG3', 'HE1', 'HB2', 'HB3', 'HD3', 'HA2', 'HA', 'HG2'}, 
 '2C': {'CB', 'CG', 'CG1'}, 
 'S': {'SD'}, 
 'CC': {'CG'}, 
 'NB': {'ND1'}, 
 'CR': {'CE1'}, 
 'H5': {'HE1'}, 
 'NA': {'ND1', 'NE1', 'NE2'}, 
 'CW': {'CD1', 'CD2'}, 
 'H4': {'HD1', 'HD2'}, 
 'C8': {'CD', 'CB', 'CE', 'CG'}, 
 'N2': {'NH1', 'NH2', 'NE'}, 
 'CA': {'CE1', 'CG', 'CH2', 'CZ', 'CD1', 'CZ2', 'CE3', 'CE2', 'CZ3', 'CD2'}, 
 'CO': {'CD', 'CG'}, 
 'O2': {'OD2', 'OE1', 'OXT', 'OD1', 'OE2', 'O'}, 
 'C*': {'CG'}, 
 'CN': {'CE2'}, 
 'HA': {'HE2', 'HD2', 'HE3', 'HH2', 'HZ3', 'HZ2', 'HD1', 'HE1', 'HZ'}, 
 'CB': {'CD2'}, 
 'OH': {'OD2', 'OG1', 'OG', 'OE2', 'OH'}, 
 'HO': {'HG1', 'HE2', 'HD2', 'HG', 'HH'}, 
 '3C': {'CG', 'CB'}, 
 'Y1': {'OE1'}, 
 'Y2': {'OE2'}, 
 'Y3': {'OE1'}, 
 'Y4': {'OE2'}, 
 'Y5': {'ND1'}, 
 'SH': {'SG'}, 
 'HS': {'HG'}, 
 'Y8': {'OE1'}, 
 'Y9': {'OE2'}, 
 'Z1': {'OE1'}, 
 'Z2': {'OE2'}, 
 'Z3': {'NE2'}, 
 'CV': {'CD2'}, 
 'Y6': {'O1'}, 
 'Y7': {'O2'}, 
 'M1': {'FE'}, 
 'M2': {'FE'}, 
 'Na+': {'Na+'}, 
 'OW': {'O'}, 
 'HW': {'H2', 'H1'}}



def get_updated_dictionary(amber_atom_dict, to_include_tag = ['X', 'Y', 'Z', 'M']):
    """
    Function to update the dictionary with the correct elements
    """
    updated_dictionary = {}
    for key in amber_atom_dict:
        #infer element 
        element = []
        for normal_atom in amber_atom_dict[key]:
            element.append(DICTIONARY[normal_atom]['element'])
        element = set(element)
        if len(element) > 1:
            print('Warning: {} has multiple elements'.format(key))
        
        tag = False
        if any(ele in key for ele in to_include_tag):
            tag = True
        updated_dictionary[key] = {'element': element.pop(), 'extra': tag}
    return updated_dictionary

print(get_updated_dictionary(amber_atom_dict))
