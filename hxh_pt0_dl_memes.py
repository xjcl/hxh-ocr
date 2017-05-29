import os
from subprocess import DEVNULL, STDOUT, check_call

import urllib.request

import argparse


TESSERACT_OPTIONS_FILE = 'hxh-tesseract-config'
MIN_OUTPUT_SIZE = 10


parser = argparse.ArgumentParser(description='gay')
parser.add_argument('--image-dir', dest='image_dir',
                    default='/home/jan/Music/pics/hxh-textposts/')
args = parser.parse_args()

IMG_DIR = args.image_dir



check_call(['mkdir', '-p', IMG_DIR + 'input/'])

with open(IMG_DIR + 'input/hxh_urls', 'w') as f:
    check_call(['ruby', 'tumblr-photo-ripper-urls.rb'], stdout=f)

with open(IMG_DIR + 'input/hxh_urls') as f:
    n = sum(1 for line in f)

with open(IMG_DIR + 'input/hxh_urls') as f:

    for cnt,url in enumerate(f):

        print(cnt, '/', n, url)

        url = url.rstrip()  # strip the single newline
        filename = url.replace('/', '+').replace(':', '-')

        # Download the file if it does not exist
        if not os.path.isfile(IMG_DIR + filename):
            urllib.request.urlretrieve(url, IMG_DIR + filename)


print('done pt 0')
