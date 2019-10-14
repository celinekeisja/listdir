import os
import argparse
import csv
import hashlib
import zipfile


def hash_file(file, algorithm):
    ''' Hashes the file using MD5 or SHA1 algorithm. '''
    if algorithm == 'md5':
        hasher = hashlib.md5()
    elif algorithm == 'sha1':
        hasher = hashlib.sha1()
    blocksize = 65536
    with open(file, 'rb') as f:
        buf = f.read(blocksize)
        while len(buf) > 0:
            hasher.update(buf)
            buf = f.read(blocksize)

    return hasher.hexdigest()


def zip_file(name):
    ''' Zips the file under the user-defined name. '''
    with zipfile.ZipFile(f"{name}.zip", 'w') as file:
        file.write(name)


def directory_files(name, files):
    ''' Puts the Parent Path, File Name, File Size, Hash in MD5, and Hash in SHA1 of files within the specified directory in a CSV file and zips it. '''
    with open(f'{name}.csv', 'w+', newline='') as csv_file:
        field_n = ['Parent Path', 'File Name', 'File Size', 'MD5', 'SHA1']
        writer = csv.DictWriter(csv_file, fieldnames=field_n)
        writer.writeheader()
        for r, d, f in os.walk(files):
            for file in f:
                size = os.path.getsize(r+"//"+file)
                d = {"Parent Path": r, "File Name": file, "File Size": size,
                     "MD5": hash_file(f"{r}/{file}", 'md5'), "SHA1": hash_file(f"{r}/{file}", 'sha1')}
                writer.writerow(d)
    zip_file(f'{name}.csv')
    return f'Created {name}.csv!'


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    parser.add_argument("name")
    args = parser.parse_args()
    directory_name = args.path
    output_name = args.name
    directory_files(output_name, directory_name)
