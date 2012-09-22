import json
import sys

# Giant hack to convert Cygwin's "setup" file to a JSON
# file, you know, so someone can use it for something with a
# reasonable amount of work :|
# started it at ~12:15, roughly finished with a decent
# draft at ~12:35. Not bad, even if it is a giant
# hack...

if len(sys.argv) > 1:
    setupfile = file(sys.argv[1], 'r')
else:
    setupfile = file('setup', 'r')

packages = {}
pkg_name = None
pkg = None
prev_flag = False
for line in setupfile:
    line = line[0:-1]
    if '@ ' == line[0:2]:
        pkg_name = line[2:]
        packages[pkg_name] = {}
        pkg = packages[pkg_name]
        prev_flag = False
    elif '# ' == line [0:2]:
        continue
    elif 'setup-' == line[0:7]:
        continue
    elif 'sdesc' in line:
        pkg['sdesc'] = line[8:]
    elif 'ldesc' in line:
        ldesc = [line[9:]]
        for nu_line in setupfile:
            ldesc.append(nu_line)
            if '"' in nu_line:
                break
        pkg['ldesc'] = ''.join(ldesc)
    elif 'category:' in line:
        pkg['category'] = line[10:]
    elif 'requires:' in line:
        pkg['requires'] = line[10:].split(' ')
    elif '[prev]' in line:
        prev_flag = True
    elif 'version:' in line[0:9]:
        if prev_flag:
            pkg['prev_version'] = line[9:]
        else:
            pkg['version'] = line[9:]
    elif 'install:' in line:
        if prev_flag:
            pkg['prev_install'] = line[9:].split(' ')
        else:
            pkg['install'] = line[9:].split(' ')
    elif 'source:' in line:
        if prev_flag:
            pkg['prev_source'] = line[8:].split(' ')
        else:
            pkg['source'] = line[8:].split(' ')


print json.dumps(packages)
