get_pins [get_cells mem/ram_reg]
get_nets [get_cells mem/ram_reg]

set rampins [get_pins -of_objects [get_cells mem/ram_reg]]
foreach rpin $rampins {
    puts [get_bel_pins -of_objects $rpin]
}

set ramnets [get_nets -of_objects [get_cells mem/ram_reg]]
foreach rnet $rampins {
    puts [get_bel_pins -of_objects $rnet]
}

foreach rnet [get_nets -of_objects [get_cells mem/ram_reg]] {
    puts $rnet
    puts [get_bel_pins -of_objects $rnet]
}


foreach ram [get_cells mem/ram_reg] {
    puts $ram
    foreach rnet [get_nets -of_objects $ram]] {
        #puts "    "$rnet
        puts [get_bel_pins -of_objects $rnet]
    }
    foreach rpin [get_pins -of_objects $ram]] {
        #puts $rpin
        puts "    [get_bel_pins -of_objects $rpin]"
    }
}






set bpinset [get_bel_pins -of_objects [get_pins -of_objects [get_cells mem/ram_reg]]]
foreach bpin bpinset {
puts $bpin

}


get_bel_pins -of_objects [get_pins -of_objects [get_cells mem/ram_reg]]


set DESIGNDIR designs/16_by_1k
write_checkpoint -force ${DESIGNDIR}/report.dcp


#foreach ram [get_cells "roi/inst_*/ram"] {
#    set site [get_sites -of_objects [get_bels -of_objects $ram]]
#    set IS_CLKARDCLK_INVERTED [get_property IS_CLKARDCLK_INVERTED $ram]
#    set IS_CLKBWRCLK_INVERTED [get_property IS_CLKBWRCLK_INVERTED $ram]
#    puts $fp "$site,$IS_CLKARDCLK_INVERTED,$IS_CLKBWRCLK_INVERTED"
#}