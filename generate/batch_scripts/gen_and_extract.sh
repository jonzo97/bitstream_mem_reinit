#!/bin/bash


source gen_scripts/gen_and_extract.sh   1     16k     init.txt
source gen_scripts/gen_and_extract.sh   2     8k      init.txt
source gen_scripts/gen_and_extract.sh   4     4k      init.txt
source gen_scripts/gen_and_extract.sh   8     2k      init.txt
source gen_scripts/gen_and_extract.sh   9     2k      init.txt
source gen_scripts/gen_and_extract.sh   16    1k      init.txt
source gen_scripts/gen_and_extract.sh   18    1k      init.txt
source gen_scripts/gen_and_extract.sh   32    512     init.txt
source gen_scripts/gen_and_extract.sh   64    256     init.txt
source gen_scripts/gen_and_extract.sh   3     4k      init.txt
source gen_scripts/gen_and_extract.sh   5     2k      init.txt
source gen_scripts/gen_and_extract.sh   15    1k      init.txt
# source gen_scripts/gen_and_extract.sh 128 128 128 2
# source gen_scripts/gen_and_extract.sh 256 64 64 1
# source gen_scripts/gen_and_extract.sh 512 32 32 1
# source gen_scripts/gen_and_extract.sh 1024 16 16 1
# source gen_scripts/gen_and_extract.sh 2048 8 8 1
# source gen_scripts/gen_and_extract.sh 4092 4 4 1
