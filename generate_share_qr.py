#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

import qrcode
from qrcode.constants import ERROR_CORRECT_H


ROOT = Path(__file__).resolve().parent


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a QR code for the report share page.")
    parser.add_argument(
        "--url",
        default="https://kentwu-730.github.io/accio-weekly-report/",
        help="Target URL for the QR code.",
    )
    parser.add_argument(
        "--output",
        default=str(ROOT / "share-qr.png"),
        help="Output PNG path.",
    )
    args = parser.parse_args()

    qr = qrcode.QRCode(
        version=None,
        error_correction=ERROR_CORRECT_H,
        box_size=12,
        border=4,
    )
    qr.add_data(args.url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    output = Path(args.output).expanduser().resolve()
    img.save(output)
    print(output)


if __name__ == "__main__":
    main()
