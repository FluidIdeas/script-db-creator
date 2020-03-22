import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from dependencylist import DependencyList
import json

class PackageEditor(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title='AryaLinux Package Database Editor')
        self.init_components()
        self.add_components()
        self.set_border_width(6)

    def init_components(self):
        self.the_box = Gtk.VBox()
        self.name = Gtk.Entry()
        self.version = Gtk.Entry()
        self.url = Gtk.Entry()
        self.description = Gtk.TextView()
        self.tarball = Gtk.Entry()
        self.commands = Gtk.TextView()
        self.commands_buffer = self.commands.get_buffer()
        self.dependencies = Gtk.HBox()
        self.required = DependencyList(self)
        self.recommended = DependencyList(self)
        self.optional = DependencyList(self)
        self.section = Gtk.Entry()
        self.downloadUrls = DependencyList(self)
        

        self.labels = list()
        for label_text in ['Name', 'Section', 'URL', 'Version', 'Download URLs', 'Commands', 'Dependencies']:
            label = Gtk.Label.new(label_text)
            label.set_xalign(0.0)
            self.labels.append(label)

        self.scrolledwindow1 = Gtk.ScrolledWindow()

        self.panel1 = Gtk.VBox()
        self.panel2 = Gtk.VBox()
        self.panel3 = Gtk.HBox()
        self.panel4 = Gtk.VBox()
        self.panel5 = Gtk.VBox()
        self.panel6 = Gtk.HBox()
        

    def add_components(self):
        self.scrolledwindow1.add(self.commands)

        self.dependencies.pack_start(self.required, True, True, 3)
        self.dependencies.pack_start(self.recommended, True, True, 3)
        self.dependencies.pack_start(self.optional, True, True, 3)

        self.panel1.pack_start(self.labels[0], False, False, 3)
        self.panel1.pack_start(self.name, False, True, 3)
        self.panel1.pack_start(self.labels[1], False, False, 3)
        self.panel1.pack_start(self.section, False, True, 3)
        self.panel1.pack_start(self.labels[4], False, False, 3)
        self.panel1.pack_start(self.downloadUrls, True, True, 3)

        self.panel2.pack_start(self.labels[2], False, False, 3)
        self.panel2.pack_start(self.url, False, True, 3)
        self.panel2.pack_start(self.labels[3], False, False, 3)
        self.panel2.pack_start(self.version, False, True, 3)
        self.panel2.pack_start(self.labels[5], False, False, 3)
        self.panel2.pack_start(self.scrolledwindow1, True, True, 3)

        self.panel3.pack_start(self.panel1, True, True, 3)
        self.panel3.pack_start(self.panel2, True, True, 3)

        self.the_box.pack_start(self.panel3, True, True, 3)

        self.the_box.pack_start(self.labels[6], False, False, 3)
        self.the_box.pack_start(self.dependencies, True, True, 3)

        self.add(self.the_box)

    def on_new(self, source, event):
        pass

    def on_previous(self, source, event):
        pass

    def on_next(self, source, event):
        pass

    def on_save(self, source, event):
        pass

    def set_data(self, package):
        self.name.set_text(package['name'])
        if package['version'] != None:
            self.version.set_text(package['version'])
        if package['url'] != None:
            self.url.set_text(package['url'])
        if package['section'] != None:
            self.section.set_text(package['section'])
        self.commands_buffer.set_text('\n'.join(package['commands']))
        self.downloadUrls.set_data(package['downloadUrls'])
        self.required.set_data(package['dependencies']['required'])
        self.recommended.set_data(package['dependencies']['recommended'])
        self.optional.set_data(package['dependencies']['optional'])

def load_packages(packagedb_path):
    with open(packagedb_path, 'r') as fp:
        packages = json.load(fp)
        return packages

if __name__ == "__main__":
    packages = load_packages('../packages.json')
    window = PackageEditor()
    window.connect('destroy', Gtk.main_quit)
    window.show_all()
    window.set_data(packages[59])
    Gtk.main()