import uuid
from datetime import datetime
from typing import TypeVar, Literal
from math import floor
import numpy as np
from scipy.stats import truncnorm, truncexpon
from constants import RANDOM_SEED
T = TypeVar('T')


class RandomGenerator():
    def __init__(self):
        self.rng = np.random.default_rng(seed=RANDOM_SEED)

    def zero_or_more_choices(self, elements: list[T], mass_distribution: list[float]) -> list[T]:
        """
        Randomly choose between zero and n items from the "elements" list
        mass_distribution is a list of weights: [P(return zero choices), P(return one choice), P(return 2 choices), etc]
        length is arbitrary, but weights should sum to one
        each individual choice is made using a normal distribution
        """
        num_choices = self.biased_die_roll(mass_distribution)
        if num_choices == 0:
            return []
        weights_for_elements = self.gaussian_weights(len(elements))
        return list(self.rng.choice(elements, size=num_choices, replace=False, p=weights_for_elements))

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

    def biased_coin_toss(self, p_win_toss: float) -> Literal[0, 1]:
        return self.biased_die_roll([1-p_win_toss, p_win_toss])

    def float_from_gaussian_range(self, low: float, high: float, mean: float, sd: float) -> float:
        return float(truncnorm.rvs((low-mean)/sd, (high-mean)/sd, loc=mean, scale=sd, random_state=self.rng))

    def int_from_gaussian_range(self, low: float, high: float, mean: float, sd: float) -> int:
        return floor(self.float_from_gaussian_range(low, high, mean, sd))

    def float_from_exponential_range(self, low: float, high: float, mean: float) -> float:
        return float(truncexpon.rvs((high - low)/mean, loc=low, scale=mean, random_state=self.rng))

    def int_from_exponential_range(self, low: float, high: float, mean: float) -> int:
        return floor(self.float_from_exponential_range(low, high, mean))

    def int_from_uniform_range(self, low: float, high: float) -> int:
        return int(self.rng.integers(low, high))

    def random_uuid4(self) -> str:
        return str(uuid.UUID(bytes=self.rng.bytes(16), version=4))
    
    def random_recent_date(self) -> str:
        year = f"202{self.int_from_exponential_range(low=0, high=4, mean=3)}"
        d = self.int_from_gaussian_range(low=1, high=366, mean=366/2, sd=366/6)
        month_day = datetime.strptime(f"{d}", "%j").strftime("%m-%d")
        return year + "-" + month_day

    def gaussian_weights(self, size: int) -> list[np.float64]:
        """
        weights for choice methods
        These are only quasi-gaussian since we take the absolute value and normalize so they sum to one
        """
        g = self.rng.normal(size=size)
        g_pos = abs(g)
        g_sum = sum(g_pos)
        return [n / g_sum for n in g_pos]
