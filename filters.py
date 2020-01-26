import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class Filters(Gtk.VBox):
    def __init__(self, filter_function):
        Gtk.VBox.__init__(self)
        self.filter_function = filter_function
        self.components = list()
        self.init_components()
    
    def init_components(self):
        self.none = Gtk.ToggleButton("All Packages")
        self.installed = Gtk.ToggleButton("Installed Packages")
        self.not_installed = Gtk.ToggleButton("Available Packages")
        self.to_be_updated = Gtk.ToggleButton("Packages to be updated")

        self.components.append(self.none)
        self.components.append(self.installed)
        self.components.append(self.not_installed)
        self.components.append(self.to_be_updated)

        self.pack_start(self.none, True, True, 3)
        self.pack_start(self.installed, True, True, 3)
        self.pack_start(self.not_installed, True, True, 3)
        self.pack_start(self.to_be_updated, True, True, 3)

        self.set_border_width(5)

        self.current = self.none
        self.current.set_active(True)

        self.none.connect('toggled', self.on_none_toggle)
        self.installed.connect('toggled', self.on_installed_toggle)
        self.not_installed.connect('toggled', self.on_not_installed_toggle)
        self.to_be_updated.connect('toggled', self.on_to_be_updated_toggle)

    def on_none_toggle(self, event_source):
        if event_source.get_active() == False:
            return
        if self.current != event_source:
            self.current.set_active(False)
        self.current = self.none
        self.filter_function(None)

    def on_installed_toggle(self, event_source):
        if event_source.get_active() == False:
            return
        if self.current != event_source:
            self.current.set_active(False)
        self.current = self.installed
        self.filter_function(1)

    def on_not_installed_toggle(self, event_source):
        if event_source.get_active() == False:
            return
        if self.current != event_source:
            self.current.set_active(False)
        self.current = self.not_installed
        self.filter_function(2)

    def on_to_be_updated_toggle(self, event_source):
        if event_source.get_active() == False:
            return
        if self.current != event_source:
            self.current.set_active(False)
        self.current = self.to_be_updated
        self.filter_function(3)
