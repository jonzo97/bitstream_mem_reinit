#!/bin/bash

source gen_scripts/make_mem_and_top.sh  1   16k     1                 
source gen_scripts/make_mem_and_top.sh  2   8k      2                 
source gen_scripts/make_mem_and_top.sh  3   4k      4                 
source gen_scripts/make_mem_and_top.sh  4   4k      8                 
source gen_scripts/make_mem_and_top.sh  5   2k      10                
source gen_scripts/make_mem_and_top.sh  8   2k      80                
source gen_scripts/make_mem_and_top.sh  15  1k      4000              
source gen_scripts/make_mem_and_top.sh  16  1k      8000              
source gen_scripts/make_mem_and_top.sh  18  1k      28000             
source gen_scripts/make_mem_and_top.sh  32  512     80000000          
source gen_scripts/make_mem_and_top.sh  64  256     8000000000000000  
# source gen_scripts/make_mem_and_top.sh 128 128 128 0 2 hex
# source gen_scripts/make_mem_and_top.sh 256 64 64 0 1 hex
# source gen_scripts/make_mem_and_top.sh 512 32 32 0 1 hex
# source gen_scripts/make_mem_and_top.sh 1024 16 16 0 1 hex
# source gen_scripts/make_mem_and_top.sh 2048 8 8 0 1 hex
# source gen_scripts/make_mem_and_top.sh 4092 4 4 0 1 hex
