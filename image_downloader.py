import sys
import os
import re
from urllib.error import HTTPError, URLError
from urllib.request import urlretrieve
from socket import timeout
import multiprocessing
import time


def start(t_path_to_file, t_folder_for_images):
    """ Main method with app algorithm
    @input: t_path_to_file - string with path to the file with URLs
            t_folder_for_images - string with path to the folder for downloaded images
    """

    print(get_local_time_string() + ": Checking...")
    file = open_text_file(t_path_to_file)
    if file is None:
        sys.exit()

    valid_urls = file_parser(file)
    file.close()
    if len(valid_urls) <= 0:
        print(get_local_time_string() + ": Nothing to download")
        sys.exit()

    if not check_dir(t_folder_for_images):
        print(get_local_time_string() + ": Failed to create folder for images")
        sys.exit()

    print(get_local_time_string() + ": Downloading...")
    start_download(valid_urls, t_folder_for_images)

    print(get_local_time_string() + ": Done.")


def get_local_time_string():
    """ Get string with current date and local time
    @output: string with date and time
    """

    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


def open_text_file(t_file_path):
    """ Opens a text file.
    @input: t_file_path - string with path to the file with URLs
    @output: transcript - successfully opened text file
    """

    transcript = None
    try:
        transcript = open(t_file_path, "r")
    except (OSError, IOError):
        print(get_local_time_string() + ": Failed to open file!")

    return transcript


def file_parser(t_file):
    """ Parses a file for urls.
    @input: t_file - file object to be parsed
    @output: list of valid URLs
    """

    valid_urls = list()
    for line in t_file:
        match = re.search('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', line)
        try:
            current_match = match.group(0)
        except AttributeError:
            continue

        if match is None:
            continue

        try:
            check_result = is_image(current_match)
        except (HTTPError, URLError, timeout) as err:
            print(current_match + '\n' + "Bad URL or timeout: {0}".format(err))
            continue

        if check_result is True:
            valid_urls.append(current_match)

    return valid_urls


def is_image(t_url):
    """ Checks url to see if it's an image (only check extension)
    @input: t_url - Url of a potential image
    @output: boolean value for whether url contains an image
    """

    image_extensions = ["jpg", "jpeg", "bmp", "png", "gif", "tiff"]
    url_parts = str.split(t_url, '.')
    extension = url_parts[-1:][0]
    extension = extension.lower()

    if extension in image_extensions:
        return True

    return False


def check_dir(t_path):
    """ Checks if new image directory exists, creates one if it doesn't.
    @input: t_path - string with path to folder for images
    @output: boolean value for whether path to folder is OK
    """

    if not os.path.isabs(t_path):
        return False
    if not os.path.isdir(t_path):
        try:
            os.makedirs(t_path)
        except OSError:
            return False

    return True


def start_download(t_urls, t_path):
    """ Start downloading process
    @input: t_urls - list of URLs
            t_path - string with path to folder for images
    """

    cores_num = multiprocessing.cpu_count()
    url_chunks = list_split(t_urls, cores_num)
    jobs = list()
    for i in range(cores_num):
        thread = multiprocessing.Process(target=img_downloader, args=(next(url_chunks), t_path,))
        jobs.append(thread)
        thread.start()

    for thread in jobs:
        thread.join()


def list_split(t_list, t_size):
    """ Generator that split list of elements in n chunks
    @input: t_list - list of elements
            t_size - size of chunk
    @output: generator of lists of chunks
    """

    new_length = int(len(t_list) / t_size)
    for i in range(0, t_size - 1):
        yield t_list[i * new_length:i * new_length + new_length]
    yield t_list[t_size * new_length - new_length:]


def img_downloader(t_urls, t_folder):
    """ Downloads images to folder.
    @input: t_urls - list of url of image to be downloaded
            t_folder - folder for images
    """

    for url in t_urls:
        path = os.path.join(t_folder, url.rsplit('/', 1)[1])
        try:
            urlretrieve(url, path)
        except Exception:
            print(get_local_time_string() + ": Failed to download " + url)
            continue

        print(get_local_time_string() + ": " + url + " downloaded.")
        time.sleep(2)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Invalid arguments")
        sys.exit()

    path_to_file = sys.argv[1]
    folder_for_images = sys.argv[2]
    start(path_to_file, folder_for_images)