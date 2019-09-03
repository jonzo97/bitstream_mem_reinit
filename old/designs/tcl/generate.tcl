create_project -force -part $::env(XRAY_PART) design design

read_verilog ../../top.v
synth_design -top top

se
set_property LOCK_PINS {I0:A1 I1:A2 I2:A3 I3:A4 I4:A5 I5:A6} \
        [get_cells -quiet -filter {REF_NAME == LUT6} -hierarchical]

create_pblock roi
add_cells_to_pblock [get_pblocks roi] [get_cells roi]
resize_pblock [get_pblocks roi] -add "$::env(XRAY_ROI)"

set_property CFGBVS VCCO [current_design]
set_property CONFIG_VOLTAGE 3.3 [current_design]
set_property BITSTREAM.GENERAL.PERFRAMECRC YES [current_design]
set_param tcl.collectionResultDisplayLimit 0

#My line
set_property BITSTREAM.General.UnconstrainedPins {Allow} [current_design]


set_property CLOCK_DEDICATED_ROUTE FALSE [get_nets clk_IBUF]

place_design
route_design

write_checkpoint -force design.dcp


########################################
# Unmodified design with random LUTs

proc write_txtdata {filename} {
    puts "Writing $filename."
    set fp [open $filename w]
    foreach cell [get_cells -hierarchical -filter {REF_NAME == LUT6}] {
        set bel [get_property BEL $cell]
        set loc [get_property LOC $cell]
        set init [get_property INIT $cell]
        puts $fp "$loc $bel $init"
    }
    close $fp
}

write_bitstream -force design_0.bit
write_txtdata design_0.txt


