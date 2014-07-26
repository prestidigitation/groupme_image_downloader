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

    fake_folder = "../fake/folder"
    assert(not image_downloader.check_dir(fake_folder))


def test_open_file_invalid():
    fake_file = "/fake/file.txt"
    assert(not image_downloader.open_text_file(fake_file))


def test_open_file_valid():
    file_path = create_empty_file()
    assert(image_downloader.open_text_file(file_path))
    remove_file(file_path)


def create_empty_file():
    path = os.getcwd() + "/test_file.txt"
    open(path, 'a').close()
    return path


def create_file_with_urls():
    path = os.getcwd() + "/test_file.txt"
    with open(path, 'a') as file:
        file.write("http://upload.wikimedia.org/wikipedia/commons/f/ff/Picea_likiangensis.jpg")
        file.write("http://www.bountiful-farms.com/photos/plants/piceafastigiata.jpg")
        file.write("http://farm1.static.flickr.com/67/175175908_9d19e087c7.jpg")

    return path


def remove_file(t_path):
    os.remove(t_path)


if __name__ == '__main__':
    test_is_image_valid_url()
    test_is_image_invalid_url()
    test_check_dir_valid_path()
    test_check_dir_invalid_path()
    test_open_file_invalid()
    test_open_file_valid()

    print("Tests passed!")