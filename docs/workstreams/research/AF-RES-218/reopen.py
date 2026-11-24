"""Read the fixed unscaled primary image in a new process."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import struct


def digest(data):
    return hashlib.sha256(data).hexdigest()


def read_sample(path, hdu_index, pixel_index):
    from astropy import units as u
    from astropy.io import fits

    path = path.resolve(strict=True)
    with path.open("rb") as file:
        info = os.fstat(file.fileno())
        raw = file.read()
        file.seek(0)
        with fits.open(file, mode="readonly", memmap=False, lazy_load_hdus=False) as hdul:
            hdu = hdul[hdu_index]
            header = hdu.header
            if len(hdul) != 1 or not isinstance(hdu, fits.PrimaryHDU):
                raise ValueError("expected the single primary HDU")
            if header["BITPIX"] != -64 or header["NAXIS"] != 1:
                raise ValueError("expected the one-dimensional 64-bit float fixture")
            if any(key in header for key in ("BSCALE", "BZERO", "BLANK")):
                raise ValueError("expected an unscaled fixture")
            if not 0 <= pixel_index < header["NAXIS1"]:
                raise ValueError("pixel outside the fixture")

            offsets = hdul.fileinfo(hdu_index)
            hdu_data_start = offsets["datLoc"]
            hdu_data_end = hdu_data_start + offsets["datSpan"]
            pixel_start = hdu_data_start + pixel_index * 8
            pixel = raw[pixel_start:pixel_start + 8]
            raw_value = struct.unpack(">d", pixel)[0]
            value = float(hdu.data[pixel_index])
            if raw_value != value or hdu_data_end != len(raw):
                raise ValueError("wire value or primary HDU span disagrees")
            file.seek(0)
            if file.read() != raw or not os.path.samestat(info, path.stat()):
                raise ValueError("file changed during this independent read")

            return {
                "pid": os.getpid(),
                "path": str(path),
                "device": info.st_dev,
                "inode": info.st_ino,
                "size_bytes": len(raw),
                "hdu_index": hdu_index,
                "pixel_index": pixel_index,
                "bitpix": header["BITPIX"],
                "naxis": header["NAXIS"],
                "naxis1": header["NAXIS1"],
                "bunit": header["BUNIT"],
                "unit": str(u.Unit(header["BUNIT"], format="fits")),
                "history": [card.value for card in header.cards if card.keyword == "HISTORY"],
                "dtype": hdu.data.dtype.str,
                "data_offset": hdu_data_start,
                "pixel_offset": pixel_start,
                "value": value,
                "raw_pixel_value": raw_value,
                "raw_pixel_hex": pixel.hex(),
                "sha256": digest(raw),
                "header_sha256": digest(raw[offsets["hdrLoc"]:hdu_data_start]),
                "data_sha256": digest(raw[hdu_data_start:hdu_data_end]),
                "other_data_sha256": digest(raw[hdu_data_start:pixel_start] +
                                            raw[pixel_start + 8:hdu_data_end]),
            }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", type=Path)
    parser.add_argument("--hdu", type=int, required=True)
    parser.add_argument("--pixel", type=int, required=True)
    args = parser.parse_args()
    print(json.dumps(read_sample(args.file, args.hdu, args.pixel), allow_nan=False))
