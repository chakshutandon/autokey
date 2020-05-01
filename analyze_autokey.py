import argparse
import os

import wordninja

from crypto import english
from crypto.analysis import autokey
from crypto import transformation

def get_file_contents(filepath):
    with open(filepath, 'r') as f:
        return f.readlines()

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="filepath to ciphertext")
    parser.add_argument("probe", help="probe for plaintext in key")

    args = parser.parse_args()
    assert(os.path.isfile(args.file)), f"File {args.file} not found."

    return args

def main():
    args = parse_args()
    ciphertext = get_file_contents(args.file)[0]

    alphabet = english.ALPHABET

    partial = autokey.decode_autokey_probe_plaintext_key(ciphertext, args.probe, alphabet)
    print(partial)

if __name__ == "__main__":
    main()