create_project -force -part $::env(XRAY_PART) bigmem_test bigmem_test

#set_param general.maxBackupLogs 0
read_verilog $::env(DESIGNDIR)/top.sv

synth_design -top top

set_property CFGBVS VCCO [current_design]
set_property CONFIG_VOLTAGE 3.3 [current_design]
set_property BITSTREAM.GENERAL.PERFRAMECRC YES [current_design]
set_param tcl.collectionResultDisplayLimit 0
set_property BITSTREAM.General.UnconstrainedPins {Allow} [current_design]

place_design
route_design

write_checkpoint -force $::env(DESIGNDIR)/logs/report.dcp
write_bitstream -force $::env(DESIGNDIR)/top.bit

