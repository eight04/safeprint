#! python3

import re
from os import path
from io import open

from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

def read(file):
	with open(path.join(here, file), encoding='utf-8') as f:
		content = f.read()
	return content
	
def find_version(file):
	return re.search(r"__version__ = (\S*)", read(file)).group(1).strip("\"'")
	
setup(
	name = "safeprint",
	version = find_version("safeprint/__init__.py"),
	description = 'A printer suppressing UnicodeEncodeError',
	long_description = read("README.rst"),
	url = 'https://github.com/eight04/safeprint',
	author = 'eight',
	author_email = 'eight04@gmail.com',
	license = 'MIT',
	# See https://pypi.python.org/pypi?%3Aaction=list_classifiers
	classifiers = [
		'Development Status :: 5 - Production/Stable',
		"Environment :: Console",
		"Environment :: Win32 (MS Windows)",
		"Intended Audience :: Developers",
		"License :: OSI Approved :: MIT License",
		"Natural Language :: Chinese (Traditional)",
		"Operating System :: Microsoft :: Windows :: Windows 7",
		"Programming Language :: Python :: 3.5",
		"Topic :: Terminals"
	],
	keywords = 'windows cmd unicode print',
	packages = find_packages(),
	install_requires = [
		"win-unicode-console >= 0.4; sys_platform == 'win32' and python_version < '3.6'"
	],
	entry_points = {
		"console_scripts": [
			
		]
	}
)
