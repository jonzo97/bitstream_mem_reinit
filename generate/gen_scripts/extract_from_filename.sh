#!/bin/bash

source ~/meminit/utils/init_setup.sh

# WIDTH=1
# DEPTH= $((16384 * 2))
# DEPTHNAME='32k'
# DATA='0'
# PERLINE=256
# INIT_FRMT='hex'
DESIGNDIR="designs/$1"
echo $DESIGNDIR
export DESIGNDIR
mkdir -p $DESIGNDIR

#python3 utils/memmaker.py $DESIGNDIR/init.txt $WIDTH $DEPTH $DATA $PERLINE
#python3 utils/make_top.py $DESIGNDIR/top.sv $WIDTH $DEPTH $DESIGNDIR/init.txt $INIT_FRMT
#$XRAY_VIVADO -mode batch -source utils/generate.tcl

$XRAY_BIT2FASM $DESIGNDIR/top.bit > $DESIGNDIR/extracted.fasm

bash utils/extract.sh $DESIGNDIR/top.bit $DESIGNDIR/extracted.mem

