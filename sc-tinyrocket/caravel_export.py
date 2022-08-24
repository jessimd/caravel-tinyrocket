import subprocess

CARAVEL_USER_PROJECT = '/home/ubuntu/caravel-tinyrocket'

job_name = 'job0'

# core_name = 'ChipTop'

def main():

    # GL
    subprocess.run(['rm', '-r', CARAVEL_USER_PROJECT + '/verilog/gl'])
    subprocess.run(['mkdir', CARAVEL_USER_PROJECT + '/verilog/gl'])
    # subprocess.run(['cp', core_name + '.vg', CARAVEL_USER_PROJECT + '/verilog/gl/' + core_name + '.vg'])
    subprocess.run(['cp', 'user_project_wrapper.vg', CARAVEL_USER_PROJECT + '/verilog/gl/user_project_wrapper.v'])

    # RTL
    subprocess.run(['rm', '-r', CARAVEL_USER_PROJECT + '/verilog/rtl'])
    subprocess.run(['mkdir', CARAVEL_USER_PROJECT + '/verilog/rtl'])
    # subprocess.run(['cp', 'build/' + core_name + '/' + job_name + '/convert/0/outputs/' + core_name + '.v', CARAVEL_USER_PROJECT + '/verilog/rtl/' + core_name + '.v'])
    subprocess.run(['cp', 'user_project_wrapper.v', CARAVEL_USER_PROJECT + '/verilog/rtl/user_project_wrapper.v'])

    # GDS
    subprocess.run(['rm', '-r', CARAVEL_USER_PROJECT + '/gds'])
    subprocess.run(['mkdir', CARAVEL_USER_PROJECT + '/gds'])
    # subprocess.run(['cp', core_name + '.gds', CARAVEL_USER_PROJECT + '/gds/' + core_name + '.gds'])
    subprocess.run(['cp', 'build/user_project_wrapper/' + job_name + '/export/0/outputs/user_project_wrapper.gds', CARAVEL_USER_PROJECT + '/gds/user_project_wrapper.gds'])

    # LEF
    subprocess.run(['rm', '-r', CARAVEL_USER_PROJECT + '/lef'])
    subprocess.run(['mkdir', CARAVEL_USER_PROJECT + '/lef'])
    # subprocess.run(['cp', core_name + '.lef', CARAVEL_USER_PROJECT + '/lef/' + core_name + '.lef'])
    subprocess.run(['cp', 'build/user_project_wrapper/' + job_name + '/export/0/inputs/user_project_wrapper.lef', CARAVEL_USER_PROJECT + '/lef/user_project_wrapper.lef'])

    # DEF
    subprocess.run(['rm', '-r', CARAVEL_USER_PROJECT + '/def'])
    subprocess.run(['mkdir', CARAVEL_USER_PROJECT + '/def'])
    # subprocess.run(['cp', core_name + '.def', CARAVEL_USER_PROJECT + '/def/' + core_name + '.def'])
    subprocess.run(['cp', 'build/user_project_wrapper/' + job_name + '/export/0/inputs/user_project_wrapper.def', CARAVEL_USER_PROJECT + '/def/user_project_wrapper.def'])

    # SDC
    subprocess.run(['rm', '-r', CARAVEL_USER_PROJECT + '/sdc'])
    subprocess.run(['mkdir', CARAVEL_USER_PROJECT + '/sdc'])
    # subprocess.run(['cp', 'build/' + core_name + '/' + job_name + '/export/0/inputs/' + core_name + '.sdc', CARAVEL_USER_PROJECT + '/sdc/' + core_name + '.sdc'])
    subprocess.run(['cp', 'build/user_project_wrapper/' + job_name + '/export/0/inputs/user_project_wrapper.sdc', CARAVEL_USER_PROJECT + '/sdc/user_project_wrapper.sdc'])


if __name__ == '__main__':
    main()
