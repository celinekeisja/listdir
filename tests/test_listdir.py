from listdir import listdir
from datetime import datetime
import os

test_filename = 'test_file'


def test_datetime():
    assert listdir.datetime_filename(test_filename) == f'{test_filename}_{datetime.now().strftime("%Y%m%d_%H%M%S")}'


def test_md5():
    assert listdir.hash_file(r"C:\Users\TEU_USER\PycharmProjects\listdir\tests\test.txt", 'md5') =='69fa9f283f8e6fc0bac9faa5e23bf1fd'


def test_sha1():
    assert listdir.hash_file(r"C:\Users\TEU_USER\PycharmProjects\listdir\tests\test.txt",
                             'sha1') == '27d1a529469ce7cfca656744461aaf3679015953'


def test_dir():
    assert listdir.directory_files(test_filename, r'C:\Users\TEU_USER\PycharmProjects\listdir\tests\test.txt') == 'test_file.csv'
    assert os.path.isfile(r'C:\Users\TEU_USER\PycharmProjects\listdir\tests\test_file.csv')