import sys
import os
import re
from urllib.error import HTTPError, URLError
from urllib.request import urlretrieve
from socket import timeout
import multiprocessing
import time


def start():
    """ Main method """

    if len(sys.argv) != 3:
        print("Invalid arguments")
        sys.exit()

    print("Checking...")
    file = open_text_file(sys.argv[1])
    if file is None:
        sys.exit()

    valid_urls = file_parser(file)
    file.close()
    if len(valid_urls) <= 0:
        print("Nothing to download")
        sys.exit()

    folder_path = sys.argv[2]
    if not check_dir(folder_path):
        print("Failed to create folder for images")
        sys.exit()

    print("Downloading...")
    start_download(valid_urls, folder_path)
    print("Done.")


def open_text_file(t_file_path):
    """ Opens a text file.
    @input: t_file_path - string with path to the file with URLs
    @output: transcript - successfully opened text file
    """

    transcript = None
    try:
        transcript = open(t_file_path, "r")
    except OSError:
        print('Failed to open file!')

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
        except HTTPError as err:
            print(current_match + '\n' + "Bad URL or timeout: {0}".format(err))
            continue
        except URLError as err:
            print(current_match + '\n' + "Bad URL or timeout: {0}".format(err))
            continue
        except timeout as err:
            print(current_match + '\n' + "Timeout error: {0}".format(err))
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
        os.makedirs(t_path)

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
            print("Failed to download " + url)
            continue

        print(url + " downloaded.")
        time.sleep(2)


if __name__ == '__main__':
    start()