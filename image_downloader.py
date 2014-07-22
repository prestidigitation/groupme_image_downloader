import sys
import os
import re
from urllib.error import HTTPError, URLError
from urllib.request import urlopen, urlretrieve
import imghdr
from socket import timeout
import multiprocessing
import itertools


## Opens a text file.
#  @param: t_file_path - string with path to the file with URLs
#  @return: transcript - successfully opened text file
def open_text_file(t_file_path):
    transcript = None
    try:
        transcript = open(t_file_path, "r")
    except OSError:
        print('Failed to open file!')

    return transcript


## Parses a file for urls.
#  @param: t_file - file object to be parsed
#  @return: list of valid URLs
def file_parser(t_file):
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


## Checks url to see if it's an image.
#  @param: t_url - Url of a potential image
#  @return: boolean value for whether url contains an image
def is_image(t_url):
    try:
        url_data = urlopen(t_url, timeout=60).read()
    except URLError as err:
        return False

    what_type = imghdr.what("filename to ignore", url_data)
    if what_type is None:
        return False

    return True


## Checks if new image directory exists, creates one if it doesn't.
#  @param: t_path - string with path to folder for images
#  @return: boolean value for whether path to folder is OK
def check_dir(t_path):
    if not os.path.isabs(t_path):
        return False
    if not os.path.isdir(t_path):
        os.makedirs(t_path)

    return True


## Start downloader threads
def start_download(t_urls, t_folder):
    cores_num = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(cores_num)
    pool.map(img_downloader, zip(t_urls, itertools.repeat(t_folder)))
    pool.close()
    pool.join()


## Downloads images to folder.
#  @param: t_urls - list of url of image to be downloaded
#  @param: t_folder - folder for images
def img_downloader(params):
    t_urls, t_folder = params
    for url in t_urls:
        print(url)
        path = os.path.join(t_folder, url.rsplit('/', 1)[1])
        try:
            urlretrieve(url, path)
        except URLError as err:
            print("Failed to download: " + url)
            print(err.reason)
            continue


## Main method
def start():
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


if __name__ == '__main__':
    start()