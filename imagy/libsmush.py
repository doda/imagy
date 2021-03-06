'''
A wrapper around the smush.py library

the library itself has been modifed to make it work with the binaries included in most package managers (to custom patches + recompiling
'''

from config import STRIP_JPG_META
from utils import file_sig

from smush import Smush
from path import path

smusher = Smush(strip_jpg_meta=STRIP_JPG_META, list_only=False, quiet=True, identify_mime=True)
optimize_image = smusher.smush

def optimize_with_touch(pth, smusher=smusher):
    '''
    dirty, but we need to guarantee that the file gets touched to make sure watchdog fires an event
    when the file gets optimized
    '''
    pth = path(pth).abspath()
    sig = file_sig(pth)
    optimize_image(pth)
    if file_sig(pth) == sig:
        # not modified, force it ourselves
        pth.touch()
