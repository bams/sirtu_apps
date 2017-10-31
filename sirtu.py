#!/usr/bin/env python
import ui
import sqlite3
from escpos.printer import Usb

pos_printer = Usb(0x4b43,0x3538,in_ep=0x82,out_ep=0x2)

try:
    if pos_printer:
        print 'initialize pos printer, please wait...'
except:
    raise ValueError('printer doesn\'t exist')
    pass

conn = sqlite3.connect('dbApp')
c = conn.cursor()
c.close()
# print(urwid.version)
