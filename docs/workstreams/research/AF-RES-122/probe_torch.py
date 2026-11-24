"""Run bounded positive and negative inputs against the pinned CPU build."""

import json
import platform

import numpy as np
import torch
from torch.utils.data import (
    BatchSampler, DataLoader, TensorDataset, WeightedRandomSampler,
    default_collate, default_convert,
)

PIN = "a8d6afb511a69687bbb2b7e88a3cf67917e1697e"


def raises_runtime(action):
    try:
        action()
    except RuntimeError:
        return True
    return False


def storage(tensor):
    return tensor.untyped_storage().data_ptr()


def sampler_cases():
    grouped = list(BatchSampler(range(10), 3, False))
    dropped = list(BatchSampler(range(10), 3, True))
    data = TensorDataset(torch.arange(10, 20))
    batches = [item[0].tolist() for item in DataLoader(data, batch_sampler=grouped)]
    weighted = list(WeightedRandomSampler([1, 0, 0], 3, True))
    unique = list(WeightedRandomSampler([1, 1, 1], 3, False, torch.Generator().manual_seed(42)))
    assert grouped == [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]]
    assert dropped == grouped[:-1]
    assert batches == [[10, 11, 12], [13, 14, 15], [16, 17, 18], [19]]
    assert weighted == [0, 0, 0] and sorted(unique) == [0, 1, 2]
    return {
        "C01": {"keep_grouped": grouped, "drop_grouped": dropped, "loader_sample_values": batches},
        "C02": {"with_replacement_one_positive": weighted, "without_replacement_three_positive_seed42": unique},
    }


def shape_cases():
    tensor = torch.arange(6).reshape(2, 3)
    view = tensor.view(3, 2)
    reshaped = tensor.reshape(3, 2)
    transposed = tensor.transpose(0, 1)
    permuted = tensor.permute(1, 0)
    assert torch.equal(view, reshaped) and torch.equal(transposed, permuted)
    assert not torch.equal(view, transposed)
    assert all(storage(item) == storage(tensor) for item in (view, reshaped, transposed, permuted))

    grid = torch.ones(5, 5)
    view_25 = grid.view(25)
    same = grid.reshape(25)
    different = grid.t().reshape(25)
    view_25[6] = 0
    compatible = torch.arange(12).reshape(3, 4)[:, ::2]
    compatible_view = compatible.view(6)
    refused = raises_runtime(lambda: grid.t().view(25))
    assert storage(same) == storage(grid) and storage(different) != storage(grid)
    assert grid[1, 1].item() == 0 and different[6].item() == 1
    assert not compatible.is_contiguous() and storage(compatible) == storage(compatible_view)
    assert refused
    return {
        "C03-C09": {"same_shape": list(view.shape), "view_and_reshape": view.tolist(), "transpose_and_permute": transposed.tolist(),
                    "all_share_storage": True},
        "C04": {"grid_write_reaches_source": grid[1, 1].item(), "copy_from_transposed_before_write": different[6].item(),
                "compatible_noncontiguous_stride": list(compatible.stride()), "compatible_view": compatible_view.tolist(),
                "incompatible_view_raises": refused},
    }


def copy_cases():
    original = torch.ones(2, requires_grad=True)
    copied = original.clone()
    detached = original.detach()
    detached_copy = original.detach().clone()
    copied.sum().backward()
    assert original.grad.tolist() == [1, 1] and original.requires_grad
    assert storage(copied) != storage(original) and copied.requires_grad
    assert storage(detached) == storage(original) and not detached.requires_grad
    with torch.no_grad():
        detached[0] = 9
    assert original.tolist() == [9, 1] and copied.tolist() == [1, 1]
    assert detached_copy.tolist() == [1, 1] and not detached_copy.requires_grad

    source = torch.ones(5, 1)
    expanded = source.expand(5, 5)
    repeated = source.repeat(1, 5)
    initially_equal = torch.equal(expanded, repeated)
    assert initially_equal
    overlap_refused = raises_runtime(lambda: expanded.add_(1))
    expanded[2, 2] = 0
    repeated[2, 2] = 7
    assert expanded[2].tolist() == [0, 0, 0, 0, 0]
    assert repeated[2].tolist() == [1, 1, 7, 1, 1] and source[2, 0].item() == 0
    assert storage(expanded) == storage(source) and storage(repeated) != storage(source)
    assert overlap_refused
    return {
        "C05-C06": {"gradient_from_clone": original.grad.tolist(), "after_detached_write_original": original.tolist(),
                    "clone": copied.tolist(), "detach_then_clone": detached_copy.tolist(), "detach_shares_storage": True},
        "C07": {"initially_equal": initially_equal, "expand_stride": list(expanded.stride()),
                "expanded_row": expanded[2].tolist(), "repeated_row": repeated[2].tolist(), "overlap_refused": overlap_refused},
    }


def conversion_case():
    sample = {"x": np.array([2, 3]), "label": 7}
    converted = default_convert(sample)
    as_batch = default_collate([sample])
    assert converted["x"].tolist() == [2, 3] and isinstance(converted["label"], int)
    assert as_batch["x"].tolist() == [[2, 3]] and as_batch["label"].tolist() == [7]
    return {"C08": {"converted_shape": list(converted["x"].shape), "converted_label_type": type(converted["label"]).__name__,
                    "batch_shape": list(as_batch["x"].shape), "batch_label_shape": list(as_batch["label"].shape)}}


def consumer_cases():
    # Reconstructed shapes only. No author model weights or pasted code is executed.
    model = torch.nn.LSTM(6, 4)
    tensor = torch.zeros(28, 32, 6)
    _, (wrong, _) = model(tensor)
    expected, (correct, _) = model(tensor.transpose(0, 1))
    assert list(wrong.shape) == [1, 32, 4] and list(correct.shape) == [1, 28, 4]
    assert list(expected.shape) == [32, 28, 4]
    emb = torch.nn.Embedding(5, 2)
    same = emb(torch.zeros(2, 3, 1, dtype=torch.long))
    many = emb(torch.zeros(2, 3, 4, dtype=torch.long))
    assert list(same.reshape(2, 3, 2).shape) == [2, 3, 2]
    assert raises_runtime(lambda: many.reshape(2, 3, 2))
    return {"O3143-derived": {"default_h": list(wrong.shape), "axis_swap_h": list(correct.shape)},
            "O3665-derived": {"singleton": list(same.shape), "multi_feature": list(many.shape),
                              "multi_feature_reshape_raises": True}}


def main():
    assert torch.version.git_version == PIN
    torch.manual_seed(122)
    torch.set_num_threads(1)
    result = {
        "actor": "Codex Cloud / bounded PyTorch CPU calls",
        "torch": torch.__version__,
        "torch_git_version": torch.version.git_version,
        "python": platform.python_version(),
        "os": platform.system(),
        "arch": platform.machine(),
        "numpy": np.__version__,
    }
    for run in (sampler_cases, shape_cases, copy_cases, conversion_case, consumer_cases):
        result.update(run())
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
