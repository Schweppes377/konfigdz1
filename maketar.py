import tarfile
import os

# Создание файлов и подкаталога для архива
os.makedirs('subdir', exist_ok=True)
with open('file1.txt', 'w') as f:
    f.write("This is file1")
with open('file2.txt', 'w') as f:
    f.write("This is file2")
with open('subdir/file3.txt', 'w') as f:
    f.write("This is file3 in subdir")

# Создание архива
with tarfile.open('test_archive.tar', 'w') as tar:
    tar.add('file1.txt')
    tar.add('file2.txt')
    tar.add('subdir')
