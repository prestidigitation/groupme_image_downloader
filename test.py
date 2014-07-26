__author__ = "Antony Cherepanov"

import image_downloader
import os
import shutil


def test_is_image_valid_url():
    valid_url = "http://upload.wikimedia.org/wikipedia/commons/f/ff/Picea_likiangensis.jpg"
    assert(image_downloader.is_image(valid_url))


def test_is_image_invalid_url():
    invalid_url = "http://upload.wikimedia.org/wikipedia/commons/f/ff/Picea_likiangensis.txt"
    assert(not image_downloader.is_image(invalid_url))


def test_check_dir_valid_path():
    # Check with existent folder
    path = get_path_to_folder_for_images()
    assert(image_downloader.check_dir(path))

    # Check with non existent folder
    remove_folder(path)
    assert(image_downloader.check_dir(path))
    remove_folder(path)


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


def test_file_parsing():
    file_path = create_file_with_urls()
    file = open(file_path, 'r')
    num_of_urls = sum(1 for line in file)
    file.seek(0, 0)
    valid_urls = image_downloader.file_parser(file)

    file.close()
    remove_file(file_path)

    if len(valid_urls) != num_of_urls:
        raise Exception("Fail. Not all URLs validated")


def test_img_downloader_valid_urls():
    urls = get_test_urls()
    folder_path = get_path_to_folder_for_images()
    image_downloader.img_downloader(urls, folder_path)

    files = os.listdir(folder_path)
    remove_folder(folder_path)
    if len(files) != len(urls):
        raise Exception("Fail. Not all images was downloaded")


def test_img_downloader_invalid_urls():
    urls = get_invalid_urls()
    folder_path = get_path_to_folder_for_images()
    image_downloader.img_downloader(urls, folder_path)

    files = os.listdir(folder_path)
    remove_folder(folder_path)
    if len(files) != 0:
        raise Exception("Fail. Image downloaded by invalid link")


def test_start_download():
    urls = get_test_urls()
    folder_path = get_path_to_folder_for_images()
    image_downloader.start_download(urls, folder_path)

    files = os.listdir(folder_path)
    remove_folder(folder_path)
    if len(files) != len(urls):
        raise Exception("Fail. Not all images was downloaded")


def test_start():
    file_path = create_file_with_urls()
    file = open(file_path, 'r')
    num_of_urls = sum(1 for line in file)
    file.close()

    folder_path = get_path_to_folder_for_images()
    image_downloader.start(file_path, folder_path)

    files = os.listdir(folder_path)
    remove_folder(folder_path)
    remove_file(file_path)
    if len(files) != num_of_urls:
        raise Exception("Fail. Not all images was downloaded")


def create_empty_file():
    path = get_test_file_path()
    open(path, 'a').close()
    return path


def get_test_file_path():
    return os.getcwd() + "/test_file.txt"


def create_file_with_urls():
    path = get_test_file_path()
    urls = get_test_urls()
    with open(path, 'a') as file:
        for url in urls:
            file.write(url + "\n")
        file.close()

    return path


def get_test_urls():
    urls = list()
    urls.append("http://upload.wikimedia.org/wikipedia/commons/f/ff/Picea_likiangensis.jpg")
    urls.append("http://farm1.static.flickr.com/67/175175908_9d19e087c7.jpg")
    urls.append("http://upload.wikimedia.org/wikipedia/commons/thumb/8/80/Wikipedia-logo-v2.svg/150px-Wikipedia-logo-v2.svg.png")
    return urls


def get_invalid_urls():
    urls = list()
    urls.append("http://www.bountiful-farms.com/photos/plants/piceafastigiata.jpg")
    return urls


def remove_file(t_path):
    os.remove(t_path)


def get_path_to_folder_for_images():
    path = os.getcwd() + "/test_folder"
    if not os.path.exists(path):
        os.mkdir(path)

    return path


def remove_folder(t_path):
    shutil.rmtree(t_path, True)


if __name__ == '__main__':
    test_is_image_valid_url()
    test_is_image_invalid_url()

    test_check_dir_valid_path()
    test_check_dir_invalid_path()

    test_open_file_valid()
    test_open_file_invalid()

    test_file_parsing()

    test_img_downloader_valid_urls()
    test_img_downloader_invalid_urls()

    test_start_download()

    test_start()

    print("Tests passed!")