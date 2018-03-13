from .algorithms import heartrate_models, w_prime_balance
from .algorithms.metrics import core, power
from .base import BaseWorkoutDataFrame
from .helpers import requires


class WorkoutDataFrame(BaseWorkoutDataFrame):
    _metadata = ['athlete']

    @requires(columns=['power'])
    def compute_mean_max_power(self):
        return core.mean_max(self.power)

    @requires(columns=['power'])
    def compute_weighted_average_power(self):
        return core.weighted_average_power(self.power, type='WAP')

    @requires(columns=['power'], athlete=['weight'])
    def compute_power_per_kg(self):
        return power.wpk(self.power, self.athlete.weight)

    @requires(columns=['power'], athlete=['cp', 'w_prime'])
    def compute_w_prime_balance(self, algorithm=None, *args, **kwargs):
        return w_prime_balance.w_prime_balance(self.power, self.athlete.cp,
            self.athlete.w_prime, algorithm, *args, **kwargs)

    @requires(columns=['power'])
    def compute_mean_max_bests(self, duration, number):
        return core.multiple_best_intervals(self.power, duration, number)

    @requires(columns=['power', 'heartrate'])
    def compute_heartrate_model(self):
        return heartrate_models.heartrate_model(self.heartrate, self.power)


class Athlete:
    def __init__(self, name=None, sex=None, weight=None, dob=None, ftp=None,
            cp=None, w_prime=None):
        self.name = name
        self.sex = sex
        self.weight = weight
        self.dob = dob
        self.ftp = ftp
        self.cp = cp
        self.w_prime = w_prime
