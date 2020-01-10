#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk
from packagelist import PackageList

class MainWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title='AryaLinux Packaging System')
        self.packagelist = PackageList(self)
        self.add(self.packagelist.list)

        self.packagelist.add_row([True, 'LibreOffice', '6.3', '6.4', 'Open Source Office Productivity Suite'])

win = MainWindow()
win.connect('destroy', Gtk.main_quit)
win.show_all()
Gtk.main()