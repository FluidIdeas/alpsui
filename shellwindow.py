#!/usr/bin/env python3

import subprocess
import signal
import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk, Gdk, GLib, Gio
from streamtextbuffer import StreamTextBuffer

class ShellWindow(Gtk.Window):
    def __init__(self, title):
        Gtk.Window.__init__(self, title=title)
        self.init_components()
        self.add_components()
    
    def init_components(self):
        self.root_panel = Gtk.VBox()
        self.scrolled_window = Gtk.ScrolledWindow()
        self.log_text_area = Gtk.TextView()
        self.scrolled_window.add(self.log_text_area)
        self.buffer = StreamTextBuffer()
        self.log_text_area.set_buffer(self.buffer)
        self.close_button = Gtk.Button('Close')
        self.close_button.connect('clicked', self.on_close)
        self.log_text_area.set_sensitive(False)

    def add_components(self):
        self.add(self.root_panel)
        self.root_panel.pack_start(self.scrolled_window, True, True, 0)
        self.root_panel.pack_start(self.close_button, False, False, 0)
        self.close_button.set_hexpand(False)

    def run_process(self, commands):
        self.subprocess = subprocess.Popen(commands, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.buffer.bind_subprocess(self.subprocess)

    def on_close(self, source):
        returncode = self.subprocess.poll()
        if returncode == None:
            response = self.prompt("Are you sure you want to Close?", "If you cancel the installation before it is complete, the system may end up in an unusable state.")
            self.prompt_dialog.destroy()
            if response == Gtk.ResponseType.OK:
                self.subprocess.send_signal(signal.SIGINT)
                self.destroy()
                self.mainframe.show_all()
        else:
            self.destroy()
            self.mainframe.show_all()

    def show(self):
        screen = Gdk.Screen.get_default()
        self.set_size_request(screen.get_width()/2.5, screen.get_height()/2.5)
        self.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
        self.set_border_width(5)
        self.show_all()

    def set_mainframe(self, mainframe):
        self.mainframe = mainframe

    def prompt(self, heading, message):
        dialog = Gtk.Dialog(heading, self.mainframe, 0, (Gtk.STOCK_YES, Gtk.ResponseType.OK, Gtk.STOCK_NO, Gtk.ResponseType.CANCEL))
        dialog.set_default_size(150, 100)
        label = Gtk.Label(message)
        dialog.get_content_area().add(label)
        dialog.show_all()
        self.prompt_dialog = dialog
        return dialog.run()