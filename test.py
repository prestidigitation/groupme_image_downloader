__author__ = "Antony Cherepanov"

import image_downloader


def test_is_image_valid_url():
    valid_url = "http://upload.wikimedia.org/wikipedia/commons/f/ff/Picea_likiangensis.jpg"
    assert(image_downloader.is_image(valid_url))


def test_is_image_invalid_url():
    invalid_url = "http://upload.wikimedia.org/wikipedia/commons/f/ff/Picea_likiangensis.txt"
    assert(not image_downloader.is_image(invalid_url))


if __name__ == '__main__':
    test_is_image_valid_url()
    print("Tests passed!")