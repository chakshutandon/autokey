#!/usr/bin/env python3

import os
import argparse

import wordninja

from crypto import metrics
from crypto import transformation
from crypto import english
    
def get_file_contents(filepath):
    with open(filepath, 'r') as f:
        return f.readlines()

def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("file", help="filepath to ciphertext")
    parser.add_argument("--autokey", action='store_true', help="use autokey method for decryption")
    parser.add_argument("key", type=str, help="key to use for decyption")

    args = parser.parse_args()
    assert(os.path.isfile(args.file)), f"File {args.file} not found."

    return args

def main():
    args = parse_args()

    ciphertext = get_file_contents(args.file)[0]

    key = args.key
    alphabet = english.ALPHABET

    decode_func = transformation.decode_string_with_repeated_key
    encode_func = transformation.encode_string_with_repeated_key

    if args.autokey:
        decode_func = transformation.decode_string_with_plaintext_autokey
        encode_func = transformation.encode_string_with_plaintext_autokey

    pt = decode_func(ciphertext, key, alphabet)
    ct = encode_func(pt, key, alphabet)

    assert(ct == ciphertext)
    assert(len(pt) == len(ciphertext))

    pt = wordninja.split(pt)
    print(" ".join(pt))
    
    return

if __name__ == "__main__":
    main()