import siliconcompiler

def lib_setup(chip):
    ## sram_64x21
    libname = 'sky130sram_64x21'
    lib = siliconcompiler.Chip(libname)

    stackup = '5M1LI' # TODO: this should this be extracted from something
    version = 'v0_0_2'

    lib.set('package', 'version', version)

    lib.set('asic', 'pdk', 'skywater130b_demo')
    lib.set('asic', 'stackup', stackup)

    lib.add('model', 'timing', 'nldm', 'typical', 'srams/sram_64x21/sky130_sram_0kbytes_1rw_21x64_21_TT_1p8V_25C.lib')
    lib.add('model', 'layout', 'lef', stackup, 'srams/sram_64x21/sky130_sram_0kbytes_1rw_21x64_21.lef')
    lib.add('model', 'layout', 'gds', stackup, 'srams/sram_64x21/sky130_sram_0kbytes_1rw_21x64_21.gds')

    chip.import_library(lib)

    ## sram_1024x32
    libname = 'sky130sram_1024x32'
    lib = siliconcompiler.Chip(libname)

    stackup = '5M1LI' # TODO: this should this be extracted from something
    version = 'v0_0_2'

    lib.set('package', 'version', version)

    lib.set('asic', 'pdk', 'skywater130b_demo')
    lib.set('asic', 'stackup', stackup)

    lib.add('model', 'timing', 'nldm', 'typical', 'srams/sram_1024x32/sky130_sram_4kbytes_1rw_32x1024_32_TT_1p8V_25C.lib')
    lib.add('model', 'layout', 'lef', stackup, 'srams/sram_1024x32/sky130_sram_4kbytes_1rw_32x1024_32.lef')
    lib.add('model', 'layout', 'gds', stackup, 'srams/sram_1024x32/sky130_sram_4kbytes_1rw_32x1024_32.gds')

    chip.import_library(lib)

    ## sram_1024x37
    libname = 'sky130sram_1024x37'
    lib = siliconcompiler.Chip(libname)

    stackup = '5M1LI' # TODO: this should this be extracted from something
    version = 'v0_0_2'

    lib.set('package', 'version', version)

    lib.set('asic', 'pdk', 'skywater130b_demo')
    lib.set('asic', 'stackup', stackup)

    lib.add('model', 'timing', 'nldm', 'typical', 'srams/sram_1024x37/sky130_sram_5kbytes_1rw_37x1024_37_TT_1p8V_25C.lib')
    lib.add('model', 'layout', 'lef', stackup, 'srams/sram_1024x37/sky130_sram_5kbytes_1rw_37x1024_37.lef')
    lib.add('model', 'layout', 'gds', stackup, 'srams/sram_1024x37/sky130_sram_5kbytes_1rw_37x1024_37.gds')

    chip.import_library(lib)

    ## sram_4096x8
    libname = 'sky130sram_4096x8'
    lib = siliconcompiler.Chip(libname)

    stackup = '5M1LI' # TODO: this should this be extracted from something
    version = 'v0_0_2'

    lib.set('package', 'version', version)

    lib.set('asic', 'pdk', 'skywater130b_demo')
    lib.set('asic', 'stackup', stackup)

    lib.add('model', 'timing', 'nldm', 'typical', 'srams/sram_4096x8/sky130_sram_4kbyte_1rw_32x1024_8_TT_1p8V_25C.lib')
    lib.add('model', 'layout', 'lef', stackup, 'srams/sram_4096x8/sky130_sram_4kbyte_1rw_32x1024_8.lef')
    lib.add('model', 'layout', 'gds', stackup, 'srams/sram_4096x8/sky130_sram_4kbyte_1rw_32x1024_8.gds')

    chip.import_library(lib)
