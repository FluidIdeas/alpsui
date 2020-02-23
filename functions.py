#!/usr/bin/env python3

import requests

def append_unique(lst, item):
    if item not in lst:
        lst.append(item)

def loadconfig():
    with open('/etc/alps/alps.conf', 'r') as fp:
        lines = fp.readlines()
    conf = dict()
    for line in lines:
        parts = line.split('=')
        key = parts[0].strip()
        value = parts[1].strip()
        if value[0] == '"':
            value = value[1:]
        if value[len(value) - 1] == '"':
            value = value[:-1]
        conf[key] = value
    return conf

def read_dependencies(script_path):
    with open(script_path, 'r') as fp:
        lines = fp.readlines()
    deps = list()
    for line in lines:
        if '#REQ:' in line and line.index('#REQ:') == 0:
            deps.append(line.replace('#REQ:', '').strip())
    return deps

def get_dependencies(package_name, processed = list()):
    conf = loadconfig()
    if package_name in processed:
            return list()
    processed.append(package_name)
    deps = read_dependencies(conf['SCRIPTS_DIR'] + package_name + '.sh')
    dep_chain = list()
    for dep in deps:
        dep_list = get_dependencies(dep, processed)
        for dep_item in dep_list:
            append_unique(dep_chain, dep_item)
    dep_chain.append(package_name)
    return dep_chain

def install(package_name):
    conf = loadconfig()
    
    # Run the script associated with the package

