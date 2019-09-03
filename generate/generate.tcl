# parray env
# puts $::env(DESIGN_NAME)
create_project -force -part $::env(XRAY_PART) bigmem_test bigmem_test

#set_param general.maxBackupLogs 0
read_verilog $::env(SV_FILE_LOC)

synth_design -top top -flatten_hierarchy full

set_property CFGBVS VCCO [current_design]
set_property CONFIG_VOLTAGE 3.3 [current_design]
set_property BITSTREAM.GENERAL.PERFRAMECRC YES [current_design]
# set_param tcl.collectionResultDisplayLimit 0
set_property BITSTREAM.General.UnconstrainedPins {Allow} [current_design]

place_design
route_design

source generate/mdd_make.tcl
mddMake ${::env(BATCH_DIR)}/mdd/${::env(DESIGN_NAME)}

write_edif -force ${::env(BATCH_DIR)}/vivado/reports/${::env(DESIGN_NAME)}.edif
write_checkpoint -force ${::env(BATCH_DIR)}/vivado/reports/${::env(DESIGN_NAME)}.dcp
write_bitstream -force ${::env(BATCH_DIR)}/vivado/bs/${::env(DESIGN_NAME)}.bit

