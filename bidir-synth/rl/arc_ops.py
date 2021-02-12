from rl.operations import Op, ForwardOp, InverseOp, CondInverseOp, ConstantOp
from typing import Callable, List, Tuple, Dict

import bidir.primitives.functions as F
import bidir.primitives.inverse_functions as F2
from bidir.primitives.types import Color


def tuple_return(f: Callable):
    '''
    Inverse functions should take in the output and return a tuple of input
    arguments.
    This function is useful if the inverse function is already implemented as a
    forward function, and we simply want it to return a tuple with a single
    element instead of a single value.
    For example, the proper inverse of rotate_cw is tuple_return(rotate_ccw).
    '''
    return lambda x: (f(x), )


FUNCTIONS: List[Callable] = [
    F.get_color,
    F.hstack_pair,
    F.hflip,
    F.vflip,
    F.vstack_pair,
    F.rotate_cw,
    F.rotate_ccw,
    F.rows,
    F.columns,
    F.hstack,
    F.vstack,
    F.block,
    F.set_bg,
    F.unset_bg,
    F.crop,
    F.kronecker,
    F.top_half,
]

FORWARD_OPS = [ForwardOp(fn) for fn in FUNCTIONS]

COLOR_OPS = [ConstantOp(c) for c in Color]
BOOL_OPS = [ConstantOp(b) for b in [True, False]]
MAX_INT = 3
INT_OPS = [ConstantOp(i) for i in range(MAX_INT + 1)]
CONSTANT_OPS = COLOR_OPS + BOOL_OPS + INT_OPS

# TODO: Should we move these defs into bidir.primitives.functions?
"""
Note that every invertible function has two InverseOps associated with it
So if you want to apply rotate_cw, you'll call the first InverseOp we have below
If you want to apply rotate_ccw, you'll call the second InverseOp we have below
"""
_FUNCTION_INV_PAIRS: List[Tuple[Callable, Callable]] = [
    (F.rotate_ccw, tuple_return(F.rotate_cw)),
    (F.rotate_cw, tuple_return(F.rotate_ccw)),
    (F.vflip, tuple_return(F.vflip)),
    (F.hflip, tuple_return(F.hflip)),
    (F.rows, tuple_return(F.vstack)),
    (F.columns, tuple_return(F.hstack)),
    (F.block, F2.block_inv),
]

INV_OPS = [
    InverseOp(fn, inverse_fn) for (fn, inverse_fn) in _FUNCTION_INV_PAIRS
]

_FUNCTION_COND_INV_PAIRS: List[Tuple[Callable, Callable, List[bool]]] = [
    (F.vstack_pair, F2.vstack_pair_cond_inv_top, [True, False]),
    (F.vstack_pair, F2.vstack_pair_cond_inv_bottom, [False, True]),
    (F.hstack_pair, F2.hstack_pair_cond_inv_left, [True, False]),
    (F.hstack_pair, F2.hstack_pair_cond_inv_right, [False, True]),
    #(F.inflate, F2.inflate_cond_inv),
]

COND_INV_OPS = [
    CondInverseOp(fn, inverse_fn, expects_cond)
    for (fn, inverse_fn, expects_cond) in _FUNCTION_COND_INV_PAIRS
]

ALL_OPS = FORWARD_OPS + CONSTANT_OPS + INV_OPS + COND_INV_OPS  # type: ignore

duplicates = [op for op in ALL_OPS if sum(op == i for i in ALL_OPS) > 1]
if not len(set(op.name for op in ALL_OPS)) == len(ALL_OPS):
    duplicates = [
        op for op in ALL_OPS if sum(op.name == i.name for i in ALL_OPS) > 1
    ]
    assert False, f"duplicate op names: {duplicates}"

OP_DICT: Dict[str, Op] = {op.name: op for op in ALL_OPS}

if __name__ == '__main__':
    print(OP_DICT)
    # print(OP_DICT['3'].fn)
