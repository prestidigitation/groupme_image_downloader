from sys import exit, argv
from os import makedirs
from os.path import dirname, exists, abspath, isabs, isdir
from re import search
from urllib.error import HTTPError, URLError, ContentTooShortError
from urllib.request import urlopen, urlretrieve
from imghdr import what
from socket import timeout


## Parses a file for urls.
#  @param: file_name - name of file to be parsed
#  @return: list of valid URLs
def file_parser(file_name):
    valid_urls = list()
    for line in file_name:
        match = search('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', line)
        try:
            current_match = match.group(0)
        except AttributeError:
            continue

        if match is not None:
            try:
                if is_image(current_match):
                    valid_urls.append(current_match)
            except HTTPError as err:
                print(current_match + '\n' + "Bad URL or timeout: {0}".format(err))
                continue
            except URLError as err:
                print(current_match + '\n' + "Bad URL or timeout: {0}".format(err))
                continue
            except timeout as err:
                print(current_match + '\n' + "Timeout error: {0}".format(err))
                continue

    return valid_urls


## Checks url to see if it's an image.
#  @param: url - Url of a potential image
#  @return: boolean value for whether url contains an image
def is_image(url):
    url_data = urlopen(url, timeout=60).read()
    what_type = what('ignore', url_data)

    is_image_bool = False
    if what_type is not None:
        is_image_bool = True

    return is_image_bool


## Checks if new image directory exists, creates one if it doesn't.
#  @param: t_path - string with path to folder for images
#  @return: boolean value for whether path to folder is OK
def check_dir(t_path):
    if not isabs(t_path):
        return False
    if not isdir(t_path):
        makedirs(t_path)

    return True


## Downloads images to folder.
#  @param: t_urls - list of url of image to be downloaded
#  @param: t_folder - folder for images
def img_downloader(t_urls, t_folder):
    images_per_percent = len(t_urls) / 100
    counter = 0
    percent = 0

    for url in t_urls:
        counter += 1
        path = t_folder + url.rsplit('/', 1)[1]
        try:
            urlretrieve(url, path)
        except URLError as err:
            print("Failed to download: " + url)
            print(err.reason)
            continue

        if counter == images_per_percent:
            counter = 0
            percent += 1
            print(percent + "%")


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


## Main method
def start():
    if len(argv) != 2:
        print("Invalid arguments")
        exit()

    file = open_text_file(argv[0])
    if file is None:
        exit()

    valid_urls = file_parser(file)
    file.close()
    if len(valid_urls) <= 0:
        print("Nothing to download")
        exit()

    folder_path = argv[1]
    if not check_dir(folder_path):
        print("Failed to create folder for images")
        exit()

    img_downloader(valid_urls, folder_path)
    print("Done.")


if __name__ == '__main__':
    start()