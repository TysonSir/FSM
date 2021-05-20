import os, sys
import shutil
from common import *

src_view = os.path.join(workspaceFolder, 'app/view')
dst_view = os.path.join(dist_dir, 'view')

src_resource = os.path.join(workspaceFolder, 'app/resource')
dst_resource = os.path.join(dist_dir, 'resource')

def copy_dir(src_dir, dst_dir):
    if os.path.exists(dst_dir):
        shutil.rmtree(dst_dir)
    shutil.copytree(src_dir, dst_dir)

def copy_file(src_file, dst_dir):
    shutil.copy(src_file, dst_dir)

if __name__ == '__main__':
    copy_dir(src_view, dst_view)
    copy_dir(src_resource, dst_resource)
    copy_file(os.path.join(workspaceFolder, 'lib/libz3.dll'), dist_dir)
    copy_file(os.path.join(workspaceFolder, 'app/config.json'), dist_dir)
    print(f'Build Success：{dist_dir}')

