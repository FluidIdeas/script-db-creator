import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class Search(Gtk.HBox):
    def __init__(self):
        Gtk.HBox.__init__(self)
        self.init_components()
        self.add_components()

    def init_components(self):
        self.keywords = Gtk.Entry()
        self.search = Gtk.Button.new_with_label('Search')
        self.search.connect('clicked', self.on_search_clicked)

    def add_components(self):
        self.pack_start(self.keywords, True, True, 3)
        self.pack_start(self.search, False, False, 3)
    
    def set_on_search(self, on_search):
        self.on_search = on_search

    def on_search_clicked(self, event):
        self.on_search(event)

    def get_keywords(self):
        return self.keywords.get_text()