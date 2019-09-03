set_property CFGBVS VCCO [current_design]
set_property CONFIG_VOLTAGE 3.3 [current_design]
set_property BITSTREAM.GENERAL.PERFRAMECRC YES [current_design]
set_property BITSTREAM.General.UnconstrainedPins {Allow} [current_design]


place_design
route_design

write_checkpoint -force design.dcp
write_bitstream -force design.bit
