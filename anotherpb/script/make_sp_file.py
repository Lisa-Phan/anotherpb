"""
mini script to generate a series of file for single point broken symmetry calculations

input: 

trj: a trj file, containing coordinates of 
all images

template: a template containing 
the setting for the sp broken symmetry calculation

basename: file base name for the output files
"""

from itertools import islice
import argparse


def read_trj(trj_file):
    """
    read trj file one image at a time
    new image is defined when starting line contains atom count number

    images start with the input reactant and end with output product
    """

    image_store = []

    with open(trj_file, 'r') as trj:
        atom_number = int(trj.readline().strip())
        print(f'atom number: {atom_number}')
        trj.seek(0)
        #read file in chunks of n lines where n = atom_number + 2
        chunk = list(islice(trj, atom_number + 2))
        while chunk:
            image_store.append(chunk)
            chunk = list(islice(trj, atom_number + 2))
    return image_store


def generate_files(trj, template, basename, charge_multi_strip = '*xyz 0 1'):
    # Read the template file
    with open(template, 'r') as template_file:
        template_content = template_file.read()

    images_block = read_trj(trj)
    images_xyz = [image[2:] for image in images_block]


    # Generate a file for each image with the specified basename
    for i, image in enumerate(images_xyz):
        output_filename = f"{basename}_im{i}.inp"
        with open(output_filename, 'w') as output_file:
            # Write template content to the output file
            output_file.write(template_content)
            
            # Write coordinates for the current image
            output_file.write(charge_multi_strip)
            output_file.write('\n')
            for line in image:
                output_file.write(line)
            #finish writing
            output_file.write('*\n')
            output_file.close()

def main():
    
    parser = argparse.ArgumentParser(description='Generate a series of files for single point broken symmetry calculations')
    parser.add_argument('trj', help='trj file containing the coordinates of all images')
    parser.add_argument('template', help='template file containing the settings for the sp broken symmetry calculation')
    parser.add_argument('basename', help='file base name for the output files')
    parser.add_argument('--charge_multi_strip', help='charge and multiplicity line to be stripped from the template file', default='*xyz 0 1\n')
    args = parser.parse_args()

    generate_files(args.trj, args.template, args.basename, args.charge_multi_strip)

if __name__ == '__main__': 
    main()
