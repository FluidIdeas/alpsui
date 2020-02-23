#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk
from packagelist import PackageList
from category_list  import Categories
from filters import Filters
from menubar import AlpsUIMenuBar
from searchbar import AlpsUISearchBar
from toolbar import AlpsUIToolBar
from statusbar import AlpsUIStatusBar
import api

class MainWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title='AryaLinux Packaging System')
        self.current_filter = None
        self.current_category = None

        self.init_components()
        self.do_layout()
        self.maximize()

    def init_components(self):
        self.packages = api.get_packages()
        (total, installed, updates) = api.get_stats(self.packages)
        self.categories = api.get_sections(self.packages)

        #self.main_menu = AlpsUIMenuBar()
        self.searchbar = AlpsUISearchBar()
        self.toolbar = AlpsUIToolBar(self.searchbar)
        self.toolbar_container = self.toolbar.layout()
        self.packagelist = PackageList(self)
        self.filters = Filters(self.on_filter)
        self.scrolledwindow = self.wrap_scrollbar(self.packagelist.list)
        self.statusbar = AlpsUIStatusBar()

        self.category_list = Categories(self.categories, self.on_category_change)
        self.packagelist.set_packages(self.packages)
        self.toolbar.init_statusbar(self.statusbar)
        self.toolbar.set_mainframe(self)

        self.searchbar.set_category_list(self.category_list)
        self.searchbar.set_package_list(self.packagelist)

        self.statusbar.set_status_text(0, total)
        self.statusbar.set_status_text(1, installed)
        self.statusbar.set_status_text(2, updates)

    def wrap_scrollbar(self, child):
        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_hexpand(True)
        scrolledwindow.set_vexpand(True)
        scrolledwindow.add(child)
        return scrolledwindow

    def do_layout(self):
        self.parent_pane = Gtk.VBox()
        self.main_paned = Gtk.Paned.new(Gtk.Orientation.HORIZONTAL)
        self.right_paned = Gtk.Paned.new(Gtk.Orientation.VERTICAL)
        self.left_panel = Gtk.VBox()
        self.left_panel.pack_start(self.category_list, True, True, 0)
        self.left_panel.pack_start(self.filters, False, False, 5)
        self.main_paned.add1(self.left_panel)
        self.main_paned.add2(self.right_paned)
        self.right_paned.add1(self.scrolledwindow)
        #self.parent_pane.pack_start(self.main_menu, False, False, 0)
        self.parent_pane.pack_start(self.toolbar_container, False, False, 0)
        self.parent_pane.pack_start(self.main_paned, True, True, 0)
        self.parent_pane.pack_start(self.statusbar, False, False, 0)
        self.add(self.parent_pane)

    def on_category_change(self, a, b):
        selection = self.category_list.get_selection()
        category = selection.data
        if category == 'All':
            category = None
        self.current_category = category
        self.packagelist.clear_packages()
        self.packagelist.set_packages(self.packages, self.current_category, self.current_filter)

    def on_filter(self, the_filter):
        self.current_filter = the_filter
        self.packagelist.clear_packages()
        self.packagelist.set_packages(self.packages, self.current_category, self.current_filter)

win = MainWindow()
win.connect('destroy', Gtk.main_quit)
win.set_icon_name("system-software-install")
win.show_all()
win.set_size_request(1000, 600)
win.main_paned.set_position(250)
Gtk.main()