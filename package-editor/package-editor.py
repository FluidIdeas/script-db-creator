import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from dependencylist import DependencyList

class PackageEditor(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title='AryaLinux Package Database Editor')
        self.init_components()
        self.add_components()

    def init_components(self):
        self.the_box = Gtk.VBox()
        self.name = Gtk.Entry()
        self.version = Gtk.Entry()
        self.url = Gtk.Entry()
        self.description = Gtk.TextView()
        self.tarball = Gtk.Entry()
        self.commands = Gtk.TextView()
        self.dependencies = Gtk.HBox()
        self.required = DependencyList()
        self.recommended = DependencyList()
        self.optional = DependencyList()
        self.section = Gtk.Entry()
        self.downloadUrls = DependencyList()
        

        self.labels = list()
        self.labels.append(Gtk.Label('Name', xalign=0))
        self.labels.append(Gtk.Label('Section', xalign=0))
        self.labels.append(Gtk.Label('URL', xalign=0))
        self.labels.append(Gtk.Label('Version', xalign=0))
        self.labels.append(Gtk.Label('Download URLs', xalign=0))
        self.labels.append(Gtk.Label('Commands', xalign=0))
        self.labels.append(Gtk.Label('Dependencies', xalign=0))

    def add_components(self):
        self.the_box.pack_start(self.labels[0], False, False, 0)
        self.the_box.pack_start(self.name, False, True, 0)
        self.the_box.pack_start(self.labels[1], False, False, 0)
        self.the_box.pack_start(self.section, False, True, 0)
        self.the_box.pack_start(self.labels[2], False, False, 0)
        self.the_box.pack_start(self.url, False, True, 0)
        self.the_box.pack_start(self.labels[3], False, False, 0)
        self.the_box.pack_start(self.version, False, True, 0)
        self.the_box.pack_start(self.labels[4], False, False, 0)
        self.the_box.pack_start(self.downloadUrls, False, True, 0)
        self.the_box.pack_start(self.labels[5], False, False, 0)
        self.the_box.pack_start(self.commands, True, True, 0)

        self.add(self.the_box)

    def on_new(self, source, event):
        pass

    def on_previous(self, source, event):
        pass

    def on_next(self, source, event):
        pass

    def on_save(self, source, event):
        pass


window = PackageEditor()
window.connect('destroy', Gtk.main_quit)
window.show_all()
Gtk.main()