import os, sys, glob
from subprocess import DEVNULL, STDOUT, check_call
from collections import defaultdict
from html import escape
import json

import argparse



parser = argparse.ArgumentParser(description='gay')
parser.add_argument('--image-dir', dest='image_dir',
                    default='/home/jan/Music/pics/hxh-textposts/')
args = parser.parse_args()

IMG_DIR = args.image_dir



web_dir = IMG_DIR + 'webpage/'

check_call(['mkdir', '-p', web_dir])

d = dict()



files = list(sorted(glob.iglob(IMG_DIR + '*.png'), key = lambda x: x[x.index('tumblr_'):]))

# for filename_image_in in glob.iglob(IMG_DIR + '*.png'):
# for filename_image_in in [IMG_DIR + 'http://68.media.tumblr.com/fa0e4c160d0319bc7ced162425cebb9d/tumblr_o4uvc2Ed981ue484to1_1280.png'.replace('/', '+').replace(':', '-')]:

for i in range(len(files)):

    filename_image_in = files[i]

    # filename_image_in  = IMG_DIR + filename_image_in
    s = IMG_DIR + 'output/' + filename_image_in[len(IMG_DIR):]
    filename_text_out  = s

    # url = filename_image_in[len(IMG_DIR):].replace('+', '/').replace('-', ':')
    url = filename_image_in[len(IMG_DIR):]

    if '1_' not in url:
        continue

    d[url] = {'urls': [], 'ocr': ''}

    # this is complicated. reason:
    # every POST (i) may have multiple IMAGES (k) which might have multiple TEXTBOXES (j)
    for k in range(10):

        if i+k >= len(files) or ('1_' in files[i+k] and k != 0):
            break

        u = files[i+k][len(IMG_DIR):]

        d[url]['urls'].append(u)

        filename_text_out  = IMG_DIR + 'output/' + u

        for j in range(10):
            if os.path.isfile(filename_text_out + '.' + str(j) + '.png.txt'):
                with open(filename_text_out + '.' + str(j) + '.png.txt') as f:
                    d[url]['ocr'] += f.read().strip() + '\n'
        d[url]['ocr'] = d[url]['ocr'].strip()

        d[url]['ocr'] += '\n\n'

    d[url]['ocr'] = d[url]['ocr'].strip()

    if not d[url]['ocr']:
        d[url]['ocr'] = '[no text]'

d2 = dict()

for k in d.keys():
    k2 = k.replace('+', '/').replace('-', ':')
    d2[k2] = dict()
    d2[k2]['urls'] = [u.replace('+', '/').replace('-', ':') for u in d[k]['urls']]
    d2[k2]['ocr']  = d[k]['ocr']

d = d2



with open('template.html') as t:
    with open(web_dir + 'index.html', 'w') as f:

        for line in t:

            if line.strip() != '$PYDATA':
                f.write(line)
                continue

            f.write('<table>\n')

            for url in sorted(d, key = lambda x: x[x.index('tumblr_'):]):
                f.write('<tr>')
                f.write('<td>')
                s = '<br/>'.join('<a href="'+escape(u)+'">'+escape(u)+'</a>' for u in d[url]['urls'])
                f.write(s)
                # f.write('<img src="'+escape(url)+'">')  # don't do this tho
                f.write('</td>')
                f.write('<td>')
                f.write(escape(d[url]['ocr']).replace('\n', '<br/>'))
                f.write('</td>')
                f.write('</tr>\n')

            f.write('</table>\n')



# TODO better search

out = []
for k in d:
    # will be escaped in the js, hopefully
    out.append({ 'urls': d[k]['urls'], 'ocr': d[k]['ocr'] })

with open(web_dir + 'database.json', 'w') as f:
    json.dump(out, f)


print('done pt 3')

