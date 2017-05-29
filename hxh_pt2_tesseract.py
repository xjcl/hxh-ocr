import os, sys, glob
from subprocess import DEVNULL, STDOUT, check_call

import argparse


TESSERACT_OPTIONS_FILE = 'hxh_tesseract_config'
MIN_OUTPUT_SIZE = 10


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
TESSERACT_OPTIONS_FILE_FULL = IMG_DIR + 'config/' + TESSERACT_OPTIONS_FILE



check_call(['mkdir', '-p', IMG_DIR + 'output/'])
check_call(['mkdir', '-p', IMG_DIR + 'config/'])


# there seems to be no easier to way to pass these options to tesseract
with open(TESSERACT_OPTIONS_FILE_FULL, 'w') as f:
    f.write('tessedit_char_blacklist ﬁﬂ\n')
    # f.write('language_model_penalty_non_freq_dict_word 0.6\n')
    # f.write('language_model_penalty_non_dict_word 0.9\n')
    # # needed to make above two work, see https://stackoverflow.com/questions/29826591
    # f.write('enable_new_segsearch 1\n')
    # f.write('tessedit_enable_dict_correction 1\n')
    # # THESE VALUES STILL HAVE NO EFFECT ??? IS IT USING THE DICT AT ALL ?????

    # DICT ???
    # TESTS ??? flag for only certain files ?



files = list(glob.iglob(IMG_DIR + 'midput/' + '*.png'))
if args.test:
    files = list(sorted(files, key = lambda x: x[x.index('tumblr_'):]))[:args.test]


for cnt,filename_image_out in enumerate(files):

    print(cnt, '/', len(files), filename_image_out)

    # filename_image_in  = IMG_DIR + filename_image_in
    s = IMG_DIR + 'output/' + filename_image_out[len(IMG_DIR + 'midput/'):]
    filename_text_out  = s

    if os.path.isfile(filename_text_out + '.txt') and not args.force_redo:
        continue


    # ** ACTUAL WORK **

    check_call(['tesseract', '-l', 'eng', '-psm', '6', filename_image_out, filename_text_out, TESSERACT_OPTIONS_FILE_FULL], stdout=DEVNULL, stderr=DEVNULL)
    # check_call(['tesseract', '-l', 'eng', filename_image_out, filename_text_out, TESSERACT_OPTIONS_FILE_FULL])


    # tesseract keeps adding txt's even if it already ends in '.txt' :v
    filename_text_out += '.txt'

    # ** POST PROCESSING **

    # remove empty or garbage outputs
    if os.path.getsize(filename_text_out) < MIN_OUTPUT_SIZE:
        os.remove(filename_text_out)
        continue

    # TODO change into check_call
    os.system("sed -i \"s/’/'/g\" " + filename_text_out)
    os.system("sed -i \"s/‘/'/g\" " + filename_text_out)
    os.system('sed -i \"s/“/\\\"/g\" ' + filename_text_out)
    os.system('sed -i \"s/”/\\\"/g\" ' + filename_text_out)

    # TODO: detect garbage files (no dict-words(?), empty, etc)


os.remove(TESSERACT_OPTIONS_FILE_FULL)

print('done pt 2')

