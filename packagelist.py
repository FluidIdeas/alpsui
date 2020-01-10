import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk

class PackageList:
    def __init__(self, parent):
        self.parent_window = parent
        self.model = Gtk.ListStore(bool, str, str, str, str)
        self.list = Gtk.TreeView.new()
        self.list.set_model(self.model)

        self.append_columns([
            self.create_bool_column('Installed', 0),
            self.create_string_column('Name', 1),
            self.create_string_column('Installed Version', 2),
            self.create_string_column('Available Version', 3),
            self.create_string_column('Description', 4)
        ])

        self.model_copy = Gtk.ListStore(bool, str, str, str, str)

    def add_row(self, row):
        self.model.append(row)
        self.model_copy.append(row)

    def append_columns(self, column_list):
        for column in column_list:
            self.list.append_column(column)

    def create_string_column(self, title, column):
        return Gtk.TreeViewColumn(title, Gtk.CellRendererText(), text=column)

    def create_bool_column(self, title, column):
        cell_renderer = Gtk.CellRendererToggle()
        cell_renderer.set_property('activatable', True)
        cell_renderer.connect('toggled', self.on_toggle)
        return Gtk.TreeViewColumn(title, cell_renderer, active=column)

    def on_toggle(self, cell, path):
        if path is not None:
            it = self.model.get_iter(path)
            it1 = self.model_copy.get_iter(path)
            if self.confirm_change(self.model[it][1], self.model[it][0], self.model_copy[it1][0]):
                self.model[it][0] = not self.model[it][0]

    def confirm_change(self, name, status, origin_status):
        if not status:
            if not origin_status:
                msg = 'install ' + name + ' and all its dependencies?'
            else:
                return True
        else:
            msg = 'remove ' + name
        dialog = Gtk.MessageDialog(
            self.parent_window, 0, Gtk.MessageType.QUESTION, Gtk.ButtonsType.YES_NO,
            'Are you sure you want to ' + msg)
        response = dialog.run()
        dialog.destroy()
        if response == Gtk.ResponseType.YES:
            return True
        else:
            return False