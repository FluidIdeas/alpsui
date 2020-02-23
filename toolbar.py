import api
import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk, Gdk, GLib
from shellwindow import ShellWindow
import subprocess

class AlpsUIToolBar(Gtk.Toolbar):
    def __init__(self, searchbar):
        Gtk.Toolbar.__init__(self)
        self.searchbar = searchbar
        self.init_components()

    def init_components(self):
        self.get_style_context().add_class(Gtk.STYLE_CLASS_PRIMARY_TOOLBAR)
        self.refresh = self.create_tool_button('view-refresh', 'Update Scripts', self.refresh_clicked)
        self.apply = self.create_tool_button('emblem-default', 'Apply Changes', self.apply_clicked)
        self.install_updates = self.create_tool_button('system-software-update', 'Install Updates', self.install_updates_clicked)
        self.settings = self.create_tool_button('emblem-system', 'Preferences', self.settings_clicked)

        self.insert(self.refresh, 0)
        self.insert(self.apply, 1)
        self.insert(self.install_updates, 2)
        self.insert(self.settings, 3)

        self.set_hexpand(False)
        self.set_vexpand(False)

    def layout(self):
        container = Gtk.HBox()
        container.pack_start(self, False, False, 0)
        container.pack_start(self.searchbar, True, True, 0)
        return container

    def create_tool_button(self, icon_name, label, target_function):
        btn = Gtk.ToolButton.new(Gtk.Image.new_from_icon_name(icon_name, Gtk.IconSize.LARGE_TOOLBAR), label)
        btn.set_is_important(True)
        btn.connect('clicked', target_function)
        return btn

    def init_statusbar(self, statusbar):
        self.statusbar = statusbar

    def refresh_clicked(self, source):
        self.refresh.set_sensitive(False)
        api.start_daemon(['ping', 'www.google.com'], self.statusbar,self.enable_refresh)

    def apply_clicked(self, source):
        shell_win = ShellWindow('Installing packages...')
        shell_win.set_mainframe(self.mainframe)
        self.mainframe.hide()
        shell_win.run_process('alps -ni install qt5'.split())
        shell_win.show()

    def install_updates_clicked(self, source):
        pass

    def settings_clicked(self, source):
        pass

    def enable_refresh(self):
        self.refresh.set_sensitive(True)

    def set_mainframe(self, mainframe):
        self.mainframe = mainframe
