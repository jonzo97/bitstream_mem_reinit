#!/bin/bash

source ~/meminit/utils/init_setup.sh

# WIDTH=1
    # DEPTH= $((16384 * 2))
    # DEPTHNAME='32k'
    # DATA='0'
    # PERLINE=256
    # INIT_FRMT='hex'
    # WIDTH=($1)
    # DEPTH=($2)
    # DEPTHNAME=($3)
    # DATA=($4)
    # PERLINE=($5)
    #INIT_FRMT=($6)
    # DEPTHNAME=($1)
    # WIDTH=($2)



    # WIDTH=0
    # DEPTHNAME=0
    # DATA='0'
    # while getopts ":w:d:D:" opt; do
    #     case "$opt" in
    #     w) WIDTH=$OPTARG ;;
    #     d) DEPTHNAME=$OPTARG ;;
    #     D) DATA=$OPTARG ;;
    #     esac
    # done


WIDTH=($1)
DEPTHNAME=($2)
DATA='0'
DESIGN="test"
DESIGN_SUBDIR=''
if [ $# -ge 3 ]
  then
    DATA=($3)
fi
if [ $# -ge 4 ]
  then
    DESIGN=($4)
fi
if [ $# -ge 5 ]
  then
    DESIGN_SUBDIR="$5/"
fi
DEPTH=0
case  "$DEPTHNAME"  in
            64k|64K) DEPTH=$((2**16)) ;;
            32k|32K) DEPTH=$((2**15)) ;;
            16k|16K) DEPTH=$((2**14)) ;;
            8k|8K) DEPTH=$((2**13)) ;;
            4k|4K) DEPTH=$((2**12)) ;;
            2k|2K) DEPTH=$((2**11)) ;;
            1k|1K) DEPTH=$((2**10)) ;;
            *) DEPTH=$DEPTHNAME
        esac 

REALWID=0
PERLINE=0
if [ "$WIDTH" -le "1" ]; then
        REALWID=1
        PERLINE=256
    elif [ "$WIDTH" -le "2" ]; then
        REALWID=2
        PERLINE=128
    elif [ "$WIDTH" -le "4" ]; then
        REALWID=4
        PERLINE=64
    elif [ "$WIDTH" -le "8" ]; then
        REALWID=8
        PERLINE=32
    elif [ "$WIDTH" -le "9" ]; then
        REALWID=9
        PERLINE=32
    elif [ "$WIDTH" -le "18" ]; then
        REALWID=18
        PERLINE=16
    elif [ "$WIDTH" -le "36" ]; then
        REALWID=36
        PERLINE=8
    else
        return 1
    fi

DESIGNDIR="designs/${WIDTH}_by_${DEPTHNAME}"
#DESIGNDIR="designs/${DEPTHNAME}_by_${WIDTH}"
echo "DESIGNDIR" $DESIGNDIR
    # echo "WIDTH" $WIDTH
    # echo "REALWID" $REALWID
    # echo "DEPTH" $DEPTH
    # echo "DEPTHNAME" $DEPTHNAME
    # echo "DATA" $DATA
    # echo "PERLINE" $PERLINE
export DESIGNDIR
mkdir -p $DESIGNDIR
mkdir -p $DESIGNDIR/mem 
mkdir -p $DESIGNDIR/logs
mkdir -p $DESIGNDIR/analysis


python3 utils/memmaker.py $DESIGNDIR/mem/$DESIGN.init $WIDTH $DEPTH $DATA $PERLINE
python3 utils/make_top.py $DESIGNDIR/top.sv $WIDTH $DEPTH $DESIGNDIR/mem/$DESIGN.init #$INIT_FRMT

#$XRAY_VIVADO -mode batch -source utils/generate_and_export.tcl
$XRAY_VIVADO -mode batch -source utils/generate.tcl -log $DESIGNDIR/logs/vivado.log -journal $DESIGNDIR/logs/vivado.jou

$XRAY_BIT2FASM $DESIGNDIR/top.bit > $DESIGNDIR/$DESIGN.fasm
bash utils/extract.sh $DESIGNDIR/top.bit $DESIGNDIR/mem/$DESIGN.mem
python3 utils/addr_interpret.py -fasm $DESIGNDIR/$DESIGN.fasm -outfile $DESIGNDIR/analysis/${DESIGN}_addresses.txt
python3 utils/simplify_fasm.py -fasm $DESIGNDIR/$DESIGN.fasm -outfile $DESIGNDIR/analysis/interpreted_$DESIGN.fasm

