$XRAY_BIT2FASM bit/1_by_16k.bit > fasm/1_by_16k.fasm
bash utils/extract.sh bit/1_by_16k.bit mem/1_by_16k.mem

$XRAY_BIT2FASM bit/1_by_32k.bit > fasm/1_by_32k.fasm
bash utils/extract.sh bit/1_by_32k.bit mem/1_by_32k.mem

bash utils/extract.sh bit/2_by_8k.bit mem/2_by_8k.mem
$XRAY_BIT2FASM bit/2_by_8k.bit > fasm/2_by_8k.fasm
bash utils/extract.sh bit/3_by_5k.bit mem/3_by_5k.mem
$XRAY_BIT2FASM bit/3_by_5k.bit > fasm/3_by_5k.fasm
