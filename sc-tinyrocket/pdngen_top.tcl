
# Add PDN connections for each voltage domain.
add_global_connection -net vccd1 -pin_pattern "^VPWR$" -power
add_global_connection -net vssd1 -pin_pattern "^VGND$" -ground
add_global_connection -net vccd1 -pin_pattern "^POWER$" -power
add_global_connection -net vssd1 -pin_pattern "^GROUND$" -ground
add_global_connection -net vccd1 -pin_pattern vccd1
add_global_connection -net vssd1 -pin_pattern vssd1
global_connect

set_voltage_domain -name Core -power vccd1 -ground vssd1 -secondary_power {vccd2 vssd2 vdda1 vssa1 vdda2 vssa2}
#set_voltage_domain -name Core -power vccd1 -ground vssd1
define_pdn_grid -name top_grid -voltage_domain Core -starts_with POWER -pins {met4 met5}

add_pdn_stripe -grid top_grid -layer met1 -width 0.48 -pitch 5.44 -spacing 2.24 -offset 0 -starts_with POWER -nets {vccd1 vssd1}
add_pdn_stripe -grid top_grid -layer met4 -width 3.1 -pitch 90 -spacing 41.9 -offset 5 -starts_with POWER -extend_to_core_ring -nets {vccd1 vssd1}
add_pdn_stripe -grid top_grid -layer met5 -width 3.1 -pitch 90 -spacing 41.9 -offset 5 -starts_with POWER -extend_to_core_ring -nets {vccd1 vssd1}
add_pdn_connect -grid top_grid -layers {met1 met4}
add_pdn_connect -grid top_grid -layers {met4 met5}

add_pdn_ring -grid top_grid -layers {met4 met5} -widths {3.1 3.1} -spacings {1.7 1.7} -core_offset {12.45 12.45}
#add_pdn_ring -grid top_grid -layers {met4 met5} -widths {3.1 3.1} -spacings {1.7 1.7} -core_offset {14 14}

define_pdn_grid -macro -name macro -voltage_domain Core -halo 3.0 -starts_with POWER -grid_over_boundary -cells {sky130_sram_1kbyte_1rw1r_8x1024_8, sky130_sram_2kbyte_1rw1r_32x512_8, sky130_sram_1kbyte_1rw1r_32x256_8}
add_pdn_connect -grid macro -layers {met4 met5}

# Done defining commands; generate PDN.
pdngen