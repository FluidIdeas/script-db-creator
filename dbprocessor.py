#!/usr/bin/env python3

import json

def add_url(package):
    if len(package['downloadUrls']) > 0:
        package['url'] = package['downloadUrls'][0]
    return package

def add_processed(package):
    package['processed'] = False
    return package

def replace_xorg_config(package):
    new_cmds = list()
    if 'export XORG_CONFIG=\"--prefix=/usr --sysconfdir=/etc --localstatedir=/var --disable-static\"' in package['commands']:
        package['commands'].remove('export XORG_CONFIG=\"--prefix=/usr --sysconfdir=/etc --localstatedir=/var --disable-static\"')
    for cmd in package['commands']:
        if '$XORG_CONFIG' in cmd:
            new_cmds.append(cmd.replace('$XORG_CONFIG', '--prefix=/usr --sysconfdir=/etc --localstatedir=/var --disable-static'))
        else:
            new_cmds.append(cmd)
    package['commands'] = new_cmds
    return package

new_packages = list()
with open('packagedb.json', 'r') as fp:
    packages = json.load(fp)
    for package in packages:
        new_packages.append(replace_xorg_config(package))

with open('packagedb.json', 'w') as fp:
    fp.write(json.dumps(new_packages, indent=4))