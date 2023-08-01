import pytest
import shutil
from pathlib import Path
import os



cwd = Path('D:/Repo/algorithm/ns_api/')
base_name = fr'{str(cwd)}\123213412321341242131'
print(base_name)
archive = Path(rf'C:\Users\future\Desktop\eraLi')
root_dir = Path('C:/User/future/Desktop')


# setup
def test_zip():
    # os.chdir(cwd)
    assert shutil.make_archive(base_name, 'zip',base_dir=archive)
    # 删除压缩包
    os.remove(f'{base_name}.zip')