import random
import numpy as np


def random_weights(controlled_vocabulary):
    # generate random weights for random distribution of values
    np_random_weights = np.random.dirichlet(np.ones(len(controlled_vocabulary)), size=1)
    weights = [round(i, 2) for i in np_random_weights.tolist()[0]]
    return weights


def generic_random_choices(controlled_vocabulary):
    return random.choices(controlled_vocabulary, random_weights(controlled_vocabulary), k=1)[0]

def random_skewed_gen(max):
    v = np.random.noncentral_chisquare(3, 0.1, 10000)
    scale = max / v.max()
    v = v * scale
    for val in v:
        if max and val > max:
            continue
        yield val
