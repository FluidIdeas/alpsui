#!/usr/bin/env python3

with open('/etc/alps/versions') as fp:
    lines = fp.readlines()

versions = dict()
for line in lines:
    if ':' in line:
        parts = line.split(':')
        versions[parts[0]] = parts[1]

with open('/etc/alps/versions', 'w') as fp:
    for name, version in versions.items():
        fp.write(name + ':' + version)
