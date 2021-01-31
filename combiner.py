import argparse
from pathlib import Path
import os
import time

if __name__ == '__main__':
    parser = argparse.ArgumentParser("Combine password lists")
    parser.add_argument("-d", "--directory", required=True, help="Directory with all password lists to combine")
    parser.add_argument("-o", "--outfile", required=True, help="Output file")

    args = parser.parse_args()

    dir_path = Path(args.directory)
    print(f"Currently processing the {dir_path} directorly...\n")

    start = time.time()
    password_list = []
    for root, dirnames, filenames in os.walk(dir_path.absolute()):
        for files in filenames:
            file_path = Path(root) / files
            # Keeping only .txt
            if file_path.suffix not in [".txt"]:
                print(f"Excluding {file_path} because not a .txt file...")
                continue
            # Removing files "-withcount"
            if "-withcount" in file_path.as_posix():
                print(f"Excluding {file_path} because it's a file with frequencies...")
                continue

            with open(file_path, encoding="utf-8", errors='ignore') as f:
                print(f"Processing {file_path}...")
                data = f.readlines()
                # print(data[0])

            # Files in this folder have a username:pwd strucuture
            if "Default-Credentials" in file_path.as_posix():
                password_list += [line.split(":")[-1] for line in data]

            # Pwd in mirai-botnet.txt have a username pwd structure
            elif "mirai-botnet.txt" in file_path.as_posix():
                password_list += [line.split(" ")[-1] for line in data if "(none)" not in line]

            # Pwd in python-heralding-sep2019 have a pwd,usrname structure
            elif "python-heralding-sep2019.txt" in file_path.as_posix():
                password_list += [line.split(",")[0] for line in data]

            else:
                password_list += data

    end = time.time()
    print(f"\nThe processing of the files is done! ({int(end - start)} seconds)")
    print(f"Number of recovered passwords: {len(password_list)} !")

    print("\nRemoving duplicates...")
    start = time.time()
    unique_passwords = list(set(password_list))
    end = time.time()
    print(f"Finished! ({int(end - start)} seconds)")

    print(f"\nNumber of unique passwords : {len(unique_passwords)} !")

    print("\nSorting passwords...")
    start = time.time()
    unique_passwords.sort()
    end = time.time()
    print(f"Finished! ({int(end - start)} seconds)\n")

    outfile = Path(args.outfile)
    if outfile.is_file():
        print(f"{outfile.as_posix()} already exists...")
        outfile = outfile.parents[0] / (outfile.stem + "_new" + outfile.suffix)
    print(f"Writing result in {outfile.as_posix()}...")
    start = time.time()
    with open(outfile, "w", encoding="utf-8") as f:
        f.writelines(unique_passwords)
    end = time.time()
    print(f"Finished! ({int(end - start)} seconds)")