create_project -force -part $::env(XRAY_PART) bigmem_test bigmem_test

set_param general.maxBackupLogs 0
read_verilog $::env(DESIGNDIR)/top.sv

synth_design -top top

set_property CFGBVS VCCO [current_design]
set_property CONFIG_VOLTAGE 3.3 [current_design]
set_property BITSTREAM.GENERAL.PERFRAMECRC YES [current_design]
set_param tcl.collectionResultDisplayLimit 0
set_property BITSTREAM.General.UnconstrainedPins {Allow} [current_design]

place_design
route_design

write_checkpoint -force $::env(DESIGNDIR)/report.dcp
write_bitstream -force $::env(DESIGNDIR)/top.bit


set fp [open "$::env(DESIGNDIR)/design.csv" "w"]
puts $fp "site,IS_CLKARDCLK_INVERTED,IS_CLKBWRCLK_INVERTED"
foreach ram [get_cells "roi/inst_*/ram"] {
    set site [get_sites -of_objects [get_bels -of_objects $ram]]
    set IS_CLKARDCLK_INVERTED [get_property IS_CLKARDCLK_INVERTED $ram]
    set IS_CLKBWRCLK_INVERTED [get_property IS_CLKBWRCLK_INVERTED $ram]
    puts $fp "$site,$IS_CLKARDCLK_INVERTED,$IS_CLKBWRCLK_INVERTED"
}
close $fp
