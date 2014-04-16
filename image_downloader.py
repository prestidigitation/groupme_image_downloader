import os
import re
import urllib

import imghdr
import httplib
import cStringIO

# Need parser that searches txt file for addresses beginning with http://i.groupme.com/

group_id = "transcript-5815609.txt"
transcript = open(group_id)
for line in transcript:
    pass
#    # Do string processing here
#    #if 'http://i.groupme.com/' in 
#    #re.search(pattern, string, flags=0)
#    match = re.search('http://i.groupme.com/', line, flags=0)
#    if match:
#        process(match)
    
#transcript.close()

#handlers= {"p": # p tag handler
#           "h1": # h1 tag handler
#          }

## ... in the loop
#    if lyne.rstrip() in handlers :  # strip to remove trailing whitespace
#       # close current handler?
#        # start new handler?
#    else :
        # pass string to current handler

example_domain = 'www.ovguide.com'
example_path = '/img/global/ovg_logo.png'

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

image_id = 'e3f9d0c0ac520130022766900689df55'
url = 'http://i.groupme.com/' + image_id
image = urllib.URLopener()
script_directory = os.path.dirname(os.path.abspath(__file__))

## Checks if new image directory exists, creates one if it doesn't
# 
if not os.path.exists(script_directory + '/images/'):
    os.makedirs(script_directory + '/images/')

image.retrieve(url, script_directory + '/images/' + image_id + '.jpg')

# (?P<url>http?://[^\s]+)