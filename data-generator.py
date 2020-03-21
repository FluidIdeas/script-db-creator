#!/usr/bin/env python3

from bs4 import BeautifulSoup
import json

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

def parse_page(page_path):
    with open(page_path, 'rb') as fp:
        data = fp.read()
        doc = BeautifulSoup(data, features='lxml')
        package = dict()
        package['name'] = get_name(page_path)
        #package['description'] = get_description(doc)
        package['section'] = get_section(page_path)
        package['downloadUrls'] = get_unique_urls(get_download_urls(doc))
        package['commands'] = get_commands(doc)
        package['url'] = None
        if len(package['downloadUrls']) > 0:
            package['url'] = package['downloadUrls'][0]
        package['tarball'] = get_tarball(package['url'])
        package['version'] = get_version(package['tarball'])
        return package

def get_packages(index_path):
    links = get_links(index_path)
    packages = list()
    for link in links:
        packages.append(parse_page(link))
    return packages

if __name__ == "__main__":
    index_path = '/home/chandrakant/aryalinux/books/blfs/index.html'
    packages = get_packages(index_path)
    print(json.dumps(packages, indent=4))