#https://oauth.groupme.com/oauth/authorize?client_id=CLIENT_ID

#access token: 	284988d0a1120131fd7746de321d195f

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import requests
import time
import json
from urllib import URLopener, urlretrieve

def onRequestError(request):
    print(request.status_code)
    print(request.headers)
    print(request.text)
    sys.exit(2)

def main():
    """blah.py group_id access_token
    
Creates a folder called "group_id_images" and downloads all images in the given group's gallery to that folder.

If a folder by that name already exists, this will update the folder with any new images added to the gallery since the previous download.
    """

    if len(sys.argv) > 2:
        print(main.__doc__)
        sys.exit(1)
    
    group_id = sys.argv[1]
    access_token = sys.argv[2]
    url = 'https://api.groupme.com/v3/groups?token=' + access_token
    
    r = requests.get(url, params=params, headers=headers)
    response = r.json()
    messages = response[u'response'][u'messages']
    
    
    
    transcript = open("transcript.txt")
    for line in transcript:
        if 'http://i.groupme.com/' in line:
            
    transcript.close()
    
    image = urllib.URLopener()
    image.retrieve("")
    # parser searching for addresses beginning with http://i.groupme.com/
    
# If groupme doesn't let you download images directly through their API,
# then probably will have to download entire transcipt, then scrape it for
# image URLs, then download each one of the images from those URLs into the
# newly created folder.
