import os, shutil
from common import *

os.chdir(app_dir)

def clear():
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)

    os.makedirs(output_dir)

if __name__ == '__main__':
    clear()

    args = ''
    args += ' --workpath %s' % build_dir
    args += ' --distpath %s' % dist_dir
    args += ' --specpath %s' % spec_path

    cmd = 'pyinstaller -Fw FS.py ' + args
    exec_cmd(app_dir, cmd)
