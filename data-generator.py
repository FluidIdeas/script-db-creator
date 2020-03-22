#!/usr/bin/env python3

from bs4 import BeautifulSoup
import json

invalid_packages = list()

def get_links(index_path):
    root_dir = '/'.join(index_path.split('/')[0:-1])
    links = list()
    with open(index_path, 'rb') as fp:
        data = fp.read()
        doc = BeautifulSoup(data, features='lxml')
        anchors = doc.select('li.sect1 a')
        for anchor in anchors:
            links.append(root_dir + '/' + anchor.attrs['href'])
    return links

def get_name(page_path):
    parts = page_path.split('/')
    filename = parts[-1]
    return filename.replace('.html', '')

def get_download_urls(doc):
    anchors = doc.select('div.itemizedlist ul.compact li.listitem p a.ulink')
    urls = list()
    for anchor in anchors:
        urls.append(anchor.attrs['href'])
    return urls

def get_unique_urls(urls):
    unique = list()
    for url in urls:
        found = False
        for u in unique:
            if url.split('/')[-1] == u.split('/')[-1]:
                found = True
        if not found:
            unique.append(url)
    return unique

def get_description(doc):
    desc_p = doc.select('div.package p')
    desc = None
    for p in desc_p:
        desc = p.text
        break
    if desc != None:
        desc_lines = desc.split('\n')
        processed_lines = list()
        for desc_line in desc_lines:
            processed_lines.append(desc_line.strip())
        return ' '.join(processed_lines).strip()
    else:
        return None

def get_section(page_path):
    parts = page_path.split('/')
    return parts[-2]

def get_tarball(url):
    if url != None:
        return url.split('/')[-1]
    else:
        return None

def version_tgz(tarball):
    if tarball.startswith('LVM2'):
        return tarball[5:tarball.index('.tgz')]
    else:
        return tarball

def version_bz2(tarball):
    if tarball.startswith('boost'):
        return tarball[6: tarball.index('.tar.bz2')]
    elif tarball.startswith('p7zip'):
        return tarball[tarball.index('_') + 1:tarball.index('_src')]
    elif tarball.startswith('lynx'):
        return tarball.replace('lynx', '').replace('.tar.bz2', '')
    else:
        return tarball[tarball.rindex('-') + 1:tarball.index('.tar.bz2')]

def version_xz(tarball):
    if '.orig' in tarball:
        return tarball[tarball.index('_') + 1: tarball.index('.orig')]
    elif tarball.startswith('librep'):
        return tarball.replace('librep_', '').replace('.tar.xz', '')
    elif tarball.startswith('sawfish'):
        return tarball.replace('sawfish_', '').replace('.tar.xz', '')
    else:
        return tarball[tarball.rindex('-') + 1:tarball.index('.tar.xz')]

def version_gz(tarball):
    if tarball.startswith('libpaper') or tarball.startswith('lsof'):
        return tarball[tarball.index('_') + 1: tarball.index('.tar.gz')]
    elif '.orig.tar' in tarball:
        return tarball[tarball.index('_') + 1: tarball.index('.orig')]
    elif tarball.startswith('unzip'):
        return tarball.replace('.tar.gz', '').replace('unzip', '')
    elif tarball.startswith('zip'):
        return tarball.replace('.tar.gz', '').replace('zip', '')
    elif tarball.startswith('expect'):
        return tarball.replace('expect', '').replace('.tar.gz', '')
    elif tarball.startswith('wireless_tools.'):
        return tarball.replace('wireless_tools.', '').replace('.tar.gz', '')
    elif tarball.startswith('sendmail.'):
        return tarball.replace('sendmail.', '').replace('.tar.gz', '')
    elif tarball.startswith('LMDB_'):
        return tarball.replace('LMDB_', '').replace('.tar.gz', '')
    elif tarball.startswith('x265_'):
        return tarball.replace('x265_', '').replace('.tar.gz', '')
    else:
        return tarball[tarball.rindex('-') + 1:tarball.index('.tar.gz')]

def get_version(tarball):
    if tarball != None:
        if tarball.endswith('.tar.gz'):
            return version_gz(tarball)
        elif tarball.endswith('.tar.bz2'):
            return version_bz2(tarball)
        elif tarball.endswith('.tar.xz'):
            return version_xz(tarball)
        elif tarball.endswith('.tgz'):
            return version_tgz(tarball)
        else:
            return tarball
    else:
        return None

