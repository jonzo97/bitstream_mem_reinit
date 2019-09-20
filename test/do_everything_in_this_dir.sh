#!/bin/bash

# source ~/meminit/utils/init_setup.sh

BATCHDIR=($1)
WIDTH=($2)
DEPTHNAME=($3)
DEPTH=($4)
PERLINE=($5)
DATA=($6)
SUBTITLE=""
if [ $# -ge 7 ]
  then
    SUBTITLE="_${7}"
fi



BATCHDIR="$BATCHDIR"
export BATCH_DIR=$BATCHDIR
echo "BATCHDIR" $BATCHDIR
DESIGN="${DEPTHNAME}b${WIDTH}${SUBTITLE}"
# export DESIGN=$DESIGN
echo "DESIGN" $DESIGN
mkdir -p $BATCHDIR
mkdir -p $BATCHDIR/init
mkdir -p $BATCHDIR/mdd
mkdir -p $BATCHDIR/mem
mkdir -p $BATCHDIR/fasm
mkdir -p $BATCHDIR/vivado
mkdir -p $BATCHDIR/vivado/logs
mkdir -p $BATCHDIR/vivado/reports
mkdir -p $BATCHDIR/vivado/bs
mkdir -p $BATCHDIR/vivado/verilog
mkdir -p $BATCHDIR/analysis
mkdir -p $BATCHDIR/analysis/shortfasm
mkdir -p $BATCHDIR/analysis/addrs




python3 utils/memmaker.py $BATCHDIR/init/$DESIGN.init $WIDTH $DEPTH $DATA $PERLINE
SV_FILE_LOC="$BATCHDIR/vivado/verilog/$DESIGN.sv"
export SV_FILE_LOC
export DESIGN_NAME=$DESIGN
python3 utils/make_top.py $BATCHDIR/vivado/verilog/$DESIGN.sv $WIDTH $DEPTH $BATCHDIR/init/$DESIGN.init 

$XRAY_VIVADO -mode batch -source generate/generate.tcl -log $BATCHDIR/vivado/logs/$DESIGN.log -journal $BATCHDIR/vivado/logs/$DESIGN.jou

$XRAY_BIT2FASM $BATCHDIR/vivado/bs/$DESIGN.bit > $BATCHDIR/$DESIGN.fasm
bash utils/extract.sh $BATCHDIR/vivado/bs/$DESIGN.bit $BATCHDIR/mem/$DESIGN.mem
python3 utils/addr_interpret.py -fasm $BATCHDIR/$DESIGN.fasm -outfile $BATCHDIR/analysis/addrs/${DESIGN}.addrs
python3 utils/simplify_fasm.py -fasm $BATCHDIR/$DESIGN.fasm -outfile $BATCHDIR/analysis/shortfasm/$DESIGN.ifasm
