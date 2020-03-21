#!/usr/bin/env python3

import json

def add_url(package):
    if len(package['downloadUrls']) > 0:
        package['url'] = package['downloadUrls'][0]
    return package

def add_processed(package):
    package['processed'] = False
    return package

new_packages = list()
with open('packagedb.json', 'r') as fp:
    packages = json.load(fp)
    for package in packages:
        new_packages.append(add_processed(package))

with open('packagedb.json', 'w') as fp:
    fp.write(json.dumps(new_packages, indent=4))