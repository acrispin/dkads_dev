import os
import qrcode
from uuid import uuid4

BASE_URL = "http://idtaxi.pe/unidad/%s"

def _create(data, out_file, out_directory):
    x = qrcode.QRCode(version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=10,
                    border=4)

    x.add_data(data)
    x.make()
    if not os.path.exists(out_directory):
        os.mkdir(out_directory)
    img = x.make_image()
    img.save(os.path.join(out_directory, out_file))

def generate(out_directory=""):
    _uuid = str(uuid4())
    if not out_directory:
        out_directory = os.curdir
    _create(BASE_URL % _uuid, _uuid + ".png", out_directory)
    return _uuid

if __name__ == "__main__":
    generate()
