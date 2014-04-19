import os
import re
import urllib

import imghdr
import httplib
import cStringIO

## Checks if new image directory exists, creates one if it doesn't
#  @param N/a
#  @return N/a
def directory_exists():
    script_directory = os.path.dirname(os.path.abspath(__file__))
    if not os.path.exists(script_directory + '/images/'):
        os.makedirs(script_directory + '/images/')


## Checks url to see if it's an image.
#  @param domain_url http domain of a potential image's url
#  @param path_url path of potential image's url that gets appended to a domain url
#  @return is_image_bool Boolean value for whether url contains an image or not
def is_image(domain_url, path_url):
    domain_fetcher = httplib.HTTPConnection(domain_url, timeout = 60)
    domain_fetcher.request('GET', path_url)
    r1 = domain_fetcher.getresponse()

    image_file_obj = cStringIO.StringIO(r1.read())
    what_type = imghdr.what(image_file_obj)

    is_image_bool = False
    if what_type != None:
        is_image_bool = True
    return is_image_bool


## Parses a transcript file for urls.
#  @param transcript_file Name of transcript file to be parsed
#  @return match String of matched url
def file_parser(transcript_file):
    for line in transcript_file:
        # Do string processing here
        match = re.search('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', line)
        if match != None:
            #if is_image(match):
            print(match.group(0))

example_domain = 'www.ovguide.com'
example_path = '/img/global/ovg_logo.png'
file_name = "transcript-5815609.txt"
transcript = open(file_name, "r")
image_id = 'e3f9d0c0ac520130022766900689df55'
url = 'http://i.groupme.com/' + image_id
image = urllib.URLopener()


file_parser(transcript)
transcript.close()
#image.retrieve(url, script_directory + '/images/' + image_id + '.jpg')

