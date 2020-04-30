from statistics import mean, stdev

from .. import metrics
from .. import utils

def __get_monogram_frequencies(ciphertext, alphabet):
    func = lambda char: utils.get_frequency(ciphertext, char) / len(ciphertext)
    m = map(func, alphabet)
    return list(m)

def __monogram_frequency_test(ciphertext_frequencies, expected_frequencies):
    z = zip(ciphertext_frequencies, expected_frequencies)
    func = lambda el: (el[1] - el[0]) / el[1]
    m = map(func, z)
    return list(m)

def __get_bigram_frequencies(ciphertext, alphabet):
    dict = {}
    z = zip(ciphertext, ciphertext[1:])
    bigrams = ["".join(el) for el in z]
    func = lambda bigram: utils.get_frequency(ciphertext, bigram) / len(ciphertext)
    m = map(func, bigrams)
    return list(m)

def __bigram_frequency_test(bigram_frequencies, expected_frequencies):
    n = len(expected_frequencies)
    bigram_frequencies = sorted(bigram_frequencies, reverse=True)[:n]

    z = zip(bigram_frequencies, expected_frequencies)
    func = lambda el: (el[1] - el[0]) / el[1]
    m = map(func, z)

    return list(m)

def __ciphertext_contains_letter(ciphertext, letter):
    return letter in ciphertext

def __partition(ciphertext, k):
    return [ciphertext[i::k] for i in range(0, k)]

def __friedman(ciphertext, alphabet, max_key_len):
    res = []
    for k in range(1, max_key_len):
        substrings = __partition(ciphertext, k)
        func = lambda substring: metrics.index_of_coincidence(substring, alphabet)
        m = map(func, substrings)
        ioc = sum(m) / k
        res.append(ioc)
    return res

def permutation_cipher_test(ciphertext, alphabet, expected_frequencies):
    frequencies = __get_monogram_frequencies(ciphertext, alphabet)
    percent_differences = __monogram_frequency_test(frequencies, expected_frequencies)

    mu = mean(percent_differences)
    std = stdev(percent_differences)
    return (mu, std)

def simple_substitution_test(ciphertext, alphabet, expected_IOC):
    IOC = metrics.index_of_coincidence(ciphertext, alphabet)
    percent_difference = (IOC - expected_IOC) / expected_IOC
    return (IOC, percent_difference)

def bigram_cipher_test(ciphertext, alphabet, expected_frequencies):
    bigram_frequencies = __get_bigram_frequencies(ciphertext, alphabet)
    percent_differences = __bigram_frequency_test(bigram_frequencies, expected_frequencies)
    
    mu = mean(percent_differences)
    std = stdev(percent_differences)
    return (mu, std)

def playfair_cipher_test(ciphertext, alphabet):
    return not __ciphertext_contains_letter(ciphertext, 'j')

def friedman_ioc_test(ciphertext, alphabet, max_key_len):
    res = __friedman(ciphertext, alphabet, max_key_len)
    key_len = res.index(max(res)) + 1
    mu = mean(res)
    std = stdev(res)
    return (key_len, mu, std)

