__author__ = "Antony Cherepanov"

import image_downloader
import os


def test_is_image_valid_url():
    valid_url = "http://upload.wikimedia.org/wikipedia/commons/f/ff/Picea_likiangensis.jpg"
    assert(image_downloader.is_image(valid_url))


def test_is_image_invalid_url():
    invalid_url = "http://upload.wikimedia.org/wikipedia/commons/f/ff/Picea_likiangensis.txt"
    assert(not image_downloader.is_image(invalid_url))


def test_check_dir_valid_path():
    path = os.getcwd() + "/test_folder"

    # Check if such folder exist
    if not os.path.exists(path):
        os.makedirs(path)

    assert(image_downloader.check_dir(path))

    # Check with non existent folder
    os.rmdir(path)
    assert(image_downloader.check_dir(path))
    os.rmdir(path)


def test_check_dir_invalid_path():
    fake_folder_path = "/fake/folder"
    assert(not image_downloader.check_dir(fake_folder_path))


if __name__ == '__main__':
    test_is_image_valid_url()
    test_is_image_invalid_url()
    test_check_dir_valid_path()
    test_check_dir_invalid_path()

    print("Tests passed!")