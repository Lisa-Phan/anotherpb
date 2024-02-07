#!/bin/bash

#function to extract last cartesian coordinate from ORCA output file
get_cart() {
    #line count
    line_count=$(wc -l $1 | awk '{print $1}')
    #number of atoms
    num_atoms=$(grep -n -i 'number of atoms' *.out | tail -n 1 | awk '{print $NF}')
    #line markers for last cartesian coordinate
    cart=$(grep -i -n 'cartesian coordinates (angstroem)' $1 | cut -d':' -f1 | tail -n 1)
    #cartesian coord section ranges from line $cart_start to line $cart_end
    cart_end=$(($cart + $num_atoms + 2))
    cart_start=$((cart + 2))
    #print cartesian coordinates
    sed -n "$cart_start,$cart_end p" $1
}

#function to get xyz from gaussian gjf input with fragment 
#1: get all lines with 'Fragment'
#2: remove that tag
#3: remove all lines with #, which are either comments or part of header lines 
gjf_frag_to_xyz() {
    grep -i 'Fragment=' $1 | sed -e 's/(Fragment=[0-9])//g' | sed '/#/d'
}
