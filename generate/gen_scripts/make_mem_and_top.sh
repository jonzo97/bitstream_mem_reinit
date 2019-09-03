#!/bin/bash

source ~/meminit/utils/init_setup.sh

WIDTH=($1)
DEPTHNAME=($2)
DATA='0'
INITFILE='init.txt'
if [ $# -ge 3 ]; then
    DATA=($3)
fi
if [ $# -ge 4 ]; then
    INITFILE=($4)
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
echo $DESIGNDIR
export DESIGNDIR
mkdir -p $DESIGNDIR
mkdir -p $DESIGNDIR/mem 
mkdir -p $DESIGNDIR/logs

python3 utils/memmaker.py $DESIGNDIR/mem/$INITFILE $WIDTH $DEPTH $DATA $PERLINE
python3 utils/make_top.py $DESIGNDIR/top.sv $WIDTH $DEPTH $DESIGNDIR/mem/$INITFILE.txt 
