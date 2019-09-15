from __future__ import absolute_import, division, print_function, unicode_literals
import sys
from subprocess import call, check_output

def skip_non_default_packages(tags):
    if 'not_with_rhel7_pkg' in tags:
        # Do not run on stock RHEL7 package
        if call('rpm -qi NetworkManager |grep -q build.*bos.redhat.co', shell=True) == 0 and \
        check_output("rpm --queryformat %{RELEASE} -q NetworkManager |awk -F .  '{ print ($1 < 200) }'", shell=True).decode('utf-8').strip() == '1' and \
        call("grep -q 'release 7' /etc/redhat-release", shell=True) == 0:
            return True
        else:
            return False
    else:
        return False

current_nm_version = "".join(check_output("""NetworkManager -V |awk 'BEGIN { FS = "." }; {printf "%03d%03d%03d", $1, $2, $3}'""", shell=True).decode('utf-8').split('-')[0])

if "NetworkManager" in sys.argv[2] and "Test" in sys.argv[2]:
    test_name = "".join('_'.join(sys.argv[2].split('_')[2:]))
else:
    test_name = sys.argv[2]

raw_tags = check_output ("behave $(grep -l @%s %s/features/*.feature) -k -t %s --dry-run |grep %s" %(test_name, sys.argv[1], test_name, test_name), shell=True).decode('utf-8')
tests_tags = raw_tags.split('\n')

tests_tags = raw_tags.split('\n')

# for every line with the same test_name
for tags in tests_tags:
    run = True
    tags = [tag.strip('@') for tag in tags.split()]
    for tag in tags:
        if tag.startswith('ver=') or tag.startswith('ver+') or tag.startswith('ver-'):
            tag_version = [ int(x) for x in tag.replace("=","").replace("ver+","").replace("ver-","").split(".") ]
            if '+=' in tag:
                while len(tag_version) < 3:
                    tag_version.append(0)
                if current_nm_version < tag_version:
                    run = False

            elif '-=' in tag:
                while len(tag_version) < 3:
                    tag_version.append(9999)
                if current_nm_version > tag_version:
                    run = False

            elif '-' in tag:
                while len(tag_version) < 3:
                    tag_version.append(0)
                if current_nm_version >= tag_version:
                    run = False

            elif '+' in tag:
                while len(tag_version) < 3:
                    tag_version.append(0)
                if current_nm_version <= tag_version:
                    run = False
    if run:
        print(" -t ".join(tags))
        sys.exit(0)

sys.exit(1)
