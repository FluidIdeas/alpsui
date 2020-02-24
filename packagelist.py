import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk

class PackageList:
    def __init__(self, parent):
        self.parent_window = parent
        self.model = Gtk.ListStore(bool, str, str, str, str, bool)
        self.list = Gtk.TreeView.new()
        self.list.set_model(self.model)
        self.keywords = ''

        self.append_columns([
            self.create_bool_column('Installed', 0, 5),
            self.create_string_column('Name', 1),
            self.create_string_column('Installed Version', 2),
            self.create_string_column('Available Version', 3),
            self.create_string_column('Description', 4)
        ])

        self.model_copy = Gtk.ListStore(bool, str, str, str, str, bool)
        self.selections = list()

    def add_row(self, row):
        self.model.append(row)
        self.model_copy.append(row)

    def append_columns(self, column_list):
        for column in column_list:
            self.list.append_column(column)

    def create_string_column(self, title, column):
        return Gtk.TreeViewColumn(title, Gtk.CellRendererText(), text=column)

    def create_bool_column(self, title, column, column1):
        cell_renderer = Gtk.CellRendererToggle()
        cell_renderer.connect('toggled', self.on_toggle)
        return Gtk.TreeViewColumn(title, cell_renderer, active=column, activatable=column1)

    def on_toggle(self, cell, path):
        if path is not None:
            it = self.model.get_iter(path)
            it1 = self.model_copy.get_iter(path)
            if self.confirm_change(self.model[it][1], self.model[it][0], self.model_copy[it1][0]):
                self.model[it][0] = not self.model[it][0]

    def confirm_change(self, name, status, origin_status):
        print(status)
        print(origin_status)
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
            self.selections.append(name)
            return True
        else:
            self.selections.remove(name)
            return False

    def clear_packages(self):
        self.model.clear()
        self.model_copy.clear()

    def append_package(self, package):
        self.add_row([package['status'], package['name'], package['version'], package['available_version'], package['description'], not package['status']])
    
    def set_packages(self, packages, section=None, the_filter=None):
        for package in packages:
            if self.has_to_be_listed(package, section, the_filter):
                self.append_package(package)

    def has_to_be_listed(self, package, section=None, the_filter=None):
        if section == 'Search Results':
            if self.keywords == '':
                return False
            words = self.keywords.split()
            status = False
            for word in words:
                if word in package['name'] or (package['description'] != None and word in package['description']) or (package['version'] != None and word in package['version']):
                    status = True
                    break
            return status
        if the_filter == None and section == None:
            return True
        else:
            is_in_section = False
            if section == None:
                is_in_section = True
            elif package['section'] == section:
                is_in_section = True

            is_to_be_included = False
            if the_filter == None:
                is_to_be_included = True
            elif the_filter == 1 and package['status'] == True:
                is_to_be_included = True
            elif the_filter == 2 and package['status'] == False:
                is_to_be_included = True
            elif the_filter == 3 and package['version'] != package['available_version'] and package['version'] != None:
                is_to_be_included = True
            return is_in_section and is_to_be_included

    def set_search_text(self, keywords):
        self.keywords = keywords

    def get_selections(self):
        return self.selections
