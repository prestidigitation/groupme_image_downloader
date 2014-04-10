import os
import urllib

image_id = 'e3f9d0c0ac520130022766900689df55'
url = 'http://i.groupme.com/' + image_number
image = urllib.URLopener()
script_directory = os.path.dirname(os.path.abspath(__file__))

# Checks if new image directory already exists, creates it if it doesn't
if not os.path.exists(script_directory + '/images/'):
    os.makedirs(script_directory + '/images/')

image.retrieve(url, script_directory + '/images/' + image_id + '.jpg')


