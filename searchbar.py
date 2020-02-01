import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk, Gdk, GLib

class AlpsUISearchBar(Gtk.Grid):
    def __init__(self):
        Gtk.Grid.__init__(self)
        self.init_components()
        self.set_border_width(3)
        self.set_vexpand(False)
        self.set_hexpand(True)

    def init_components(self):
        self.search_entry = Gtk.Entry()
        self.search_button = Gtk.Button.new_with_label('Search')

        self.search_entry.set_vexpand(True)
        self.search_entry.set_hexpand(True)
        self.search_entry.set_valign(Gtk.Align.CENTER)
        self.search_button.set_vexpand(False)
        self.search_button.set_hexpand(False)
        self.search_button.set_valign(Gtk.Align.CENTER)
        self.set_column_spacing(3)

        self.attach(self.search_entry, 0, 0, 1, 1)
        self.attach(self.search_button, 1, 0, 1, 1)

        self.search_button.connect('clicked', self.on_search)

    def on_search(self, source):
        self.package_list.set_search_text(self.search_entry.get_text())
        self.category_list.select_search_results()

    def set_category_list(self, category_list):
        self.category_list = category_list

    def set_package_list(self, package_list):
        self.package_list = package_list