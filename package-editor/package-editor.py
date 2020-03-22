import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from dependencylist import DependencyList
import json
from search import Search
from buttons import Buttons

class PackageEditor(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title='AryaLinux Package Database Editor')
        self.init_components()
        self.add_components()
        self.set_border_width(6)

    def init_components(self):
        self.searchbar = Search()
        self.searchbar.set_on_search(self.on_search)
        self.buttonbar = Buttons(['Generate', 'Previous', 'Next'], [self.generate, self.on_previous, self.on_next])
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

        self.the_box.pack_start(self.searchbar, False, False, 3)

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

        self.the_box.pack_start(self.buttonbar, False, False, 3)

        self.add(self.the_box)

    def on_new(self, source):
        pass

    def on_previous(self, event):
        if self.current_index > 0:
            self.current_index = self.current_index - 1
            self.set_data(self.packages[self.current_index])

    def on_next(self, event):
        if self.current_index < len(self.packages) - 1:
            self.current_index = self.current_index + 1
            self.set_data(self.packages[self.current_index])

    def on_save(self, event):
        pass

    def set_data(self, package):
        self.current_package = package
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

    def set_packages(self, packages):
        self.packages = packages
        self.current_index = 0
        self.set_data(self.packages[0])

    def on_search(self, event):
        keywords = self.searchbar.get_keywords()
        result = 0
        result_package = None
        for i, package in enumerate(packages):
            if package['name'] == keywords:
                result = i
                result_package = package
                break
        self.set_data(result_package)
        self.current_index = result

    def generate(self, event):
        package = self.current_package
        with open('/home/chandrakant/' + package['name'] + '.sh', 'w') as fp:
            fp.write('#!/bin/bash\n')
            fp.write('set -e\n')
            fp.write('set +h\n\n')
            fp.write('. /etc/alps/alps.conf\n')
            fp.write('. /etc/alps/directories.conf\n')
            fp.write('. /var/lib/alps/functions\n\n')
            for dep in package['dependencies']['required']:
                fp.write('#REQ:' + dep + '\n')
            for dep in package['dependencies']['recommended']:
                fp.write('#REC:' + dep + '\n')
            fp.write('\n')
            fp.write('NAME=' + package['name'] + '\n')
            fp.write('SECTION=' + package['section'] + '\n')
            if '\'' in package['description']:
                fp.write('DESCRIPTION=\"' + package['description'] + '\"\n')
            else:
                fp.write('DESCRIPTION=\'' + package['description'] + '\'\n')
            fp.write('URL=' + package['url'] + '\n\n')
            fp.write('cd $SOURCE_DIR' + '\n\n')
            for url in package['downloadUrls']:
                fp.write('wget -nc ' + url + '\n')
            fp.write('TARBALL=$(echo $URL | rev | cut -d/ -f1 | rev)' + '\n')
            fp.write('unzip_file $TARBALL' + '\n')
            for cmd in package['commands']:
                fp.write(cmd + '\n')
            

def load_packages(packagedb_path):
    with open(packagedb_path, 'r') as fp:
        packages = json.load(fp)
        return packages

if __name__ == "__main__":
    packages = load_packages('../packages.json')
    window = PackageEditor()
    window.set_packages(packages)
    window.connect('destroy', Gtk.main_quit)
    window.show_all()
    Gtk.main()