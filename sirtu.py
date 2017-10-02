#!/usr/bin/env python
import ui
import sqlite3
conn = sqlite3.connect('dbApp')
c = conn.cursor()
c.close()
# print(urwid.version)
