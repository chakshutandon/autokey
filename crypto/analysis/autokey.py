import itertools

import math

from .. import transformation
from .. import metrics

def ngrams(input, n):
    output = []
    for i in range(len(input)-n+1):
        output.append(input[i:i+n])
    return output

class NGrams(object):
    # Load and parse ngrams list
    # File format should be
    # aard 5
    # etc
    def __init__(self, filename):
        self.ngrams = {}

        for line in open(filename):
            char, count = line.split(" ")
            char = char.lower()
            self.ngrams[char] = int(count)

        # The n in ngram
        self.L = len(char)
        # Total number of occurences
        self.N = sum(self.ngrams.values())

        # Turn count into a probability, then log it. Done to avoid rounding
        # errors with small floating point numbers.
        for char in self.ngrams.keys():
            self.ngrams[char] = math.log10(float(self.ngrams[char])/self.N)

        # Don't want prob to be -infty
        self.floor = math.log10(0.01/self.N)

    # Score a given text by comparing it's ngrams
    def score(self, text):
        score = 0
        for i in range(len(text)-self.L+1):
            # For each segment of the same length as the ngrams
            # Add it's probability if it's in the list of ngrams
            # Otherwise add the lowest prob
            if text[i:i+self.L] in self.ngrams:
                score += self.ngrams[text[i:i+self.L]]
            else: score += self.floor
        return score

def decode_autokey_bruteforce(ciphertext, alphabet, key_length):
    best_key = alphabet[0] * key_length
    for i in range(key_length):
        curr_key = best_key
        best_char = alphabet[0]
        max_IOC = 0
        for char in alphabet:
            curr_key = best_key[:i] + char + best_key[i+1:]
            plaintext = transformation.decode_string_with_plaintext_autokey(ciphertext, curr_key, alphabet)
            IOC = metrics.index_of_coincidence(plaintext, alphabet)
            if IOC <= max_IOC:
                continue
            best_char = char
            max_IOC = IOC
        best_key = best_key[:i] + best_char + best_key[i+1:]
    return best_key
        
def decode_autokey_probe_plaintext_key(ciphertext, probe, alphabet):
    quadgrams = NGrams("./crypto/analysis/english_quadgrams.txt")
    n = len(probe)
    partitions = ngrams(ciphertext, n)

    max_score = -1000
    best_partial = ""
    for partition in partitions:
        partial = transformation.rotate_string_with_key(partition, probe, alphabet, forward=False)
        score = quadgrams.score(partial)   
        if score <= max_score:
            continue
        best_partial = partial
        max_score = score
    
    return best_partial
