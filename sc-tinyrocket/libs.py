import siliconcompiler

OPENLANE='/path/to/OpenLane'

def lib_setup(chip):
    ## sram_64x21
    libname = 'sky130sram_32x256'
    lib = siliconcompiler.Chip(libname)

    stackup = '5M1LI' # TODO: this should this be extracted from something
    version = 'v0_0_2'

    lib.set('package', 'version', version)

    lib.set('asic', 'pdk', 'skywater130b_demo')
    lib.set('asic', 'stackup', stackup)

    lib.add('model', 'timing', 'nldm', 'typical', f'{OPENLANE}/pdks/sky130B/libs.ref/sky130_sram_macros/lib/sky130_sram_1kbyte_1rw1r_32x256_8_TT_1p8V_25C.lib')
    lib.add('model', 'layout', 'lef', stackup, f'{OPENLANE}/pdks/sky130B/libs.ref/sky130_sram_macros/lef/sky130_sram_1kbyte_1rw1r_32x256_8.lef')
    lib.add('model', 'layout', 'gds', stackup, f'{OPENLANE}/pdks/sky130B/libs.ref/sky130_sram_macros/gds/sky130_sram_1kbyte_1rw1r_32x256_8.gds')

    chip.import_library(lib)

    ## sram_1024x32
    libname = 'sky130sram_32x512'
    lib = siliconcompiler.Chip(libname)

    stackup = '5M1LI' # TODO: this should this be extracted from something
    version = 'v0_0_2'

    lib.set('package', 'version', version)

    lib.set('asic', 'pdk', 'skywater130b_demo')
    lib.set('asic', 'stackup', stackup)

    lib.add('model', 'timing', 'nldm', 'typical', f'{OPENLANE}/pdks/sky130B/libs.ref/sky130_sram_macros/lib/sky130_sram_2kbyte_1rw1r_32x512_8_TT_1p8V_25C.lib')
    lib.add('model', 'layout', 'lef', stackup, f'{OPENLANE}/pdks/sky130B/libs.ref/sky130_sram_macros/lef/sky130_sram_2kbyte_1rw1r_32x512_8.lef')
    lib.add('model', 'layout', 'gds', stackup, f'{OPENLANE}/pdks/sky130B/libs.ref/sky130_sram_macros/gds/sky130_sram_2kbyte_1rw1r_32x512_8.gds')

    chip.import_library(lib)

    ## sram_1024x37, sram_4096x8
    libname = 'sky130sram_8x1024'
    lib = siliconcompiler.Chip(libname)

    stackup = '5M1LI' # TODO: this should this be extracted from something
    version = 'v0_0_2'

    lib.set('package', 'version', version)

    lib.set('asic', 'pdk', 'skywater130b_demo')
    lib.set('asic', 'stackup', stackup)

    lib.add('model', 'timing', 'nldm', 'typical', f'{OPENLANE}/pdks/sky130B/libs.ref/sky130_sram_macros/lib/sky130_sram_1kbyte_1rw1r_8x1024_8_TT_1p8V_25C.lib')
    lib.add('model', 'layout', 'lef', stackup, f'{OPENLANE}/pdks/sky130B/libs.ref/sky130_sram_macros/lef/sky130_sram_1kbyte_1rw1r_8x1024_8.lef')
    lib.add('model', 'layout', 'gds', stackup, f'{OPENLANE}/pdks/sky130B/libs.ref/sky130_sram_macros/gds/sky130_sram_1kbyte_1rw1r_8x1024_8.gds')

    chip.import_library(lib)
