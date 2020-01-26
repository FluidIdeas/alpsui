import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk, Gdk, GLib

class AlpsUIStatusBar(Gtk.HBox):
    def __init__(self):
        Gtk.HBox.__init__(self)
        self.state = False
        self.status_messages = ['Total Packages: ', 'Installed Packages: ', 'Updates: ']
        self.init_components()
        self.layout()

    def init_components(self):
        self.main_status_label = Gtk.Label('AryaLinux Packaging System 1.0')
        self.main_status_label.set_halign(Gtk.Align.START)
        self.status_boxes = list()
        self.status_boxes.append(Gtk.Label(self.status_messages[0]))
        self.status_boxes.append(Gtk.Label(self.status_messages[1]))
        self.status_boxes.append(Gtk.Label(self.status_messages[2]))
        self.secondary_status_label = Gtk.Label('Progress ')
        self.secondary_status_label.set_halign(Gtk.Align.START)
        self.progress = Gtk.ProgressBar()
        self.progress.set_valign(Gtk.Align.CENTER)
        self.progress.set_show_text(False)

    def layout(self):
        self.pack_start(self.main_status_label, True, True, 5)
        self.pack_start(self.status_boxes[0], False, False, 5)
        self.pack_start(self.status_boxes[1], False, False, 5)
        self.pack_start(self.status_boxes[2], False, False, 5)
        self.pack_start(self.secondary_status_label, False, False, 5)
        self.pack_start(self.progress, False, False, 5)
        self.set_border_width(5)

    def pulse(self):
        self.timeout_id = GLib.timeout_add(50, self.on_timeout, None)
        self.state = True

    def on_timeout(self, data):
        self.progress.pulse()
        return self.state

    def stop(self):
        GLib.source_remove(self.timeout_id)
        self.timeout_id = 0
        self.progress.set_fraction(0.0)
        self.state = False

    def set_status_text(self, box_id, text):
        self.status_boxes[box_id].set_text(self.status_messages[box_id] + str(text))
