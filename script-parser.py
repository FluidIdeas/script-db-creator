#!/usr/bin/env python3

import os
import json

scripts_dir = '/home/chandrakant/aryalinux/aryalinux/applications'

def get_commands(lines):
    start_index = 0
    end_index = -5
    for i, line in enumerate(lines):
        if line.startswith('echo $USER > /tmp/currentuser'):
            start_index = i + 1
            break
    commands = lines[start_index:end_index]
    processed = list()
    for command in commands:
        processed.append(command.strip())
    commands = '\n'.join(processed).strip().split('\n')
    return process_commands(commands)

def process_commands(commands):
    processed = list()
    for command in commands:
        if 'cat > /tmp/rootscript.sh <<"ENDOFROOTSCRIPT"' in command:
            processed.append('# root-start #')
        elif 'ENDOFROOTSCRIPT' in command:
            processed.append('# root-end #')
        elif 'sudo rm -rf /tmp/rootscript.sh' in command or 'sudo /tmp/rootscript.sh' in command or 'chmod a+x /tmp/rootscript.sh' in command:
            pass
        else:
            processed.append(command)
    return processed

def parse_script(script_path):
    with open(script_path, 'r') as fp:
        lines = fp.readlines()
    package = dict()
    package['dependencies'] = list()
    package['downloadUrls'] = list()
    for line in lines:
        if line.startswith('NAME='):
            package['name'] = line.split('=')[1].strip()
        if line.startswith('#REQ:'):
            package['dependencies'].append(line.replace('#REQ:', '').strip())
        if line.startswith('VERSION='):
            package['version'] = line.replace('VERSION=', '').replace('"', '').strip()
        if line.startswith('DESCRIPTION='):
            package['description'] = line.replace('DESCRIPTION=', '').replace('"', '').strip()
        if line.startswith('SECTION='):
            package['section'] = line.replace('SECTION=', '').strip()
        if line.startswith('wget -nc'):
            url = line.replace('wget -nc ', '').strip()
            found = False
            for durl in package['downloadUrls']:
                if durl.split('/')[-1] == url.split('/')[-1]:
                    found = True
            if not found:
                package['downloadUrls'].append(url)
        package['commands'] = get_commands(lines)
    return package

files = os.listdir(scripts_dir)
packages = list()
for file in files:
    package = parse_script(scripts_dir + '/' + file)
    packages.append(package)
package_json = json.dumps(packages, indent=4)

with open('packagedb.json', 'w') as fp:
    fp.write(package_json)
