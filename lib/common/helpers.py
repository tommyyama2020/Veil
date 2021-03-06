"""
This file contains miscellaneous functions used by the framework
"""

import ipaddress
import os
import random
import re
import string
import sys


# Try to find and import the settings.py config file
try:
    sys.path.append("/etc/veil/")
    import settings
except ImportError:
    print( "\n [!] ERROR #1-3: Can't import /etc/veil/settings.py.   Run: %s\n" % ( os.path.abspath( "./config/update-config.py" ) ) )
    sys.exit()

# See if ./config/setup.sh has been executed
if not os.path.exists( settings.GOLANG_PATH ):
    print( "\n [!] ERROR #2-3: Can't find Go (%s).   Run: %s --force --silent\n" % ( settings.GOLANG_PATH, os.path.abspath( "./config/setup.sh" ) ) )
    sys.exit()

if not os.path.exists( settings.PYINSTALLER_PATH ):
    print( "\n [!] ERROR #2-3: Can't find PyInstaller (%s).   Run: %s --force --silent\n" % ( settings.PYINSTALLER_PATH, os.path.abspath( "./config/setup.sh" ) ) )
    sys.exit()

if not os.path.exists( settings.METASPLOIT_PATH ):
    print( "\n [!] ERROR #2-3: Can't find the Metasploit Framework (%s).   Run: %s --force --silent\n" % ( settings.METASPLOIT_PATH, os.path.abspath( "./config/setup.sh" ) ) )
    sys.exit()

if not os.path.exists( settings.WINEPREFIX ):
    print( "\n [!] ERROR #2-3: Can't find the WINE profile (%s).   Run: %s --force --silent\n" % ( settings.WINEPREFIX, os.path.abspath( "./config/setup.sh" ) ) )
    sys.exit()

if not os.path.exists( settings.WINEPREFIX + "/drive_c/Python34/python.exe" ):
    print( "\n [!] ERROR #2-3: Can't find the WINE profile for Python v3.4 (%s).   Run: %s --force --silent\n" % ( settings.WINEPREFIX + "/drive_c/Python34/python.exe", os.path.abspath( "./config/setup.sh" ) ) )
    sys.exit()

if not os.path.exists( settings.WINEPREFIX + "/drive_c/Ruby187/bin/ruby.exe" ):
    print( "\n [!] ERROR #2-3: Can't find the WINE profile for Ruby v1.8.7 (%s).   Run: %s --force --silent\n" % ( settings.WINEPREFIX + "/drive_c/Ruby187/bin/ruby.exe", os.path.abspath( "./config/setup.sh" ) ) )
    sys.exit()

if not os.path.exists( settings.WINEPREFIX + "/drive_c/Program Files/AutoIt3/Aut2Exe/Aut2exe.exe" ):
    print( "\n [!] ERROR #2-3: Can't find the WINE profile for AuotIT v3 (%s).   Run: %s --force --silent\n" % ( settings.WINEPREFIX + "/drive_c/Program Files/AutoIt3/Aut2Exe/Aut2exe.exe", os.path.abspath( "./config/setup.sh" ) ) )
    sys.exit()


def clean_payloads():
    print("\n [*] Cleaning %s" % (settings.PAYLOAD_SOURCE_PATH))
    os.system('rm -f %s/*.*' % (settings.PAYLOAD_SOURCE_PATH))

    print(" [*] Cleaning %s" % (settings.PAYLOAD_COMPILED_PATH))
    os.system('rm -f %s/*.exe' % (settings.PAYLOAD_COMPILED_PATH))

    print(" [*] Cleaning %s" % (settings.HANDLER_PATH))
    os.system('rm -f %s/*.rc' % (settings.HANDLER_PATH))

    print(" [*] Cleaning %s" % (settings.HASH_LIST))
    os.system('rm -f %s' % (settings.HASH_LIST))
    os.system('touch ' + settings.HASH_LIST)

    print(" [*] Cleaning ./tools/vt-notify/results.log")
    os.system('rm -f ./tools/vt-notify/results.log')
    return


def color(string, status=True, warning=False, bold=True, yellow=False):
    """
    Change text color for the linux terminal, defaults to green.

    Set "warning=True" for red.
    """
    attr = []
    if status:
        # green
        attr.append('32')
    if warning:
        # red
        attr.append('31')
    if bold:
        attr.append('1')
    if yellow:
        attr.append('33')
    return '\x1b[%sm%s\x1b[0m' % (';'.join(attr), string)


def check_int(incoming_int):
    # This checks if the variable is an integer and returns a boolean
    try:
        int(incoming_int)
        return True
    except ValueError:
        return False

#################################################################
#
# Randomization/obfuscation methods.
#
#################################################################


def randomString(length=-1):
    """
    Returns a random string of "length" characters.
    If no length is specified, resulting string is in between 6 and 15 characters.
    """
    if length == -1:
        length = random.randrange(6, 16)
    random_string = ''.join(random.choice(string.ascii_letters) for x in range(length))
    return random_string


def randomKey(b=32):
    """
    Returns a random string/key of "b" characters in length, defaults to 32
    """
    return ''.join(random.choice(string.ascii_letters + string.digits + "{}!@#$^&()*&[]|,./?") for x in range(b))


def randomNumbers(b=7):
    """
    Returns a random string/key of "b" characters in length, defaults to 7
    """
    random_number = int(''.join(random.choice(string.digits) for x in range(b))) + 100000

    if random_number < 1000000:
        random_number = random_number + 1000000

    return random_number


def validate_hostname(hostname):
    """
    Try to validate the passed host name, return True or False.
    """
    if len(hostname) > 255:
        return False
    if hostname[-1:] == ".":
        hostname = hostname[:-1]
    allowed = re.compile("(?!-)[A-Z\d-]{1,63}(?<!-)$", re.IGNORECASE)
    return all(allowed.match(x) for x in hostname.split("."))


def validate_ip(ip_address):
    try:
        ipaddress.ip_address(ip_address)
        return True
    except ValueError:
        return False


def validate_port(port_number):
    try:
        if 0 < int(port_number) < 65535:
            return True
        else:
            return False
    except ValueError:
        return False
