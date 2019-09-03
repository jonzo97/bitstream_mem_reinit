

# WIDTH=9
# DEPTH=8k

# source gen_scripts/gen_and_extract.sh $WIDTH $DEPTH 1000.txt 1000 
# source gen_scripts/gen_and_extract.sh $WIDTH $DEPTH 0100.txt 0100 
# source gen_scripts/gen_and_extract.sh $WIDTH $DEPTH 0010.txt 0010 
# source gen_scripts/gen_and_extract.sh $WIDTH $DEPTH 0001.txt 0001 


WIDTH=18
DEPTHNAME=4k
DPTH=4096
ADJUSTED_DEPTH=1024
PERLINE=4

source gen_scripts/pattern_init_maker.sh $WIDTH $DEPTHNAME $ADJUSTED_DEPTH '3f000 0f000 0f000 0f000' 3000 $PERLINE
source gen_scripts/pattern_init_maker.sh $WIDTH $DEPTHNAME $ADJUSTED_DEPTH '0f000 3f000 0f000 0f000' 0300 $PERLINE
source gen_scripts/pattern_init_maker.sh $WIDTH $DEPTHNAME $ADJUSTED_DEPTH '0f000 0f000 3f000 0f000' 0030 $PERLINE
source gen_scripts/pattern_init_maker.sh $WIDTH $DEPTHNAME $ADJUSTED_DEPTH '0f000 0f000 0f000 3f000' 0003 $PERLINE
source gen_scripts/pattern_init_maker.sh $WIDTH $DEPTHNAME $ADJUSTED_DEPTH '2f000 0f000 0f000 0f000' 2000 $PERLINE
source gen_scripts/pattern_init_maker.sh $WIDTH $DEPTHNAME $ADJUSTED_DEPTH '1f000 0f000 0f000 0f000' 1000 $PERLINE

source gen_scripts/gen_and_extract.sh $WIDTH $DEPTHNAME 3000 
source gen_scripts/gen_and_extract.sh $WIDTH $DEPTHNAME 0300 
source gen_scripts/gen_and_extract.sh $WIDTH $DEPTHNAME 0030 
source gen_scripts/gen_and_extract.sh $WIDTH $DEPTHNAME 0003 
source gen_scripts/gen_and_extract.sh $WIDTH $DEPTHNAME 0003 
source gen_scripts/gen_and_extract.sh $WIDTH $DEPTHNAME 0003 
