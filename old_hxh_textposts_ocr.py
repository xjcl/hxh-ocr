import os, sys, glob
from subprocess import DEVNULL, STDOUT, check_call
from itertools import chain

import numpy

import PIL
from PIL import Image




BASE_IMG_DIR = '/home/jan/Music/pics/hxh-textposts/'
TESSERACT_OPTIONS_FILE = 'hxh-tesseract-config'
BORDER = 5
SCALE = 3


def max_run_info(data):

    maxrunlen = 0
    maxrunpos = (0, 0)

    for i in range(BORDER, len(data)-BORDER):
        currunlen = 0
        currunpos = (i, 0)
        for j in range(BORDER, len(data[0])-BORDER):
            if all(data[i][j] == data[i][j-1]):  # RGB !
                currunlen += 1
                if currunlen > maxrunlen:
                    maxrunlen = currunlen
                    maxrunpos = currunpos
            else:
                currunlen = 0
                currunpos = (i, j)

    final_height = 0
    j = maxrunpos[1]
    for i in range(maxrunpos[0]+1, len(data)-BORDER):
        if not all(data[i][j] == data[i-1][j]):
            break
        final_height += 1

    return (maxrunpos[1], maxrunpos[1]+maxrunlen,
        maxrunpos[0], maxrunpos[0]+final_height)




# there seems to be no easier to way to pass these options to tesseract
with open(TESSERACT_OPTIONS_FILE, 'w') as f:
    # f.write('tessedit_char_blacklist ﬁﬂ\n')
    # f.write('tessedit_char_blacklist ﬁﬂ\ndebug_file /dev/null\n')
    f.write('tessedit_char_blacklist ﬁﬂ\nlanguage_model_penalty_non_freq_dict_word 0.3\nlanguage_model_penalty_non_dict_word 0.6\n')
    # ^ this suppressed the error-lines but not the info-lines :(


# language_model_penalty_non_freq_dict_word 0.6
# language_model_penalty_non_dict_word 0.9

check_call(['mkdir', '-p', BASE_IMG_DIR + 'output'])



# '??' needed as some end in '.1', '.2' etc
for filename_image_in in chain(
    glob.iglob(BASE_IMG_DIR + '*.png'),
    glob.iglob(BASE_IMG_DIR + '*.png??')
):
# for filename_image_in in ['tumblr_nt8lhcaOkH1ue484to1_1280.png', 'tumblr_nt8lkybAf11ue484to1_1280.png']:

    # filename_image_in  = BASE_IMG_DIR + filename_image_in
    s = BASE_IMG_DIR + 'output/' + filename_image_in[len(BASE_IMG_DIR):]
    filename_image_out = s + '.textonly.png'
    filename_text_out  = s + '.to-text'

    if os.path.isfile(filename_text_out + '.txt'):
        continue


    # ** ACTUAL WORK **

    image = Image.open(filename_image_in)
    data = numpy.asarray(image)

    # xlo, xw = max_run_info(data)
    # # ylo, yh = max_run_info(numpy.transpose(data))
    # ylo, yh = max_run_info(data.transpose(1,0,2))  # 2nd axis is RGB
    # xhi = xlo + xw
    # yhi = ylo + yh

    xlo, xhi, ylo, yhi = max_run_info(data)

    if xhi-xlo < .12*image.width or yhi-ylo < 12:
        print(filename_image_in, file=sys.stdout)  # stderr m
        continue

    image = image.crop((xlo, ylo, xhi, yhi))

    # tesseract requires upscaling such that x-height-8px font wont be considered noise
    # they should just have a --small-text or --screen-text option. sad!
    image = image.resize((SCALE*image.width, SCALE*image.height), PIL.Image.ANTIALIAS)
    # TODO try w/o antialias

    image.save(filename_image_out)

    check_call(['tesseract', filename_image_out, filename_text_out, TESSERACT_OPTIONS_FILE], stdout=DEVNULL, stderr=DEVNULL)
    # check_call(['tesseract', filename_image_out, filename_text_out, TESSERACT_OPTIONS_FILE])

    # tesseract keeps adding txt's even if it already ends in '.txt' :v
    filename_text_out += '.txt'

    # # post processing
    os.system("sed -i \"s/’/'/g\" " + filename_text_out)
    os.system("sed -i \"s/‘/'/g\" " + filename_text_out)
    os.system('sed -i \"s/“/\\\"/g\" ' + filename_text_out)
    os.system('sed -i \"s/”/\\\"/g\" ' + filename_text_out)
    # XXXX ^ not having any effect ?




print('done und danna')



# TODO mb improve? (space escape path etc)
os.system('rm ' + TESSERACT_OPTIONS_FILE)







