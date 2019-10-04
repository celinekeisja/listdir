import os
import argparse
import csv


def directory_files(name, files):
    # Puts the Parent Path, File Name, and File Size of files within the specified directory in a CSV file.
    with open(f'{name}.csv', 'w+', newline='') as csv_file:
        field_n = ['Parent Path', 'File Name', 'File Size']
        writer = csv.DictWriter(csv_file, fieldnames=field_n)
        writer.writeheader()
        for r, d, f in os.walk(directory_name):
            for file in f:
                d = {"Parent Path": r, "File Name": file, "File Size": os.path.getsize(r+"//"+file)}
                writer.writerow(d)
    return f'Created {name}.csv!'


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    parser.add_argument("name")
    parser.add_argument('-d', '--directory_files', action='store_true', help='Stores the name of a directory.')
    args = parser.parse_args()
    if args.directory_files:
        directory_name = args.path
        output_name = args.name
        directory_files(output_name, directory_name)
