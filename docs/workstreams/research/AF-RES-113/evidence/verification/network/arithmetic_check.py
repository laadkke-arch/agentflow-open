"""Two constructed arithmetic counterexamples; no target library or paper experiment."""
import datetime
import json
import platform

import numpy as np


def main():
    x = np.array([0.0, 0.0, 0.0, 1.0])
    h = np.array([1.0, 1.0])
    circular = np.fft.ifft(np.fft.fft(x, 4) * np.fft.fft(h, 4)).real
    linear = np.convolve(x, h)
    assert np.allclose(circular, [1, 0, 0, 1])
    assert np.allclose(linear, [0, 0, 0, 1, 1])
    t_irregular = np.array([0.0, 1.0, 3.0, 4.0])
    t_assumed = np.arange(4, dtype=float)
    correct = np.cos(2 * np.pi * 0.25 * t_irregular)
    assumed = np.cos(2 * np.pi * 0.25 * t_assumed)
    assert np.allclose(correct, [1, 0, 0, 1], atol=1e-12)
    assert np.allclose(assumed, [1, 0, -1, 0], atol=1e-12)
    print(json.dumps({
        "checked_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "python": platform.python_version(),
        "numpy": np.__version__,
        "scope": "constructed arithmetic only; not librosa/skimage/SNF execution or author-example reproduction",
        "tests": [
            {"test_id": "NET-TEST-CIRCULAR", "x": x.tolist(), "h": h.tolist(),
             "circular_fft_length": 4, "circular_output": circular.tolist(),
             "linear_output": linear.tolist(), "result": "pass"},
            {"test_id": "NET-TEST-IRREGULAR", "frequency_hz": 0.25,
             "actual_times_seconds": t_irregular.tolist(),
             "assumed_times_seconds": t_assumed.tolist(),
             "actual_grid_model": correct.tolist(), "assumed_grid_model": assumed.tolist(),
             "result": "pass"},
        ],
    }, indent=2))


if __name__ == "__main__":
    main()
