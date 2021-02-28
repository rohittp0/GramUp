'''
    This is a utility to use Telegram's unlimited storage for backup.
    Copyright (C) 2021  Rohit T P

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see https://www.gnu.org/licenses/
'''

from os.path import join
from re import match
from setuptools import setup

PACKAGE_NAME = "gramup"

with open("README.md", "r", encoding="utf-8") as fh:
	long_description = fh.read()

with open(join(PACKAGE_NAME, '__init__.py'),"r") as init_py :
	version = match("__version__ = ['\"]([^'\"]+)['\"]", init_py.read()).group(1)

with open("requirements.txt","r") as f:
	requires = f.read().splitlines()


setup(
	name=PACKAGE_NAME,
	version=version,
	author="Rohit T P",
	author_email="tprohit9@gmail.com",
	description="A utility to use Telegram as a backup solution.",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/rohittp0/GramUp",
	packages=[PACKAGE_NAME],
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: GNU Affero General Public License v3",
		"Operating System :: OS Independent",
	],
	entry_points={
		"console_scripts": [ "gramup=gramup.__main__:main" ]
	},
	include_package_data=True,
	install_requires=requires,
	python_requires='>=3.6',
)
