#!/usr/bin/env python3

import os
import json
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
    for script in scripts:
        package = parse_package(script)
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
    return sections

def create_menu_item(label, action_handler):
	item = Gtk.MenuItem.new_with_mnemonic(label)
	if action_handler != None:
		item.connect('activate', action_handler)
	return item

def create_menu(label, item_labels, action_handlers):
	menuitem = create_menu_item(label, None)
	menu = Gtk.Menu()
	for i in range(len(item_labels)):
		if item_labels[i] == '':
			item = Gtk.SeparatorMenuItem()
		else:
			item = create_menu_item(item_labels[i], action_handlers[i])
		menu.append(item)
	menuitem.set_submenu(menu)
	return menuitem

def create_main_menu():
	menubar = Gtk.MenuBar()
	menubar.append(create_menu('_Packages', ['_Update Scripts', '_Apply Changes', '', '_Install Updates', '', '_Exit'], [
		do_nothing,
		do_nothing,
		None,
        do_nothing,
        None,
		do_nothing]))
	menubar.append(create_menu('_Settings', ['_Options'], [do_nothing]))
	menubar.append(create_menu('_Help', ['_About'], [do_nothing]))
	return menubar

def do_nothing(a=None):
    pass

def execute(commands):
    process = subprocess.Popen(commands)
    process.communicate()
