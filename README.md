[![Build Status](https://travis-ci.org/iamantony/image_downloader.svg?branch=master)](https://travis-ci.org/iamantony/image_downloader)  [![Coverage Status](https://coveralls.io/repos/iamantony/image_downloader/badge.png)](https://coveralls.io/r/iamantony/image_downloader)

image_downloader
========================

Multithread image downloader.

Python app for parsing a text file for urls, then downloading all images from those urls.

Usage
=======================

    $ image_downloader PATH_TO_FILE FOLDER_FOR_IMAGES

* PATH_TO_FILE - absolute path to the txt-file with URLs
* FOLDER_FOR_IMAGES - absolute path to folder where downloaded images should be saved.
Folder will be created if it's not exist.
