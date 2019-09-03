create_project -force -part $::env(XRAY_PART) design design

read_verilog designs/des1/memory.sv
read_verilog designs/top/1_by_16k.sv

synth_design -top top

set_property CFGBVS VCCO [current_design]
set_property CONFIG_VOLTAGE 3.3 [current_design]
set_property BITSTREAM.GENERAL.PERFRAMECRC YES [current_design]
set_param tcl.collectionResultDisplayLimit 0

#My line
set_property BITSTREAM.General.UnconstrainedPins {Allow} [current_design]


place_design
route_design

write_checkpoint -force design.dcp

write_bitstream -force bit/1_by_16k.bit
