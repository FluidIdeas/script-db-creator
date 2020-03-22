import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class ListBoxRowWithData(Gtk.ListBoxRow):
    def __init__(self, data):
        Gtk.ListBoxRow.__init__(self)
        self.data = data
        label = Gtk.Label(data)
        label.set_xalign(0)
        self.add(label)
