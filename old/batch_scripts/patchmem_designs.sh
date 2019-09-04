#!/bin/bash

INIT="init.txt"

source gen_scripts/patchmem_control.sh 1      16k     $INIT
source gen_scripts/patchmem_control.sh 2      8k      $INIT
source gen_scripts/patchmem_control.sh 3      4k      $INIT
# source gen_scripts/patchmem_control.sh 4      4k      $INIT
source gen_scripts/patchmem_control.sh 5      2k      $INIT
source gen_scripts/patchmem_control.sh 8      2k      $INIT
source gen_scripts/patchmem_control.sh 9      2k      $INIT
source gen_scripts/patchmem_control.sh 15     1k      $INIT
source gen_scripts/patchmem_control.sh 16     1k      $INIT
source gen_scripts/patchmem_control.sh 18     1k      $INIT
source gen_scripts/patchmem_control.sh 32     512     $INIT
# source gen_scripts/patchmem_control.sh 64     256     $INIT
# source gen_scripts/gen_and_extract.sh 128 128 128 2
# source gen_scripts/gen_and_extract.sh 256 64 64 1
# source gen_scripts/gen_and_extract.sh 512 32 32 1
# source gen_scripts/gen_and_extract.sh 1024 16 16 1
# source gen_scripts/gen_and_extract.sh 2048 8 8 1
# source gen_scripts/gen_and_extract.sh 4092 4 4 1



# INIT="init.txt"
# SIZE=32
# for (( c=1; c<64; c*2 ))
# do  
#    echo "Welcome $c times"
# done