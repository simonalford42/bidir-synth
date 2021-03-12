import json
from functools import lru_cache
from typing import Dict, Tuple, Any, NamedTuple, List

import numpy as np

from bidir.primitives.types import Grid


class Task(NamedTuple):
    # list of values, each of which is tuple of examples
    inputs: Tuple[Tuple[Any, ...], ...]
    # list of examples
    target: Tuple[Any, ...]


def twenty_four_task(inputs: Tuple[int, ...], target: int) -> Task:
    return Task(tuple((i, ) for i in inputs), (target, ))


@lru_cache(maxsize=None)
def arc_task(task_num: int, train: bool = True) -> Task:
    train_exs, test_exs = get_arc_task_examples(task_num, train)
    input_exs, output_exs = zip(*train_exs)
    return Task((input_exs, ), output_exs)


@lru_cache(maxsize=None)
def get_arc_task_examples(
    task_num: int,
    train: bool = True,
) -> Tuple[Tuple[Tuple[Grid, Grid], ...], Tuple[Tuple[Grid, Grid], ...]]:
    """
    Returns a tuple (training_examples, test_examples), each of which is a
    tuple of examples, each example of which is a (Grid , Grid) tuple.

    train=False gives eval pairs
    """

    if train:
        task_path = "data/ARC/data/training/"
    else:
        task_path = "data/ARC/data/evaluation/"

    task_id = num_to_id(task_num, train=train)
    task_dict = load_task(task_id, task_path)

    train_examples = tuple(
        (Grid(x["input"]), Grid(x["output"])) for x in task_dict["train"])
    test_examples = tuple(
        (Grid(x["input"]), Grid(x["output"])) for x in task_dict["test"])

    return train_examples, test_examples


@lru_cache(maxsize=None)
def get_arc_grids() -> List[Grid]:
    """
    List of all grids used as inputs for a training or eval task.
    """
    grids = []
    for i in range(400):
        train_exs, test_exs = get_arc_task_examples(i, train=True)
        eval_train_exs, eval_test_exs = get_arc_task_examples(i, train=False)
        for (inp,
             outp) in train_exs + test_exs + eval_train_exs + eval_test_exs:
            grids.append(inp)
            # grids.append(outp)

    return grids


def num_to_id(task_num: int, train: bool = True) -> str:
    if train:
        id_path = 'data/ARC/task_number_ids.txt'
    else:
        id_path = 'data/ARC/eval_task_number_ids.txt'

    with open(id_path, 'r') as f:
        lines = [line.rstrip() for line in f]

    d = {
        int(line.split(' ')[0]): line.split(' ')[-1].rstrip(".json")
        for line in lines
    }
    return d[task_num]


def load_task(
    task_id: str,
    task_path: str = 'data/ARC/data/training/',
) -> Dict:
    filename = task_path + task_id + '.json'

    with open(filename, 'r') as f:
        task_dict = json.load(f)

    task_dict['name'] = task_id

    # turn to np arrays
    train = task_dict["train"]
    for ex in train:
        for key in ex:
            ex[key] = np.array(ex[key])

    test = task_dict["test"]
    for ex in test:
        for key in ex:
            ex[key] = np.array(ex[key])

    return task_dict
