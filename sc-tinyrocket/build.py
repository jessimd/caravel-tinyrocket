# Copyright 2020 Silicon Compiler Authors. All Rights Reserved.
import os
import shutil

from siliconcompiler.core import Chip
from siliconcompiler.floorplan import Floorplan

from libs import lib_setup

###
# Example Skywater130 / "Caravel" macro hardening with SiliconCompiler
#
# This script builds a minimal 'ChipTop' example into the Caravel harness provided by
# eFabless for their MPW runs, connecting the 3 I/O signals to the wrapper's I/O pins.
# Other Caravel signals such as the Wishbone bus, IRQ, etc. are ignored.
#
# These settings have not been tested with one of eFabless' MPW runs yet, but
# it demonstrates how to run a 'caravel_user_project' build process using SiliconCompiler.
# The basic idea is to harden the core design as a macro with half of a power delivery grid and
# a blockage on the top metal layer. The top-level design's I/O signals are then routed to the
# macro pins, and the top-level PDN is connected by running its top-layer straps over the macro
# and connecting the straps with 'define_pdn_grid -existing'.
#
# The 'pdngen' and 'macroplace' parameters used here and in 'tools/openroad/sc_floorplan.tcl'
# can demonstrate one way to insert custom TCL commands into a tool flow.
###

# User project wrapper area is 2.92mm x 3.52mm
## RAN BUILD CORE WITH DIMS:
TOP_W = 2920
TOP_H = 3520

# Margins are set to ~10mm, snapped to placement site dimensions (0.46mm x 2.72mm in sky130hd)
MARGIN_W = 9.66
MARGIN_H = 8.16

# Path to 'caravel' repository root.
CARAVEL_ROOT = '/home/ubuntu/caravel'

def configure_chip(design):
    # Minimal Chip object construction.
    chip = Chip(design)

    chip.load_target('skywater130b_demo')
    chip.load_flow('mpwflow')
    chip.set('option', 'flow', 'mpwflow')
    chip.add('option', 'define', 'USE_POWER_PINS')
    chip.set('option', 'relax', True)

    chip.set('option', 'jobname', 'job0')

    return chip

