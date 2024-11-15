import sys
import os

if __name__ == '__main__':
    
    n = len(sys.argv)
    if n < 4:
        print(f"Usage python {sys.argv[0]} <input-folder> <output-folder> <input-file>")
        sys.exit()

    input_folder = sys.argv[1]
    output_folder = sys.argv[2]
    input_file = sys.argv[3]

    if not os.path.isdir(input_folder):
        print(f"{input_folder} does not exist")
        sys.exit()

    fname = f"{input_folder}/{input_file}"
    if not os.path.isfile(fname):
        print(f"{fname} file does not exist")
        sys.exit()

    if not os.path.isdir(output_folder):
        os.makedirs(output_folder)

    print("command list check passed, proceed with regular coding")