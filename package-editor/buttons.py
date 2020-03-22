import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class Buttons(Gtk.VBox):
    def __init__(self, labels, actions):
        Gtk.VBox.__init__(self)
        self.labels = labels
        self.actions = actions
        self.init_and_add_buttons()

    def init_and_add_buttons(self):
        self.inner = Gtk.HBox()
        for i, label in enumerate(self.labels):
            button = Gtk.Button.new_with_label(label)
            self.inner.pack_start(button, True, True, 0)
            button.connect('clicked', self.actions[i])
        self.pack_start(self.inner, False, False, 0)
