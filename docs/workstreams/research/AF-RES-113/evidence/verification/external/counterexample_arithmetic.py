"""Constructed arithmetic checks only; no librosa/skimage/GDAL/audio execution."""
import datetime
import json
import math
from pathlib import Path


def checks():
    impulse_response = [0, 0, 0, 0, 1]
    circular = [0] * 4
    for index, value in enumerate(impulse_response):
        circular[index % 4] += value
    timestamps = [0.0, 0.001, 0.003]
    uniform = [i / 1000 for i in range(3)]
    frequency = 125.0
    true_samples = [math.sin(2 * math.pi * frequency * t) for t in timestamps]
    presumed_samples = [math.sin(2 * math.pi * frequency * t) for t in uniform]
    correct_corner = [100 - 0.5 * 10, 200 - 0.5 * -10]
    wrong_center = [100 + 0.5 * 10, 200 + 0.5 * -10]
    short_separation = math.log(2) / math.log(1000)
    long_separation = 5 * math.log(2) / math.log(1000)
    assert circular == [1, 0, 0, 0]
    assert impulse_response[:4] == [0, 0, 0, 0]
    assert abs(true_samples[2] - math.sqrt(0.5)) < 1e-12
    assert abs(presumed_samples[2] - 1.0) < 1e-12
    assert correct_corner == [95.0, 205.0]
    assert wrong_center == [105.0, 195.0]
    assert short_separation < 0.2 < long_separation
    return {
        "checked_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "scope": "constructed arithmetic only; original experiments and target libraries not run",
        "EXT-T1": {"response": impulse_response, "period": 4, "folded": circular,
                   "linear_first_four": impulse_response[:4]},
        "EXT-T2": {"actual_times_seconds": timestamps, "assumed_times_seconds": uniform,
                   "frequency_Hz": frequency, "actual_time_samples": true_samples,
                   "assumed_time_samples": presumed_samples,
                   "third_sample_phase_error_degrees": 360 * frequency * (timestamps[2] - uniform[2])},
        "EXT-T3": {"point_tiepoint": [100, 200], "signed_spacing": [10, -10],
                   "correct_corner": correct_corner, "wrong_center_if_tiepoint_treated_as_corner": wrong_center},
        "EXT-T6": {"frequency_ratio": 1000, "harmonic_order": 2, "response_support_seconds": 0.2,
                   "T1_separation_seconds": short_separation, "T5_separation_seconds": long_separation},
        "assertions_passed": 7,
    }


if __name__ == "__main__":
    result = checks()
    target = Path(__file__).with_name("arithmetic-checks.json")
    target.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
