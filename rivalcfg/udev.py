"""
This modules handles udev-related stuff on Linux. It contains function to
generate, check and update rules files.

.. NOTE::

   The functions of this module must only be used with udev-based Linux distro.
"""

import re
import subprocess

from .version import VERSION
from .devices import PROFILES


#: Path to the udev rules file
RULES_FILE_PATH = "/etc/udev/rules.d/99-steelseries-rival.rules"


def generate_rules():
    """Generates the content of the udev rules file.

    :rtype: str
    """
    rules = "# Generated by rivalcfg v%s\n" % VERSION
    rules += (
        "# Do not edit this file. It can be regenerated with the following command:\n"
    )
    rules += "# \n"
    rules += "#     rivalcfg --update-udev\n\n"

    for profile in PROFILES.values():
        rules += "# %s\n" % profile["name"]
        rules += (
            'SUBSYSTEM=="hidraw", ATTRS{idVendor}=="%04x", ATTRS{idProduct}=="%04x", MODE="0666"\n'
            % (profile["vendor_id"], profile["product_id"])
        )
        rules += (
            'SUBSYSTEM=="usb", ATTRS{idVendor}=="%04x", ATTRS{idProduct}=="%04x", MODE="0666"\n\n'
            % (profile["vendor_id"], profile["product_id"])
        )

    return rules


def write_rules_file(path=RULES_FILE_PATH):
    """Generates and write the udev rules file at the given place.

    :param str path: The path of the output file.

    :raise PermissionError: The user has not sufficient permissions to write
                            the file.
    """
    path = str(path)  # py27 compatibility: coerce PosixPath to string
    rules = generate_rules()
    with open(path, "w") as rules_file:
        rules_file.write(rules)


def trigger():
    """Trigger udev to take into account the new rules."""
    subprocess.check_output(["udevadm", "trigger"])


def are_rules_up_to_date(rules, current_version=VERSION):
    """Check if the given udev rules are up to date.

    :param str rules: The content of an udev rule file to check.
    :param str current_version: The current rivalcfg version.

    :rtype: bool
    """
    version_regexp = re.compile(r".*rivalcfg\s+v([0-9]+\.[0-9]+\.[0-9]+(.+)?)\s*.*")
    rules_version = None
    if version_regexp.match(rules):
        rules_version = version_regexp.match(rules).group(1)
    return rules_version == current_version


def is_rules_file_up_to_date(path=RULES_FILE_PATH):
    """Check if the given udev rules file is up to date.

    :param str path: The path of the udev rules file.

    :rtype: bool
    """
    path = str(path)  # py27 compatibility: coerce PosixPath to string
    with open(path, "r") as rules_file:
        return are_rules_up_to_date(rules_file.read())
