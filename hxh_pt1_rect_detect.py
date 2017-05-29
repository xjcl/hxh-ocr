import os, sys, glob
from subprocess import DEVNULL, STDOUT, check_call

import numpy

import PIL
import PIL.Image

import argparse



parser = argparse.ArgumentParser(description='gay')
# parser.add_argument('--force-redo', dest='force_redo', action='store_true',
parser.add_argument('--delete-cache', dest='force_redo', action='store_true',
                    help='ignore output directy and re-do entire workload')
parser.add_argument('--test', dest='test', type=int, default=0,
                    help='only act on the lexicographically first n images (for testing)')
parser.add_argument('--image-dir', dest='image_dir',
                    default='/home/jan/Music/pics/hxh-textposts/')
args = parser.parse_args()

IMG_DIR = args.image_dir


BORDER = 5
# SCALE = 3.6
SCALE = 4
MIN_HEIGHT = 12
# ^ TODO base SCALE on text-height / x-height or sth



# algo
# return points with
#   - first line runs id at least 12% of width
#   - id at least 12 px below on borders

# TODO: make faster with numpy !!
def rect_detect_find_corners(data):

    rets = []
    rect_height = 0

    for i in range(BORDER, len(data)-BORDER):

        if rect_height > 0:
            rect_height -= 1
            continue

        currunlen = 0
        currunpos = (i, 0)

        linerunlen = 0
        linerunpos = None

        for j in range(BORDER, len(data[0])-BORDER):
            if all(data[i][j] == data[i][j-1]):  # RGB !
                currunlen += 1
                if currunlen > .12*len(data[0]):
                    linerunlen = currunlen
                    linerunpos = currunpos
            else:
                currunlen = 0
                currunpos = (i, j)

        if linerunpos:
            j1 = linerunpos[1]
            j2 = linerunpos[1]+linerunlen

            for i in range(linerunpos[0]+1, len(data)-BORDER):
                if not all(data[i][j1] == data[i-1][j1]):
                    break
                if not all(data[i][j2] == data[i-1][j2]):
                    break
                rect_height += 1

            if rect_height > MIN_HEIGHT:
                rets.append(
                    (j1, j2, linerunpos[0], linerunpos[0]+rect_height)
                )

    print(rets)

    return rets


def rect_detect(image):
    data = numpy.asarray(image)

    rets = []

    for point in rect_detect_find_corners(data):

        xlo, xhi, ylo, yhi = point

        ret = image.crop((xlo, ylo, xhi, yhi))

        # tesseract requires upscaling such that x-height-8px font wont be considered noise
        # they should just have a --small-text or --screen-text option. sad!
        ret = ret.resize((int(SCALE*ret.width), int(SCALE*ret.height)), PIL.Image.ANTIALIAS)
        # TODO try w/o antialias

        rets.append(ret)

    return rets




check_call(['mkdir', '-p', IMG_DIR + 'midput/'])


files = list(glob.iglob(IMG_DIR + '*.png'))
if args.test:
    files = list(sorted(files, key = lambda x: x[x.index('tumblr_'):]))[:args.test]

for cnt,filename_image_in in enumerate(files):

    print(cnt, '/', len(files), filename_image_in)

    # filename_image_in  = IMG_DIR + filename_image_in
    filename_image_out_base = IMG_DIR + 'midput/' + filename_image_in[len(IMG_DIR):]

    if os.path.isfile(filename_image_out_base + '.0.png') and not args.force_redo:
        continue


    image = PIL.Image.open(filename_image_in)

    images = rect_detect(image)

    for i,image in enumerate(images):
        image.save(filename_image_out_base + '.' + str(i) + '.png')



print('done pt 1')

