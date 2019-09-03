create_project -force -part $::env(XRAY_PART) bigmem_test bigmem_test

read_verilog designs/des1/memory.sv
read_verilog designs/top/1_by_16k.sv

synth_design -top top

set_property CFGBVS VCCO [current_design]
set_property CONFIG_VOLTAGE 3.3 [current_design]
set_property BITSTREAM.GENERAL.PERFRAMECRC YES [current_design]
set_param tcl.collectionResultDisplayLimit 0
set_property BITSTREAM.General.UnconstrainedPins {Allow} [current_design]

place_design
route_design

write_checkpoint -force 1_by_16k.dcp
write_bitstream -force bit/1_by_16k.bit

set_property IS_ENABLED 0 [get_files 1_by_16k.sv]
read_verilog designs/top/1_by_32k.sv
synth_design -top top
set_property CFGBVS VCCO [current_design]
set_property CONFIG_VOLTAGE 3.3 [current_design]
set_property BITSTREAM.GENERAL.PERFRAMECRC YES [current_design]
set_param tcl.collectionResultDisplayLimit 0
set_property BITSTREAM.General.UnconstrainedPins {Allow} [current_design]
place_design
route_design
write_checkpoint -force 1_by_32k.dcp
write_bitstream -force bit/1_by_32k.bit

set_property IS_ENABLED 0 [get_files 1_by_32k.sv]
read_verilog designs/top/2_by_8k.sv
synth_design -top top
set_property CFGBVS VCCO [current_design]
set_property CONFIG_VOLTAGE 3.3 [current_design]
set_property BITSTREAM.GENERAL.PERFRAMECRC YES [current_design]
set_param tcl.collectionResultDisplayLimit 0
set_property BITSTREAM.General.UnconstrainedPins {Allow} [current_design]
place_design
route_design
write_checkpoint -force 2_by_8k.dcp
write_bitstream -force bit/2_by_8k.bit

set_property IS_ENABLED 0 [get_files 2_by_8k.sv]
read_verilog designs/top/3_by_5k.sv
synth_design -top top
set_property CFGBVS VCCO [current_design]
set_property CONFIG_VOLTAGE 3.3 [current_design]
set_property BITSTREAM.GENERAL.PERFRAMECRC YES [current_design]
set_param tcl.collectionResultDisplayLimit 0
set_property BITSTREAM.General.UnconstrainedPins {Allow} [current_design]
place_design
route_design
write_checkpoint -force 3_by_5k.dcp
write_bitstream -force bit/3_by_5k.bit
