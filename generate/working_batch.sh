#!/bin/sh
# source gen_scripts/do_everything.sh 4 16k 8 1000
# source gen_scripts/do_everything.sh 4 16k 4 0100
# source gen_scripts/do_everything.sh 4 16k 2 0010
# source gen_scripts/do_everything.sh 4 16k 1 0001
#script drname width depthname depth perline data subtitle

source generate/do_everything.sh 72k_8_28 18 4k 4096 16 00aa 00aa
source generate/do_everything.sh 72k_8_28 18 4k 4096 16 0055 0055
source generate/do_everything.sh 72k_8_28 18 4k 4096 16 15400 15400
source generate/do_everything.sh 72k_8_28 18 4k 4096 16 aa00 aa00
source generate/do_everything.sh 72k_8_28 18 4k 4096 16 20000 20000_ptop
source generate/do_everything.sh 72k_8_28 18 4k 4096 16 00100 00100_pbot
source generate/do_everything.sh 72k_8_28 18 4k 4096 16 20100 20100_p
source generate/do_everything.sh 72k_8_28 18 4k 4096 16 154aa 154aa_tile
source generate/do_everything.sh 72k_8_28 18 4k 4096 16 aa55 aa55_tile

source generate/do_everything.sh 36k 1 32k 32768 256    1  
source generate/do_everything.sh 36k 2 16k 16384 128    2 
source generate/do_everything.sh 36k 4 8k 8192 64       a  
source generate/do_everything.sh 36k 8 4k 4096 32       f0
source generate/do_everything.sh 36k 18 2k 2048 16      154aa
source generate/do_everything.sh 36k 36 1k 1024 8       552a954aa
source generate/do_everything.sh 36k 64 512 512 4       ffff0000
source generate/do_everything.sh 36k 128 256 256 2      ffff0000ffff0000
source generate/do_everything.sh 36k 256 128 128 1      ffff0000ffff0000ffff0000ffff0000

source generate/do_everything.sh 72k 1      64k 65636 256    1  
source generate/do_everything.sh 72k 2      32k 32768 128    2 
source generate/do_everything.sh 72k 4      16k 16384 64       a  
source generate/do_everything.sh 72k 9      8k  8192 32       1f0
source generate/do_everything.sh 72k 18     4k  4096 16      154aa
source generate/do_everything.sh 72k 36     2k  2048 8       552a954aa
source generate/do_everything.sh 72k 64     1k  1024 4       ffff0000
source generate/do_everything.sh 72k 128    512 512 2      ffff0000ffff0000
source generate/do_everything.sh 72k 256    256 256 1      ffff0000ffff0000ffff0000ffff0000



# source generate/do_everything.sh 72k 16 4k 4096 16 
# source generate/do_everything.sh 72k 16 4k 4096 16 
# source generate/do_everything.sh 72k 16 4k 4096 16 
# source generate/do_everything.sh 72k 16 4k 4096 16 
# source generate/do_everything.sh 72k 16 4k 4096 16 
# source generate/do_everything.sh 72k 16 4k 4096 16 
# source generate/do_everything.sh 72k 16 4k 4096 16 
# source generate/do_everything.sh 72k 16 4k 4096 16 
# source generate/do_everything.sh 72k 16 4k 4096 16  


