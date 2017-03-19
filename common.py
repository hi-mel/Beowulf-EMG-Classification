import struct
import pdb

def pack(fmt, *args):
    return struct.pack('<' + fmt, *args)

def unpack(fmt, *args):
    if (fmt == '6B'):
        return struct.unpack('<' + fmt, *('\x00\x00\x00\x00\x00\x00',))

    return struct.unpack('<' + fmt, *args)

def text(scr, font, txt, pos, clr=(255,255,255)):
    scr.blit(font.render(txt, True, clr), pos)
