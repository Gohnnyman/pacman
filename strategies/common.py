import random
import resource
import typing as t
from functools import wraps

from strategies import Strategy


def format(position, target, ghost=None):
    state = {
        'pacman': position,
        'target': target
    }

    if ghost is not None:
        state['ghosts'] = [ghost]

    return state


def gen_path(path, target):
    for position in path:
        yield format(position, target)
    yield None


def find_free_place(labyrinth) -> t.Tuple[int, int]:
    return random.choice(list(labyrinth.cells))


def measured(func):
    @wraps(func)
    def wrapper(self: Strategy, *args, **kwargs):
        before = resource.getrusage(resource.RUSAGE_SELF)
        res = func(self, *args, **kwargs)
        after = resource.getrusage(resource.RUSAGE_SELF)
        self.benchmarking.update({
            'cpu_user': max(self.benchmarking['cpu_user'], after.ru_utime - before.ru_utime),
            'cpu_system': max(self.benchmarking['cpu_user'], after.ru_stime - before.ru_stime),
            'memory': max(self.benchmarking['memory'], after.ru_maxrss - before.ru_maxrss),
        })
        return res
    return wrapper