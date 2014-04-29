import os
import re
from urllib.request import urlopen
from imghdr import what


## Checks if new image directory exists, creates one if it doesn't.
def directory_exists():
    script_directory = os.path.dirname(os.path.abspath(__file__))
    if not os.path.exists(script_directory + '/images/'):
        os.makedirs(script_directory + '/images/')


## Parses a transcript file for urls.
#  @param transcript_file name of transcript file to be parsed
#  @return string of matched url
def file_parser(transcript_file):
    for line in transcript_file:
        # Do string processing here
        match = re.search('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', line)
        if match is not None:
            #if is_image(match):
            print(match.group(0))


## Checks url to see if it's an image.
#  @param url Url of a potential image
#  @return boolean value for whether url contains an image
def is_image(url):
    url_data = urlopen(url).read()
    what_type = what('ignore', url_data)

    is_image_bool = False
    if what_type is not None:
        is_image_bool = True
    return is_image_bool


file_name = 'transcript-5815609.txt'
transcript = open(file_name, "r")

file_parser(transcript)
transcript.close()
