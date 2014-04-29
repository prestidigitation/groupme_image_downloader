from os import makedirs
from os.path import (dirname, exists, abspath)
from re import search
from urllib.error import (HTTPError, URLError)
from urllib.request import urlopen
from imghdr import what
from socket import timeout


## Checks if new image directory exists, creates one if it doesn't.
def directory_exists():
    script_directory = dirname(abspath(__file__))
    if not exists(script_directory + '/images/'):
        makedirs(script_directory + '/images/')


## Parses a transcript file for urls.
#  @param transcript_file name of transcript file to be parsed
#  @return string of matched url
def file_parser(transcript_file):
    for line in transcript_file:
        # Do string processing here
        match = search('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', line)
        if match is not None:
            print(match.group(0))  # TODO Remove when done testing.
            try:
                print(str(is_image(match.group(0))))  # TODO Remove when done testing.
                if is_image(match.group(0)):
                    img_url_writer(match.group(0))
                    #img_downloader()
                else:
                    non_img_url_writer(match.group(0))
            except HTTPError as err:
                print("Bad URL or timeout: {0}".format(err))
                continue
            except URLError as err:
                print("Bad URL or timeout: {0}".format(err))
                continue
            except timeout as err:
                print("Timeout error: {0}".format(err))
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


## Downloads image to folder.
#  @param img_url url of image to be downloaded.
def img_downloader(img_url):
    urlopen(img_url).write()

file_name = 'transcript-5815609.txt'
transcript = open(file_name, "r")

file_parser(transcript)
transcript.close()
