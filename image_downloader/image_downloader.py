from os import makedirs
from os.path import (dirname, exists, abspath)
from re import search
from urllib.error import (HTTPError, URLError)
from urllib.request import (urlopen, urlretrieve)
from imghdr import what
from socket import timeout


## Parses a file for urls.
#  @param file_name name of file to be parsed
#  @return string of matched url
def file_parser(file_name):
    for line in file_name:
        match = search('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', line)
        current_match = match.group(0)
        if match is not None:
            try:
                if is_image(current_match):
                    img_url_writer(current_match)
                    img_downloader(current_match)
                else:
                    non_img_url_writer(current_match)
            except HTTPError as err:
                print(current_match + '\n' + "Bad URL or timeout: {0}".format(err))
                continue
            except URLError as err:
                print(current_match + '\n' + "Bad URL or timeout: {0}".format(err))
                continue
            except timeout as err:
                print(current_match + '\n' + "Timeout error: {0}".format(err))
                continue
            except IsADirectoryError as err:
                print("IsADirectoryError: {0}".format(err))
                continue


## Checks url to see if it's an image.
#  @param url Url of a potential image
#  @return boolean value for whether url contains an image
def is_image(url):
    url_data = urlopen(url, timeout=60).read()
    what_type = what('ignore', url_data)

    is_image_bool = False
    if what_type is not None:
        is_image_bool = True
    return is_image_bool


## Writes parsed image urls to text file.
#  @param url_string url string to be appended to text file
def img_url_writer(url_string):
    urls = open('image_urls.txt', 'a')
    urls.write(url_string + '\n')
    urls.close()


## Writes parsed non-image urls to text file.
#  @param url_string url string to be appended to text file
def non_img_url_writer(url_string):
    urls = open('non_image_urls.txt', 'a')
    urls.write(url_string + '\n')
    urls.close()


## Checks if new image directory exists, creates one if it doesn't.
def directory_exists():
    script_directory = dirname(abspath(__file__))
    if not exists(script_directory + '/images/'):
        makedirs(script_directory + '/images/')


## Downloads image to folder.
#  @param img_url url of image to be downloaded.
def img_downloader(url):
    directory_exists()
    transcript_directory = dirname(abspath(__file__))
    split = url.rsplit('/', 1)
    urlretrieve(url, transcript_directory + '/images/' + url.rsplit('/', 1)[1])


transcript_name = input('Enter transcript to be parsed: ')
transcript = open(transcript_name, "r")

file_parser(transcript)
transcript.close()
print("Done.")