import ivy
from ivy.func_wrapper import with_supported_dtypes
from ivy.functional.frontends.paddle.func_wrapper import to_ivy_arrays_and_back
import numpy as np

def _broadcast_pooling_helper(x, pool_dims, name):
    if isinstance(x, int):
        return tuple([x for _ in range(pool_dims)])
    if len(x) == 1:
        return tuple([x[0] for _ in range(pool_dims)])
    elif len(x) == pool_dims:
        return tuple(x)
    elif isinstance(x,str):
        return x
    elif len(x) != pool_dims:
        raise ValueError(
            f"`{name}` must either be a single int, or a tuple of {pool_dims} ints. "
        )

@to_ivy_arrays_and_back
@with_supported_dtypes({"2.5.0 and below": ("float32", "float64")}, "paddle")
def Avgpool1d(
    x,
    kernel_size,
    stride=1,
    padding=0,
    ceil_mode=False,
    exclusive=True,
    divisor_override=None,
    data_format="NWC",
    *,
    name=None,
):
    kernel_size = _broadcast_pooling_helper(kernel_size, 1, name="kernel_size")
    stride = _broadcast_pooling_helper(stride, 1, name="stride")
    padding = _broadcast_pooling_helper(padding, 1, name="padding")
    kernel_pads = list(zip(kernel_size, padding))

    # Padding should be less than or equal to half of kernel size
    if(not isinstance(padding,str)):
        if not all([pad <= kernel // 2 for kernel, pad in kernel_pads]):
            raise ValueError(
                "pad should be smaller than or equal to half of kernel size, "
                f"but got padding={padding}, kernel_size={kernel_size}. "
            )
    
    # Figure out padding string
    # if all([pad == ivy.ceil((kernel - 1) / 2) for kernel, pad in kernel_pads]):
    #     pass
    # else:
    #     pass

    return ivy.avg_pool1d(
            x,
            kernel_size,
            stride,
            padding,
            data_format=data_format,
        )