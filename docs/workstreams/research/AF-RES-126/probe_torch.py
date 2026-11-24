"""Observe the constructed index, shape and storage contrasts on PyTorch 2.5.1 CPU."""

import json

import numpy as np
import torch
from torch.utils.data import BatchSampler, DataLoader, WeightedRandomSampler, default_convert


PIN = "a8d6afb511a69687bbb2b7e88a3cf67917e1697e"


def share(left, right):
    return left.untyped_storage().data_ptr() == right.untyped_storage().data_ptr()


def main():
    assert torch.__version__ == "2.5.1+cpu" and torch.version.git_version == PIN
    draws = list(WeightedRandomSampler([1, 0, 0], 3, replacement=True))
    batches = list(BatchSampler(range(10), batch_size=3, drop_last=False))
    sample_values = [
        batch.tolist()
        for batch in DataLoader(torch.arange(100, 110), batch_size=3, shuffle=False, drop_last=False)
    ]
    assert draws == [0, 0, 0] and batches[-1] == [9] and sample_values[-1] == [109]
    assert [len(batch) for batch in batches] == [len(batch) for batch in sample_values] == [3, 3, 3, 1]

    tensor = torch.arange(24).reshape(2, 3, 4)
    permuted = tensor.permute(2, 0, 1)
    reshaped = tensor.reshape(4, 2, 3)
    one_swap = tensor.transpose(0, 2)
    two_swaps = tensor.transpose(1, 2).transpose(0, 1)
    coordinate = (1, 0, 2)
    permutation_value = int(permuted[coordinate])
    reshape_value = int(reshaped[coordinate])
    assert permutation_value == int(tensor[0, 2, 1]) == 9 and reshape_value == 8
    assert torch.equal(two_swaps, permuted) and share(two_swaps, tensor) and share(permuted, tensor)
    assert one_swap.shape != permuted.shape

    contiguous = torch.arange(25).reshape(5, 5)
    whole_view = contiguous.view(25)
    whole_reshape = contiguous.reshape(25)
    non_contiguous_reshape = contiguous.t().reshape(25)
    assert share(whole_view, contiguous) and share(whole_reshape, contiguous)
    assert not share(non_contiguous_reshape, contiguous)
    whole_view[6] = 100
    assert int(contiguous[1, 1]) == 100

    leaf = torch.arange(6.0, requires_grad=True)
    source = leaf.reshape(2, 3).t()
    copied = source.clone()
    detached = source.detach()
    assert torch.equal(source, copied) and source.stride() == copied.stride() and not share(source, copied)
    assert share(source, detached) and detached.grad_fn is None and not detached.requires_grad
    copied.sum().backward()
    assert leaf.grad.tolist() == [1.0] * 6
    detached[1, 0] = 99
    assert source[1, 0].item() == 99 and copied[1, 0].item() == 1 and leaf.grad.tolist() == [1.0] * 6

    array, label = default_convert((np.array([3, 4]), 7))
    assert array.tolist() == [3, 4] and type(label) is int
    print(json.dumps({
        "torch_version": torch.__version__,
        "torch_git_version": torch.version.git_version,
        "numpy_version": np.__version__,
        "P01_weighted_indices": draws,
        "P02_permute_shape": list(permuted.shape),
        "P02_reshape_vs_permute_coordinate": [reshape_value, permutation_value],
        "P02_two_transposes_same_coordinates_and_storage": True,
        "P04_contiguous_share": {"view": share(whole_view, contiguous), "reshape": share(whole_reshape, contiguous)},
        "P04_noncontiguous_reshape_share": share(non_contiguous_reshape, contiguous),
        "P05_sampler_indices": batches,
        "P05_loader_samples": sample_values,
        "P06_copy_shares_storage": share(source, copied),
        "P06_copy_and_source_stride": [list(copied.stride()), list(source.stride())],
        "P06_copy_backward_to_leaf": leaf.grad.tolist(),
        "P06_detach_shares_storage": share(source, detached),
        "P06_detach_result_has_grad_fn": detached.grad_fn is not None,
        "P06_modified_source_and_copy": [source[1, 0].item(), copied[1, 0].item()],
        "C08_converted": {"values": array.tolist(), "shape": list(array.shape), "label_type": type(label).__name__},
    }, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
