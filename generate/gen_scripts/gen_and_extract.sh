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
# PERLINE=($4)


WIDTH=($1)
DEPTHNAME=($2)
DATA='0'
INITNAME='init'
OUTNAME='extracted'
if [ $# -ge 3 ]
  then
    INITNAME=($3)
    OUTNAME=$INITNAME
fi
if [ $# -ge 4 ]
  then
    OUTNAME=($4)
fi
FASMOUT="fasm/$OUTNAME.fasm"
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


            


DESIGNDIR="designs/${WIDTH}_by_${DEPTHNAME}"
echo $DESIGNDIR
export DESIGNDIR
mkdir -p $DESIGNDIR
mkdir -p $DESIGNDIR/logs
mkdir -p $DESIGNDIR/fasm

#python3 utils/memmaker.py $DESIGNDIR/init.txt $WIDTH $DEPTH $DATA $PERLINE
python3 utils/make_top.py $DESIGNDIR/top.sv $WIDTH $DEPTH $DESIGNDIR/mem/$INITNAME.txt
$XRAY_VIVADO -mode batch -source utils/generate.tcl -log $DESIGNDIR/logs/vivado.log -journal $DESIGNDIR/logs/vivado.jou

$XRAY_BIT2FASM $DESIGNDIR/top.bit > $DESIGNDIR/$FASMOUT

bash utils/extract.sh $DESIGNDIR/top.bit $DESIGNDIR/$OUTNAME.mem
#python3 utils/mem2init.py ${WIDTH}_by_${DEPTHNAME} $WIDTH $DEPTH $PERLINE


# REALWID=0
# PERLINE=0
# if [ "$WIDTH" -le "1" ]; then
#     REALWID=1
#     PERLINE=256
# elif [ "$WIDTH" -le "2" ]; then
#     REALWID=2
#     PERLINE=128
# elif [ "$WIDTH" -le "4" ]; then
#     REALWID=4
#     PERLINE=64
# elif [ "$WIDTH" -le "8" ]; then
#     REALWID=8
#     PERLINE=32
# elif [ "$WIDTH" -le "9" ]; then
#     REALWID=9
#     PERLINE=32
# elif [ "$WIDTH" -le "18" ]; then
#     REALWID=18
#     PERLINE=16
# elif [ "$WIDTH" -le "36" ]; then
#     REALWID=36
#     PERLINE=8
# else
#     return 1
# fi 