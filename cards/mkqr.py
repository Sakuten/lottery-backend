#!/usr/bin/env python

import qrcode


def gen_qr_code(out_dir, base_url, secret_id):
    """generate QR code from URL and secret key
        Parameters:
            secret_id (str): secret id to include

        1. Build URL which will be contained in QR code
        2. Generate QR code
        3. return path to the image
    """

    final_url = base_url + secret_id

    img = qrcode.make(final_url)
    qr_path = f"{out_dir}/{secret_id}.png"
    img.save(qr_path)

    return qr_path
