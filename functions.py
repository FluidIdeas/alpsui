#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import subprocess
import os

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

def get_download_urls(package_name):
    conf = loadconfig()
    filename = conf['SCRIPTS_DIR'] + package_name + '.sh'
    with open(filename) as fp:
        lines = fp.readlines()
    download_urls = list()
    for line in lines:
        if 'wget' in line and line.index('wget') == 0:
            parts = line.split()
            url = parts[len(parts) - 1]
            download_urls.append(url)
    return download_urls

def is_installed(package_name):
    conf = loadconfig()
    with open(conf['INSTALLED_LIST'], 'r') as fp:
        lines = fp.readlines()
    for line in lines:
        if package_name + '=>' in line and line.index(package_name + '=>') == 0:
            return True
    return False

def get_latest_aryalinux_version():
    p = subprocess.Popen('/usr/bin/curl -q https://sourceforge.net/projects/aryalinux/files/releases/', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    (out, err) = p.communicate()
    doc = BeautifulSoup(out, features='lxml')
    rows = doc.select('table#files_list tbody tr')
    versions = list()
    for row in rows:
        row_title = row.attrs['title']
        if row_title not in ['2015', '2016.04', '2016.08', '2017', '2017.08', '1.0']:
            versions.append(row_title)
    versions.sort()
    return versions[len(versions) - 1]

def get_aryalinux_version():
    with open('/etc/lsb-release', 'r') as fp:
        lines = fp.readlines()
    version = None
    for line in lines:
        if 'DISTRIB_RELEASE=' in line and line.index('DISTRIB_RELEASE=') == 0:
            version = line.replace('DISTRIB_RELEASE=', '').replace('"', '').strip()
            break
    return version

def get_installation_source():
    if os.path.exists('/etc/alps/install-source'):
        with open('/etc/alps/install-source') as fp:
            lines = fp.readlines()
        source = lines[0].strip()
        return source
    else:
        with open('/etc/alps/installed-list') as fp:
            lines = fp.readlines()
        xserver = False
        de = None
        libreoffice = False
        for line in lines:
            if 'xserver-meta' in line and line.index('xserver-meta') == 0:
                xserver = True
                break
        if xserver:
            for line in lines:
                if 'desktop-environment' in  line:
                    de = line.split('=')[0].strip().replace('-desktop-environment', '')
                    break
        if de == 'kde':
            de = 'kde5'
        if de != None:
            for line in lines:
                if 'libreoffice' in line and line.index('libreoffice') == 0:
                    libreoffice = True
        source = 'aryalinux-'
        if xserver and de != None and libreoffice:
            source = source + get_aryalinux_version() + '-' + de + '-x86_64.iso'
        elif xserver and de != None and not libreoffice:
            source = source + get_aryalinux_version() + '-' + de + '-slim-x86_64.iso'
        return source

