import os
import json
import threading
import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk

CONFIG_PATH = "/etc/alps/alps.conf"
import subprocess

def get_config():
    with open(CONFIG_PATH, 'r') as fp:
        lines = fp.readlines()
    config = dict()
    for line in lines:
        splits = line.split('=')
        config[splits[0]] = splits[1].strip()
    return config

def parse_package(script_path):
    config = get_config()
    versions = dict()
    with open(config['VERSION_LIST'], 'r') as fp:
        lines = fp.readlines()
    for line in lines:
        if ':' in line:
            versions[line.split(':')[0]] = line.split(':')[1].strip()
    with open(config['SCRIPTS_DIR'] + '/' + script_path, 'r') as fp:
        lines = fp.readlines()
    deps = list()
    name = None
    description = None
    section = None
    for line in lines:
        if '#REQ:' in line and line.index('#REQ:') == 0:
            deps.append(line.split(':')[1].strip())
        if 'NAME=' in line and line.index('NAME=') == 0:
            name = line.split('=')[1].replace('"', '').strip()
        if 'VERSION=' in line and line.index('VERSION=') == 0:
            available_version = line.split('=')[1].replace('"', '').strip()
        if 'DESCRIPTION=' in line and line.index('DESCRIPTION=') == 0:
            description = line.split('=')[1].replace('"', '').strip()
        if 'SECTION=' in line and line.index('SECTION=') == 0:
            section = line.split('=')[1].replace('"', '').strip()
    if name in versions:
        status = True
        version = versions[name].strip()
    else:
        version = None
        status = False
    if section == None:
        section = 'Others'
    return {
        'name': name,
        'version': version,
        'available_version': available_version,
        'dependencies': deps,
        'status': status,
        'description': description,
        'section': section
    }

def get_packages():
    config = get_config()
    scripts = os.listdir(config['SCRIPTS_DIR'])
    package_dict = dict()
    packages = list()
    names = list()
    versions = get_versions()
    for script in scripts:
        package = parse_package(script)
        if package['name'] in versions:
            package['version'] = versions[package['name']]
        package_dict[package['name']] = package
        names.append(package['name'])
    names.sort()
    for name in names:
        packages.append(package_dict[name])
    return packages

def get_sections(packages):
    sections = list()
    for package in packages:
        if package['section'] != None and package['section'] not in sections and package['section'].strip() != '':
            sections.append(package['section'])
    sections.sort()
    sections.insert(0, 'All')
    sections.append('Search Results')
    return sections

def execute(commands):
    process = subprocess.Popen(commands)
    process.communicate()

def get_stats(packages):
    total = 0
    installed = 0
    updates = 0
    for package in packages:
        total = total + 1
        if package['status']:
            installed = installed + 1
        if package['version'] != None and package['version'] != package['available_version']:
            updates = updates + 1
    return (total, installed, updates)

def daemon_thread(commands, statusbar, finalize_method):
    process = subprocess.Popen(commands)
    statusbar.pulse()
    process.communicate()
    statusbar.stop()
    finalize_method()

def start_daemon(commands, statusbar, finalize_method):
    thread = threading.Thread(target=daemon_thread, args=(commands, statusbar, finalize_method))
    thread.start()

def get_versions():
    config = get_config()
    versions_file = config['VERSION_LIST']
    with open(versions_file) as fp:
        lines = fp.readlines()
    versions = dict()
    for line in lines:
        if ':' in line:
            parts = line.split(':')
            versions[parts[0]] = parts[1].strip()
    return versions

def write_versions(versions):
    config = get_config()
    versions_file = config['VERSION_LIST']
    with open(versions_file, 'w') as fp:
        for name, version in versions.items():
            fp.write(name + ':' + version)
