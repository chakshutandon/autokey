import warnings

from . import util

def rotate_char(char, n, alphabet, forward=True):
    # Rotate a character char by n in the given alphabet
    if (not forward): n *= -1
    idx = util.get_idx(char, alphabet)
    new_idx = util.rotate_idx(idx, n, alphabet)
    return util.get_chr(new_idx, alphabet)

def rotate_string_const(string, n, alphabet, forward=True):
    # Rotate a string forward by n in the given alphabet
    if (not forward): n *= -1
    func = lambda char: rotate_char(char, n, alphabet)
    m = map(func, string)
    return "".join(m)

def __rotate_string_with_key(string, key, alphabet, forward=True):
    # Rotate a string by key in the given alphabet
    key_idxs = util.string_to_idxs(key, alphabet)[:len(string)]
    func = lambda i, n: rotate_char(string[i], n, alphabet, forward)
    m = [func(i,n) for (i,n) in enumerate(key_idxs)]
    return "".join(m)

def rotate_string_with_key(string, key, alphabet, forward=True, repeat=False):
    # Rotate a string by key in the given alphabet
    while (repeat and (len(key) < len(string))):
        key += key
    if len(key) < len(string):
        f_n = "rotate_string_with_key(string, key, alphabet, repeat)"
        err = "key length is shorter than the string length. Output may be truncated."
        warnings.warn(f"{f_n}: {err}")
    return __rotate_string_with_key(string, key, alphabet, forward)
    
def encode_string_with_repeated_key(plaintext, key, alphabet):
    # Encode plaintext with a key repeated for the length of the plaintext
    return rotate_string_with_key(plaintext, key, alphabet, forward=True, repeat=True)

def decode_string_with_repeated_key(ciphertext, key, alphabet):
    # Decode ciphertext with a key repeated for the length of the ciphertext
    return rotate_string_with_key(ciphertext, key, alphabet, forward=False, repeat=True)

def encode_string_with_plaintext_autokey(plaintext, key, alphabet):
    # Encode plaintext with an autokey
    key += plaintext
    return rotate_string_with_key(plaintext, key, alphabet, forward=True, repeat=False)

def decode_string_with_plaintext_autokey(ciphertext, key, alphabet):
    # Decode ciphertext with an autokey
    plaintext = ""
    while (len(plaintext) < len(ciphertext)):
        _key = key + plaintext
        plaintext = __rotate_string_with_key(ciphertext, _key, alphabet, forward=False)
    return plaintext