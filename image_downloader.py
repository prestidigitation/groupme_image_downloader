import os
import re
import urllib
import httplib

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

## Fetches list of headers from URL
#  @param
#  @return 
def headers_fetcher(domain_url, path_url):
    connection = httplib.HTTPConnection(domain_url)
    connection.request("HEAD", path_url)
    res = connection.getresponse()
    headers = res.getheaders()
    return headers

## Searches list of headers for an image content type, then returns string if found
#  @param headers_list list of headers
#  @return item tuple that includes 'content-type' string
def content_type_parser(headers_list):
    for item in headers_list:
        if 'content-type' in item:
            if item[1].startswith("image"):
                return item[1]

example_domain = "sstatic.net"
example_path = "/stackoverflow/img/favicon.ico"
content_type = content_type_parser(headers_fetcher(example_domain, example_path))
print(content_type)


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
