#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk
from packagelist import PackageList
from category_list  import Categories
from filters import Filters
import api

class MainWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title='AryaLinux Packaging System')
        self.current_filter = None
        self.current_category = None
        self.packagelist = PackageList(self)
        self.filters = Filters(self.on_filter)
        self.scrolledwindow = Gtk.ScrolledWindow()
        self.scrolledwindow.set_hexpand(True)
        self.scrolledwindow.set_vexpand(True)
        self.scrolledwindow.add(self.packagelist.list)
        self.packages = api.get_packages()
        self.do_layout()
        self.packagelist.set_packages(self.packages)
        self.maximize()

    def create_tool_button(self, icon_name, label, target_function):
        btn = Gtk.ToolButton.new(Gtk.Image.new_from_icon_name(icon_name, Gtk.IconSize.LARGE_TOOLBAR), label)
        btn.set_is_important(True)
        btn.connect('clicked', target_function)
        return btn
    
    def create_search_bar(self):
        self.search_entry = Gtk.Entry()
        self.search_entry.set_vexpand(True)
        self.search_entry.set_hexpand(True)
        self.search_entry.set_valign(Gtk.Align.CENTER)
        self.search_button = Gtk.Button.new_with_label('Search')
        self.search_button.set_vexpand(False)
        self.search_button.set_hexpand(False)
        self.search_button.set_valign(Gtk.Align.CENTER)
        search_panel = Gtk.Grid()
        search_panel.set_border_width(3)
        search_panel.set_column_spacing(3)
        search_panel.attach(self.search_entry, 0, 0, 1, 1)
        search_panel.attach(self.search_button, 1, 0, 1, 1)
        search_panel.set_vexpand(False)
        search_panel.set_hexpand(True)
        return search_panel

    def create_toolbar(self):
        container = Gtk.VBox()
        inner_container = Gtk.HBox()
        toolbar = Gtk.Toolbar()
        toolbar.get_style_context().add_class(Gtk.STYLE_CLASS_PRIMARY_TOOLBAR)
        refresh = self.create_tool_button('view-refresh', 'Update Scripts', self.refresh_clicked)
        apply = self.create_tool_button('emblem-default', 'Apply Changes', self.apply_clicked)
        install_updates = self.create_tool_button('system-software-update', 'Install Updates', self.install_updates_clicked)
        toolbar.insert(refresh, 0)
        toolbar.insert(apply, 1)
        toolbar.insert(install_updates, 2)
        refresh.show()
        toolbar.set_hexpand(False)
        toolbar.set_vexpand(False)
        self.main_menu = api.create_main_menu()
        container.pack_start(self.main_menu, False, False, 0)
        inner_container.pack_start(toolbar, False, False, 0)
        inner_container.pack_start(self.create_search_bar(), True, True, 0)
        container.pack_start(inner_container, True, True, 0)
        return container

    def refresh_clicked(self, a=None, b=None, c=None):
        print('Refresh Clicked...')

    def apply_clicked(self, a=None, b=None, c=None):
        print('Apply Clicked...')

    def install_updates_clicked(self, a=None, b=None, c=None):
        print('Install Updates Clicked...')
    
    def do_layout(self):
        self.parent_pane = Gtk.VBox()
        self.main_paned = Gtk.Paned.new(Gtk.Orientation.HORIZONTAL)
        self.right_paned = Gtk.Paned.new(Gtk.Orientation.VERTICAL)
        self.right_panel = Gtk.VBox()
        self.categories = api.get_sections(self.packages)
        self.category_list = Categories(self.categories, self.on_category_change)
        self.right_panel.pack_start(self.category_list, True, True, 0)
        self.right_panel.pack_start(self.filters, False, False, 5)
        self.main_paned.add1(self.right_panel)
        self.main_paned.add2(self.right_paned)
        self.right_paned.add1(self.scrolledwindow)
        self.toolbar = self.create_toolbar()
        self.parent_pane.pack_start(self.toolbar, False, False, 0)
        self.parent_pane.pack_start(self.main_paned, True, True, 0)
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