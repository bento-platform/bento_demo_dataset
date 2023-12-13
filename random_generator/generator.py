from typing import TypeVar
from math import floor
import numpy as np
from scipy.stats import truncnorm, truncexpon
from constants import RANDOM_SEED
T = TypeVar('T')


class RandomGenerator():
    def __init__(self):
        self.rng = np.random.default_rng(seed=RANDOM_SEED)

    def choices_with_multiplicity(self, elements: list[T], multiplicity_distribution: list[float]) -> list[T]:
        """
        Randomly choose between zero and n items from the "elements" list
        multiplicity_distribution is a list of weights: [P(return zero choices), P(return one choice), P(return 2 choices), etc]
        length is arbitrary, but weights should sum to one
        each individual choice is made using a normal distribution
        """
        num_choices = self.biased_die_roll(multiplicity_distribution)
        if num_choices == 0:
            return []
        weights_for_elements = self.gaussian_weights(len(elements))
        return self.rng.choice(elements, size=num_choices, replace=False, p=weights_for_elements)

    def gaussian_choice(self, elements: list[T]) -> T:
        """
        Choose one element from "elements" using randomly assigned gaussian weights
        """
        return self.rng.choice(elements, p=self.gaussian_weights(len(elements)), shuffle=False)

    def biased_die_roll(self, weights: list[float]) -> int:
        """
        biased integer die roll of arbitrary size (one side for each weight)
        """
        return self.rng.choice(len(weights), p=weights, shuffle=False)

    def float_from_gaussian_range(self, low: float, high: float, mean: float, sd: float) -> float:
        return truncnorm.rvs((low-mean)/sd, (high-mean)/sd, loc=mean, scale=sd, random_state=self.rng) 

    def int_from_gaussian_range(self, low: float, high: float, mean: float, sd: float) -> int:
        return floor(self.float_from_gaussian_range(low, high, mean, sd))

    def float_from_exponential_range(self, low: float, high: float, mean: float) -> float:
        return truncexpon.rvs((high - low)/mean, loc=low, scale=mean, random_state=self.rng)

    def int_from_exponential_range(self, low: float, high: float, mean: float) -> int:
        return floor(self.float_from_exponential_range(low, high, mean))

    def gaussian_weights(self, size: int) -> list[float]:
        """
        weights for choice methods
        These are only quasi-gaussian since we take the absoute value and normalize so they sum to one
        """
        g = self.rng.normal(size=size)
        g_pos = abs(g)
        g_sum = sum(g_pos)
        return [n / g_sum for n in g_pos]
    
    def random_bytes(self, n: int) -> bytes:
        return self.rng.bytes(n)

    # TODO
    # def random_weights(self, controlled_vocabulary):
    # # generate random weights for random distribution of values
    # np_random_weights = np.random.dirichlet(np.ones(len(controlled_vocabulary)), size=1)
    # weights = [round(i, 2) for i in np_random_weights.tolist()[0]]
    # return weights
