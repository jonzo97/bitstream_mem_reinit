#!/bin/bash

WIDTH=($1)
DEPTHNAME=($2)
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
INFILE="$DESIGNDIR/mem/init.txt"
if [ $# -ge 3 ]
  then
    INFILE="$DESIGNDIR/mem/$3"
fi
echo patchmem $DESIGNDIR
OUTFASM="$DESIGNDIR/patched.fasm"
OUTFILE="$DESIGNDIR/patched.bit"

python3 utils/readmem_patch.py -fasm $DESIGNDIR/extracted.fasm -outfile $OUTFASM -init $INFILE -width $WIDTH -depth $DEPTH -path $DESIGNDIR

# mkdir -p temp

# echo "Input Fasm File: " $OUTFASM
# echo -e "Output Bit File: " $OUTFILE "\n"

# echo "Fasm to Frames: $XRAY_FASM2FRAMES $OUTFASM temp/patched.frm"
# $XRAY_FASM2FRAMES $INFILE temp/patched.frm
# echo "Frames to Bit: $XRAY_TOOLS_DIR/xc7frames2bit --part_name $XRAY_PART --part_file $XRAY_PART_YAML --frm_file temp/patched.frm --output_file $OUTFILE"
# $XRAY_TOOLS_DIR/xc7frames2bit --part_name $XRAY_PART --part_file $XRAY_PART_YAML --frm_file temp/patched.frm --output_file $OUTFILE

# echo "Converted fasm " $OUTFASM " to bit " $OUTFILE

# rm -rf temp
# touch $DESIGNDIR/run.ok