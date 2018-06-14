# -*- coding: utf-8 -*-

import numpy as np

from .numba_utils import use_numba
if use_numba:
    from numba import jit
else:
    from .numba_utils import jit

from .data_utils import one_hot

#-----------------------------------------------------------------------------#
#                     GENERATE SYNTHETIC SEQUENCES DATA                       #
#-----------------------------------------------------------------------------#

@jit(nogil = True, cache = True)
def gen_mult_sequence_xtyt(nums, cols = 10, factor = 10, tensor_dtype = np.int):
    assert factor >= cols, 'factor should be more than or equal to cols'
    lookup = cols * factor

    x = np.zeros([nums, cols, lookup], dtype = tensor_dtype)
    y = np.zeros([nums, cols, lookup], dtype = tensor_dtype)

    for i in range(nums):
        start = np.random.randint(1, cols)
        seq   = np.arange(start, (start*cols)+1, start)
        x[i]  = one_hot(seq, lookup)
        y[i]  = np.roll(x[i], -1, axis=0)

    y[:, -1, 1] = 1

    return x, y, lookup

@jit(nogil = True, cache = True)
def gen_mult_sequence_xtym(nums, cols = 10, factor = 10, tensor_dtype = np.int):
    assert factor >= cols, 'factor should be more than or equal to cols'
    lookup = cols * factor
    cols_p = cols - 1

    x   = np.zeros([nums, cols, lookup], dtype = tensor_dtype)
    x_p = np.zeros([nums, cols_p, lookup], dtype = tensor_dtype)
    y   = np.zeros([nums, lookup], dtype = np.int)

    for i in range(nums):
        start  = np.random.randint(1, cols)
        seq    = np.arange(start, (start*cols)+1, start)
        x[i]   = one_hot(seq, lookup)
        x_p[i] = x[i,:-1,:]
        y[i]   = x[i,cols_p,:]

    return x_p, y, lookup
