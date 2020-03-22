import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from buttons import Buttons
from listboxrowwithdata import ListBoxRowWithData

class DependencyList(Gtk.VBox):
    def __init__(self, parent_window):
        Gtk.VBox.__init__(self)
        self.initialize()
        self.items = list()
        self.parent_window = parent_window

    def initialize(self):
        self.listbox = Gtk.ListBox()
        self.currentitem = Gtk.Entry()
        self.currentitem.set_hexpand(True)
        self.panel = Gtk.HBox()
        self.scrolledwindow = Gtk.ScrolledWindow()
        self.scrolledwindow.add(self.listbox)
        self.listbox.set_vexpand(True)
        self.buttons = Buttons(['Add', 'Delete', 'Update'], [self.on_add, self.on_delete, self.on_update])
        self.buttons.set_vexpand(False)
        self.panel.pack_start(self.currentitem, True, True, 3)
        self.panel.pack_start(self.buttons, False, False, 3)
        self.pack_start(self.scrolledwindow, True, True, 3)
        self.pack_start(self.panel, False, True, 3)

    def set_data(self, dependency_list):
        self.items = dependency_list
        for item in self.items:
            self.listbox.add(ListBoxRowWithData(item))
        self.show_all()
    
    def get_data(self):
        return self.items

    def on_add(self, source):
        pass
    
    def on_delete(self, source):
        pass
    
    def on_update(self, source):
        pass
    