def build_top():
    # The 'hearbeat' RTL goes in a modified 'user_project_wrapper' object, see sources.
    design = 'user_project_wrapper'
    chip = configure_chip(design)
    
    chip.set('input', 'verilog', f'{CARAVEL_ROOT}/verilog/rtl/defines.v')
    chip.set('tool', 'openroad', 'var', 'place', '0', 'place_density', ['0.60'])
    chip.add('tool', 'openroad', 'var', 'place', '0', 'pad_global_place', ['2'])
    chip.add('tool', 'openroad', 'var', 'place', '0', 'pad_detail_place', ['2'])
    chip.set('tool', 'openroad', 'var', 'route', '0', 'grt_allow_congestion', ['true'])
    chip.clock('wb_clk_i', period=20)

    chip.add('input', 'verilog', 'user_project_wrapper.v')
    chip.add('input', 'verilog', 'ChipTop.v')
    chip.add('input', 'verilog', '/home/ubuntu/OpenLane/pdks/sky130B/libs.ref/sky130_sram_macros/bb/sky130_sram_1kbyte_1rw1r_8x1024_8.bb.v')
    chip.add('input', 'verilog', '/home/ubuntu/OpenLane/pdks/sky130B/libs.ref/sky130_sram_macros/bb/sky130_sram_2kbyte_1rw1r_32x512_8.bb.v')
    chip.add('input', 'verilog', '/home/ubuntu/OpenLane/pdks/sky130B/libs.ref/sky130_sram_macros/bb/sky130_sram_1kbyte_1rw1r_32x256_8.bb.v')

    # Set top-level die/core area.
    chip.set('asic', 'diearea', (0, 0))
    chip.add('asic', 'diearea', (TOP_W, TOP_H))
    chip.set('asic', 'corearea', (MARGIN_W, MARGIN_H))
    chip.add('asic', 'corearea', (TOP_W - MARGIN_W, TOP_H - MARGIN_H))

    lib_setup(chip)

    chip.set('asic', 'macrolib', ['sky130sram_32x256', 'sky130sram_32x512', 'sky130sram_8x1024'])
        
    for step in ('extspice', 'drc'):
        chip.set('tool', 'magic', 'var', step, '0', 'exclude', ['sky130sram_32x256', 'sky130sram_32x512', 'sky130sram_8x1024'])
    chip.set('tool', 'netgen', 'var', 'lvs', '0', 'exclude', ['sky130sram_32x256', 'sky130sram_32x512', 'sky130sram_8x1024'])

    # Use pre-defined floorplan for the wrapper..
    chip.set('input', 'floorplan.def', 'user_project_wrapper_nogrid.def')

    # (No?) tapcells in the top-level wrapper.
    libtype = 'unithd'
    stackup = chip.get('asic', 'stackup')

    chip.set('asic', 'cells', 'buf', [])

    # Create PDN-generation script.
    pdk = chip.get('option', 'pdk')
    with open('pdngen_top.tcl', 'w') as pdnf:
        # TODO: Jinja template?
        pdnf.write('''
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
pdngen''')

    chip.set('pdk', pdk, 'aprtech', 'openroad', stackup, libtype, 'pdngen', 'pdngen_top.tcl')

    with open('macroplace_top.tcl', 'w') as mf:
        mf.write('''
# Place SRAMs
place_cell -inst_name mprj.system.tile_prci_domain.tile_reset_domain.tile.dcache.data.data_arrays_0.data_arrays_0_ext.mem_0_0.sram_4096x8_0 -origin {99.82 97.92} -orient R0 -status FIRM
place_cell -inst_name mprj.system.tile_prci_domain.tile_reset_domain.tile.dcache.data.data_arrays_0.data_arrays_0_ext.mem_0_0.sram_4096x8_1 -origin {99.82 644.64} -orient R0 -status FIRM
place_cell -inst_name mprj.system.tile_prci_domain.tile_reset_domain.tile.dcache.data.data_arrays_0.data_arrays_0_ext.mem_0_0.sram_4096x8_2 -origin {99.82 1191.36} -orient R0 -status FIRM
place_cell -inst_name mprj.system.tile_prci_domain.tile_reset_domain.tile.dcache.data.data_arrays_0.data_arrays_0_ext.mem_0_0.sram_4096x8_3 -origin {99.82 1738.08} -orient R0 -status FIRM

place_cell -inst_name mprj.system.tile_prci_domain.tile_reset_domain.tile.dcache.data.data_arrays_0.data_arrays_0_ext.mem_0_2.sram_4096x8_0 -origin {99.82 2284.8} -orient R0 -status FIRM
place_cell -inst_name mprj.system.tile_prci_domain.tile_reset_domain.tile.dcache.data.data_arrays_0.data_arrays_0_ext.mem_0_2.sram_4096x8_1 -origin {99.82 2831.52} -orient R0 -status FIRM
place_cell -inst_name mprj.system.tile_prci_domain.tile_reset_domain.tile.dcache.data.data_arrays_0.data_arrays_0_ext.mem_0_2.sram_4096x8_2 -origin {655.04 2284.8} -orient R0 -status FIRM
place_cell -inst_name mprj.system.tile_prci_domain.tile_reset_domain.tile.dcache.data.data_arrays_0.data_arrays_0_ext.mem_0_2.sram_4096x8_3 -origin {655.04 2831.52} -orient R0 -status FIRM

place_cell -inst_name mprj.system.tile_prci_domain.tile_reset_domain.tile.frontend.icache.data_arrays_0.data_arrays_0_0_ext.mem_0_0.sram_1024x32_0 -origin {1210.26 2284.8} -orient R0 -status FIRM
place_cell -inst_name mprj.system.tile_prci_domain.tile_reset_domain.tile.frontend.icache.data_arrays_0.data_arrays_0_0_ext.mem_0_0.sram_1024x32_1 -origin {1210.26 2831.52} -orient R0 -status FIRM

place_cell -inst_name mprj.system.tile_prci_domain.tile_reset_domain.tile.frontend.icache.tag_array.tag_array_ext.mem_0_0.sram_64x21 -origin {1765.48 97.92} -orient R0 -status FIRM

place_cell -inst_name mprj.system.tile_prci_domain.tile_reset_domain.tile.dcache.data.data_arrays_0.data_arrays_0_ext.mem_0_1.sram_4096x8_0 -origin {655.04 97.92} -orient R0 -status FIRM
place_cell -inst_name mprj.system.tile_prci_domain.tile_reset_domain.tile.dcache.data.data_arrays_0.data_arrays_0_ext.mem_0_1.sram_4096x8_1 -origin {655.04 644.64} -orient R0 -status FIRM
place_cell -inst_name mprj.system.tile_prci_domain.tile_reset_domain.tile.dcache.data.data_arrays_0.data_arrays_0_ext.mem_0_1.sram_4096x8_2 -origin {655.04 1191.36} -orient R0 -status FIRM
place_cell -inst_name mprj.system.tile_prci_domain.tile_reset_domain.tile.dcache.data.data_arrays_0.data_arrays_0_ext.mem_0_1.sram_4096x8_3 -origin {655.04 1738.08} -orient R0 -status FIRM

place_cell -inst_name mprj.system.tile_prci_domain.tile_reset_domain.tile.dcache.data.data_arrays_0.data_arrays_0_ext.mem_0_3.sram_4096x8_0 -origin {1210.26 97.92} -orient R0 -status FIRM
place_cell -inst_name mprj.system.tile_prci_domain.tile_reset_domain.tile.dcache.data.data_arrays_0.data_arrays_0_ext.mem_0_3.sram_4096x8_1 -origin {1210.26 644.64} -orient R0 -status FIRM
place_cell -inst_name mprj.system.tile_prci_domain.tile_reset_domain.tile.dcache.data.data_arrays_0.data_arrays_0_ext.mem_0_3.sram_4096x8_2 -origin {1210.26 1191.36} -orient R0 -status FIRM
place_cell -inst_name mprj.system.tile_prci_domain.tile_reset_domain.tile.dcache.data.data_arrays_0.data_arrays_0_ext.mem_0_3.sram_4096x8_3 -origin {1210.26 1738.08} -orient R0 -status FIRM

''')
    chip.set('pdk', pdk, 'aprtech', 'openroad', stackup, libtype, 'macroplace', 'macroplace_top.tcl')

    # Run the top-level build.
    # Using a helper method instead of chip.run, because we inject some logic between route/export.
    chip.run()
    # Add via definitions to the gate-level netlist.
    shutil.copy(chip.find_result('vg', step='addvias'), f'{design}.vg')

    return chip

def run_build(chip):
    chip.run()
    chip.summary()

def main():
    build_top()

if __name__ == '__main__':
    main()
