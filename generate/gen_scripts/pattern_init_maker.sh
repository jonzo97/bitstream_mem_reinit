#!/bin/bash

source ~/meminit/utils/init_setup.sh

WIDTH=($1)
DEPTHNAME=($2)
DEPTH=($3)
DATA=($4)
INITNAME=($5)
PERLINE=($6)


DESIGNDIR="designs/${WIDTH}_by_${DEPTHNAME}"
echo $DESIGNDIR
export DESIGNDIR
mkdir -p $DESIGNDIR
mkdir -p $DESIGNDIR/mem 
mkdir -p $DESIGNDIR/logs 


python3 utils/memmaker.py $DESIGNDIR/mem/$INITNAME.txt $WIDTH $DEPTH $DATA $PERLINE
