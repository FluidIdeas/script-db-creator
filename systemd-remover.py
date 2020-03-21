#!/usr/bin/env python3

import json

def get_actual_commands(blfs_install_cmd):
    blfs_makefile_path = '/home/chandrakant/work/blfs-systemd-units-20180105/Makefile'
    target = blfs_install_cmd.replace('sudo make ', '')
    print(target)
    with open(blfs_makefile_path) as fp:
        lines = fp.readlines()
    start = 0
    for line in lines:
        start = start + 1
        if line.startswith(target):
            break
    end = -1
    for i in range(start, len(lines)):
        if lines[i].startswith('install-') and ':' in lines[i]:
            end = i - 1
            break
    return lines[start: end]

def read_vars():
    blfs_makefile_path = '/home/chandrakant/work/blfs-systemd-units-20180105/Makefile'
    with open(blfs_makefile_path, 'r') as fp:
        lines = fp.readlines()
    vars = dict()
    for line in lines:
        if '=' in line:
            parts = line.split('=')
        vars[parts[0]] = parts[1].replace('${DESTDIR}', '').strip()
    return vars

def process_systemd_commands(vars, commands):
    processed = list()
    for command in commands:
        if '${' in command:
            for key, value in vars.items():
                if '${' + key + '}' in command:
                    command = command.replace('${' + key + '}', value)
        command = command.replace('test -n "${DESTDIR}" || ', '')
        processed.append(command.strip())
    return processed

def get_additional_commands(package):
    vars = read_vars()
    found = False
    index = -1
    for i, command in enumerate(package['commands']):
        if 'blfs-systemd-units' in command:
            found = True
            index = i
            break
    blfs_command = None
    if found:
        for i in range(index, len(package['commands'])):
            if 'make install-' in package['commands'][i]:
                blfs_command = package['commands'][i]
    if found:
        print('Package: ' + package['name'])
        print('Found blfs command: ' + blfs_command)
        print('Actual Command: ')
        print(process_systemd_commands(vars, get_actual_commands(blfs_command)))
    return package

new_packages = list()
with open('packagedb.json', 'r') as fp:
    packages = json.load(fp)
    for package in packages:
        new_packages.append(get_additional_commands(package))

with open('packagedb.json', 'w') as fp:
    fp.write(json.dumps(new_packages, indent=4))