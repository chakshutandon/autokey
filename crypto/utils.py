def get_frequency(string, sequence):
    # Get the frequency of sequence in string
    return string.count(sequence)

def get_chr(idx, alphabet):
    # Get the character coresponding to the idx position in the given alphabet
    assert(idx >= 0)
    assert(idx < len(alphabet))
    return alphabet[idx]

def get_idx(char, alphabet):
    # Get the position of char in the given alphabet
    assert(char in alphabet), f"'{char}' not in alphabet '{alphabet}'."
    return alphabet.index(char)

def rotate_idx(idx, n, alphabet):
    # Rotate an index by n in the given alphabet
    return (idx + n) % len(alphabet)

def string_to_idxs(string, alphabet):
    # Convert a string of characters to list of positions in the given alphabet
    func = lambda char: get_idx(char, alphabet)
    m = map(func, string)
    return list(m)

def idxs_to_string(idxs, alphabet):
    # Convert a list of positions to a string in the given alphabet
    func = lambda idx: get_chr(idx, alphabet)
    string = map(func, idxs)
    return "".join(string)
