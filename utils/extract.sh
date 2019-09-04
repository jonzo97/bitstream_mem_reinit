#!/bin/bash
#don't source or run with the dot, call as bash

INFILE=$(pwd)/$1
OUTFILE=$(pwd)/$2
#INFILE=~/bigmems/$1
#OUTFILE=~/bigmems/$2


echo "Extracting " $INFILE " to " $OUTFILE

cd ~/meminit
source utils/init_setup.sh
source utils/extract_mem.sh -i $INFILE -o $OUTFILE



#cd ~/bigmems