from . import util

def index_of_coincidence(string, alphabet):
    frequencies = map(lambda letter: util.get_frequency(string, letter), alphabet)
    coincidences = sum(f*(f-1) for f in frequencies)
    return coincidences/(len(string)*(len(string)-1))