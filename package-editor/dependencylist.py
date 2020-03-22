import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from buttons import Buttons

class DependencyList(Gtk.VBox):
    def __init__(self):
        Gtk.VBox.__init__(self)
        self.initialize()

    def initialize(self):
        self.listbox = Gtk.ListBox()
        self.listbox.set_vexpand(True)
        self.buttons = Buttons(['Add', 'Delete', 'Update'], [self.on_add, self.on_delete, self.on_update])
        self.buttons.set_vexpand(False)
        self.pack_start(self.listbox, True, True, 0)
        self.pack_start(self.buttons, False, False, 0)

    def on_add(self, source):
        pass
    
    def on_delete(self, source):
        pass
    
    def on_update(self, source):
        pass
    