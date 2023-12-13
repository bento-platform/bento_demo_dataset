from typing import TypeVar
from math import floor
import numpy as np
from scipy.stats import truncnorm, truncexpon
from constants import RANDOM_SEED
T = TypeVar('T')


class RandomGenerator:
    def __init__(self):
        self.rng = np.random.default_rng(seed=RANDOM_SEED)

    # randomly choose between zero and n items from the "elements" list
    # multiplicity_distribution is a list of weights: [P(return zero choices), P(return one choice), P(return 2 choices), etc]
    # length is arbitrary, but weights should sum to one
    # each individual choice is made using a normal distribution
    def choices_with_multiplicity(self, elements: list[T], multiplicity_distribution: list[float]) -> list[T]:
        num_choices = self.biased_die_roll(multiplicity_distribution)
        if num_choices == 0:
            return []
        weights_for_elements = self.normalized_quasi_gaussian_weights(len(elements))
        return self.rng.choice(elements, size=num_choices, replace=False, p=weights_for_elements)

    def gaussian_choice(self, elements: list[T]) -> T:
        return self.rng.choice(elements, p=self.normalized_quasi_gaussian_weights(len(elements)), shuffle=False)

    # biased die with arbitrary size (one side for each weight)
    def biased_die_roll(self, weights: list[float]) -> int:
        return self.rng.choice(range(len(weights)), p=weights, shuffle=False)

    def int_from_truncated_gaussian(self, low: float, hi: float, mean: float, sd: float) -> int:
        return floor(truncnorm.rvs((low-mean)/sd, (hi-mean)/sd, loc=mean, scale=sd, random_state=self.rng))

    # integers drawn from normal distribution between min and max
    def ints_from_truncated_gaussian(self, low: float, hi: float, mean: float, sd: float, size: int) -> list[int]:
        vals = truncnorm.rvs((low-mean)/sd, (hi-mean)/sd, loc=mean, scale=sd, size=size, random_state=self.rng)
        return [floor(val) for val in vals]

    def int_from_truncated_exponential(self, low: float, hi: float, mean: float) -> int:
        return floor(truncexpon.rvs((hi - low)/mean, loc=low, scale=mean, random_state=self.rng))

    def normalized_quasi_gaussian_weights(self, size: int) -> list[float]:
        g = self.rng.normal(size=size)
        g_pos = abs(g)
        g_sum = sum(g_pos)
        return [n / g_sum for n in g_pos]

    # TODO
    # def random_weights(self, controlled_vocabulary):
    # # generate random weights for random distribution of values
    # np_random_weights = np.random.dirichlet(np.ones(len(controlled_vocabulary)), size=1)
    # weights = [round(i, 2) for i in np_random_weights.tolist()[0]]
    # return weights
