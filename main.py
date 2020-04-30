import argparse
import os

from crypto import english
from crypto.analysis import cipher_id_tests

def get_file_contents(filepath):
    with open(filepath, 'r') as f:
        return f.readlines()

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="filepath to ciphertext")
    parser.add_argument("--max-key-length", type=int, default=20, help="maximum length of key")

    args = parser.parse_args()
    assert(os.path.isfile(args.file)), f"File {args.file} not found."

    return args

def main():
    args = parse_args()
    ciphertext = get_file_contents(args.file)[0]

    MAX_KEY_LEN = args.max_key_length

    alphabet = english.ALPHABET
    expected_frequencies = english.LETTER_FREQUENCIES
    expected_bigram_frequencies = english.BIGRAM_FREQUENCIES
    expected_IOC = english.INDEX_OF_COINCIDENCE

    print("---------------------------------- Permutation Cipher Test ---------------------------------")
    print()
    print(cipher_id_tests.permutation_cipher_test(ciphertext, alphabet, expected_frequencies))
    print()
    print("------------------------------ Simple Substitution Cipher Test -----------------------------")
    print()
    print(cipher_id_tests.simple_substitution_test(ciphertext, alphabet, expected_IOC))
    print()
    print("------------------------------------ Bigram Cipher Test ------------------------------------")
    print()
    print(cipher_id_tests.bigram_cipher_test(ciphertext, alphabet, expected_bigram_frequencies))
    print()
    print("----------------------------------- Playfair Cipher Test -----------------------------------")
    print()
    print(cipher_id_tests.playfair_cipher_test(ciphertext, alphabet))
    print()
    print("------------------------------------- Friedman IOC Test ------------------------------------")
    print()
    print(cipher_id_tests.friedman_ioc_test(ciphertext, alphabet, MAX_KEY_LEN))
    print()
    print("--------------------------------------------------------------------------------------------")

if __name__ == "__main__":
    main()
