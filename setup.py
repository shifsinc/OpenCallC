#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# ______   ______ _______ _     _ _______ __   _      _______ _______
# |     \ |_____/ |_____| |____/  |______ | \  |         |       |   
# |_____/ |    \_ |     | |    \_ |______ |  \_|         |       |                                                                    
#
#                     http://draken.hu
#
## \file setup.py
## \brief The setup script
## \author Miklos Horvath <hmiki@blackpantheros.eu>

import os
import glob
import shutil
import sys

from distutils.core import setup
from distutils.cmd import Command
from distutils.command.build import build
from distutils.command.install import install
from setuptools import setup
import subprocess
    
with open("README.md", "r") as fh:
    long_description = fh.read()

def have_gettext():
    return subprocess.getoutput("pyuic5 --help").find("--gettext") > -1

def update_messages():
    # Create empty directory
    pkgname="opencallc"
    os.system("rm -rf .tmp")
    os.makedirs(".tmp")
    # Collect UI files
    for filename in glob.glob1("modules_uic", "*.ui"):
        if have_gettext():
            os.system("pyuic5 -g -o .tmp/ui_%s.py modules_uic/%s" % (filename.split(".")[0], filename))
        else:
            os.system("pyuic5 -o .tmp/ui_%s.py modules_uic/%s" % (filename.split(".")[0], filename))
    # Collect Python files
    for filename in glob.glob1("modules_uic", "*.py"):
        shutil.copy("modules_uic/%s" % filename, ".tmp")
    # Generate POT file
    os.system("xgettext --default-domain=%s --keyword=_ --keyword=i18n --keyword=ki18n -o po/%s.pot .tmp/* src/*.py" % (pkgname,pkgname))
    # Update PO files
    for item in os.listdir("po"):
        if item.endswith(".po"):
            os.system("msgmerge -q -o .tmp/temp.po po/%s po/%s.pot" % (item,pkgname))
            os.system("cp .tmp/temp.po po/%s" % item)
    # Remove temporary directory
    os.system("rm -rf .tmp")
    
class Build(build):
    def run(self):
        os.system("rm -rf build")
        os.system("mkdir -p build/lib/opencallc")
        os.system("mkdir -p build/scripts-3.7")
        print ("Copying PYs Src...")
        os.system("cp -r src/* build/lib/opencallc")
        print ("Generating UIs...")
        for filename in glob.glob1("modules_uic", "*.ui"):
            if have_gettext():
                os.system("pyuic5 -g -o build/lib/opencallc/%s.py modules_uic/%s" % (filename.split(".")[0], filename))
            else:
                os.system("pyuic5 -o build/lib/opencallc/%s.py modules_uic/%s" % (filename.split(".")[0], filename))
        os.system("sed -i 's/import raw_rc/from opencallc import raw_rc/g' build/lib/opencallc/OpenCallCMain.py")
        print ("Generating RCs for build...")
        for filename in glob.glob1("./", "*.qrc"):
            os.system("pyrcc5 %s -o build/lib/opencallc/%s_rc.py" % (filename, filename.split(".")[0]))
        for filename in glob.glob1("./", "*.py"):
            if filename not in ["setup.py"]:
                os.system("cat %s > build/scripts-3.7/%s" % (filename, filename[:-3]))


class Install(install):
    def run(self):
        install.run(self)

if "update_messages" in sys.argv:
    update_messages()
    sys.exit(0)

setup(
    name="OpenCallC",

    version="0.0.1",

    description="Open source callcenter software for SIM800",
    long_description = """The OpenCallC is an open source callcenter software for SIM800 modules.
    If you need extra non-free functions or modems based on SIM800 please contact me.""",
    
    url="https://github.com/HMikiHTH/OpenCallC/",

    author="Miklos Horvath",
    author_email="hmiki@blackpantheros.eu",
    
    license="GPLv3+",

    classifiers=[
        "Development Status :: 1 - Planning",

        "Intended Audience :: Customer Service",
        "Intended Audience :: Financial and Insurance Industry",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Telecommunications Industry",

        "Topic :: Desktop Environment",
        "Topic :: Desktop Environment :: K Desktop Environment (KDE)",

        "Environment :: X11 Applications :: Qt",
        
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',

        "Operating System :: POSIX :: Linux",
        "Operating System :: POSIX :: BSD :: FreeBSD",
        "Operating System :: POSIX :: BSD :: OpenBSD",

        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],

    package_dir={"opencallc":"build/lib/opencallc"},
    packages=["opencallc"],
    scripts=["build/scripts-3.7/opencallc"],
    data_files  = [('/'.join(['usr']+e.split('/')[1:-1]), [e]) for e in subprocess.getoutput("find build/locale").split() if ".mo" in e],
    install_requires = ["argparse", "configparser"],
    cmdclass = {
        'build': Build,
        'install': Install,
    }
)