def get_commands(doc):
    commands = list()
    kbds = doc.select('pre kbd.command')
    for kbd in kbds:
        if 'userinput' in kbd.parent.attrs['class']:
            commands.append(kbd.text)
        else:
            commands.append('as_root ' + kbd.text)
    return commands

def get_dependencies(doc):
    dependencies = dict()
    dependencies['required'] = list()
    dependencies['recommended'] = list()
    dependencies['optional'] = list()
    required_deps = doc.select('p.required a.xref')
    for required in required_deps:
        if not required.attrs['href'].startswith('http'):
            dependencies['required'].append(required.attrs['href'].split('/')[-1].replace('.html', ''))
    recommended_deps = doc.select('p.recommended a.xref')
    for recommended in recommended_deps:
        if not recommended.attrs['href'].startswith('http'):
            dependencies['recommended'].append(recommended.attrs['href'].split('/')[-1].replace('.html', ''))
    optional_deps = doc.select('p.optional a.xref')
    for optional in optional_deps:
        if not optional.attrs['href'].startswith('http'):
            dependencies['optional'].append(optional.attrs['href'].split('/')[-1].replace('.html', ''))
    return dependencies

def parse_page(page_path):
    with open(page_path, 'rb') as fp:
        data = fp.read()
        doc = BeautifulSoup(data, features='lxml')
        package = dict()
        package['name'] = get_name(page_path)
        package['description'] = get_description(doc)
        package['section'] = get_section(page_path)
        package['downloadUrls'] = get_unique_urls(get_download_urls(doc))
        package['commands'] = get_commands(doc)
        package['url'] = None
        if len(package['downloadUrls']) > 0:
            package['url'] = package['downloadUrls'][0]
        package['tarball'] = get_tarball(package['url'])
        package['version'] = get_version(package['tarball'])
        package['dependencies'] = get_dependencies(doc)
        return package

def parse_section(module_name, section, doc):
    package = dict()
    prefix = ''
    if section == 'Python Module':
        prefix = 'python-modules#'
    elif section == 'Perl Module':
        prefix = 'perl-modules#'
    elif section == 'Perl Dep':
        prefix = 'perl-deps#'
    package['name'] = prefix + module_name
    package['description'] = get_description(doc)
    package['section'] = section
    package['downloadUrls'] = get_unique_urls(get_download_urls(doc))
    package['commands'] = get_commands(doc)
    package['url'] = None
    if len(package['downloadUrls']) > 0:
        package['url'] = package['downloadUrls'][0]
    package['tarball'] = get_tarball(package['url'])
    package['version'] = get_version(package['tarball'])
    package['dependencies'] = get_dependencies(doc)
    return package

def parse_modules_page(python_modules_page, module_type):
    with open(python_modules_page, 'rb') as fp:
        data = fp.read()
        doc = BeautifulSoup(data, features='lxml')
        packages = list()
        modules_anchors = doc.select('div.itemizedlist ul.compact li.listitem a.xref')
        for module_anchor in modules_anchors:
            module_name = module_anchor.attrs['href'].split('#')[-1]
            section_anchor = doc.select_one('div.sect2 h2.sect2 a#' + module_name)
            section = section_anchor.parent.parent
            packages.append(parse_section(module_name, module_type, section))
        return packages

def is_valid(package):
    if package['name'] not in ['krameworks5', 'plasma-all', 'alsa', 'profile'] and (package['description'] == None or len(package['commands']) == 0):
        invalid_packages.append(package['name'])
        return False
    else:
        return True

def validate_dependencies(packages):
    for package in packages:
        for name in invalid_packages:
            if name in package['dependencies']['required']:
                package['dependencies']['required'].remove(name)
            if name in package['dependencies']['recommended']:
                package['dependencies']['recommended'].remove(name)
            if name in package['dependencies']['optional']:
                package['dependencies']['optional'].remove(name)

def get_packages(index_path):
    links = get_links(index_path)
    packages = list()
    for link in links:
        if 'python-modules' in link:
            modules = parse_modules_page(link, 'Python Module')
            packages.extend(modules)
        elif 'perl-modules' in link:
            modules = parse_modules_page(link, 'Perl Module')
        elif 'perl-deps' in link:
            modules = parse_modules_page(link, 'Perl Dep')
            packages.extend(modules)
        else:
            package = parse_page(link)
            if is_valid(package):
                packages.append(package)
    return packages

if __name__ == "__main__":
    index_path = '/home/chandrakant/aryalinux/books/blfs/index.html'
    packages = get_packages(index_path)
    validate_dependencies(packages)
    print(json.dumps(packages, indent=4))