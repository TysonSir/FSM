import os

workspaceFolder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print('workspaceFolder:', workspaceFolder)

app_dir = os.path.join(workspaceFolder, 'app')
output_dir = os.path.join(workspaceFolder, 'output')

build_dir = os.path.join(output_dir, 'build')
dist_dir = os.path.join(output_dir, 'dist')
spec_path = output_dir

def exec_cmd(work_dir, cmd):
    print(f'exec_cmd: {cmd}')
    dir_backup = os.getcwd()
    os.chdir(work_dir)
    with os.popen(cmd) as pf:
        print(pf.read())
    os.chdir(dir_backup)
