# -*- coding: utf-8 -*-

import numpy as np

from .numba_utils import use_numba
if use_numba:
    from numba import jit
else:
    from .numba_utils import jit

@jit(nogil = True, cache = True)
def unroll_inputs(padded_inputs,
                                 batch_num,
                                 filter_num,
                                 output_height,
                                 output_width,
                                 kernel_size):

    unrolled_inputs = np.zeros((batch_num,
                                           filter_num,
                                           output_height * output_width,
                                           kernel_size**2))

    offset = 0
    for h in np.arange(output_height): # output height
        for w in np.arange(output_width): # output width
            for b in np.arange(batch_num): # batch number
                for f in np.arange(filter_num): # filter number
                     unrolled_inputs[b, f, offset, :] = padded_inputs[b,
                                                                      f,
                                                                      h:h+kernel_size,
                                                                      w:w+kernel_size].flatten()
            offset += 1

    return unrolled_inputs.reshape(filter_num * kernel_size**2, -1)
