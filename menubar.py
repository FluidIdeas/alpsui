import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk, GLib, Gdk

class AlpsUIMenuBar(Gtk.MenuBar):
    def __init__(self):
        Gtk.MenuBar.__init__(self)
        self.init_menus()

    def init_menus(self):
        self.append(self.create_menu('_Packages', ['_Update Scripts', '_Apply Changes', '', '_Install Updates', '', '_Exit'], [
            self.do_nothing,
            self.do_nothing,
            None,
            self.do_nothing,
            None,
            self.do_nothing]))
        self.append(self.create_menu('_Settings', ['_Options'], [self.do_nothing]))
        self.append(self.create_menu('_Help', ['_About'], [self.do_nothing]))

    def create_menu_item(self, label, action_handler):
        item = Gtk.MenuItem.new_with_mnemonic(label)
        if action_handler != None:
            item.connect('activate', action_handler)
        return item

    def create_menu(self, label, item_labels, action_handlers):
        menuitem = self.create_menu_item(label, None)
        menu = Gtk.Menu()
        for i in range(len(item_labels)):
            if item_labels[i] == '':
                item = Gtk.SeparatorMenuItem()
            else:
                item = self.create_menu_item(item_labels[i], action_handlers[i])
            menu.append(item)
        menuitem.set_submenu(menu)
        return menuitem

    def do_nothing(self, source):
        pass