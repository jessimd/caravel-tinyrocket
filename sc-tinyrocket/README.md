# Hardening a Design into the Caravel Wrapper

Note: This example is for demonstration purposes only.

This directory contains a proof-of-concept build script for creating a caravel user project featuring TinyRocket and OpenRAM SRAMs. 

The version of SiliconCompiler used for this build was commit c77e7f2941b92966062b3cd3fa3c1a243339a0ba of [this SiliconCompiler fork](https://github.com/zephray/siliconcompiler/tree/sky130hs) with changes from [this pull request](https://github.com/siliconcompiler/siliconcompiler/pull/1106/files) applied to files under the 'siliconcompiler/tools/openroad' and 'tests/examples' folders. A separate build of commit 632913385035cbd749ab9547657ed4bff3585c2b of [OpenROAD](https://github.com/The-OpenROAD-Project) was used. 

In order to test building and exporting the project using SiliconCompiler run the following in this directory:

```python
python build.py
python caravel_export.py
```

Otherwise, to test the already built project, run the follwing in the caravel-tinyrocket directory

```python
make decompress
```

and then follow [this quickstart guide](https://github.com/jessimd/caravel-ml-accel/blob/main/docs/source/quickstart.rst) to run the local precheck. Note: there are known DRC errors in this build.

