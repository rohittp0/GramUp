from setuptools import setup
from os.path import join
from re import match

package_name = "gramup"

with open("README.md", "r", encoding="utf-8") as fh:
	long_description = fh.read()

with open(join(package_name, '__init__.py'),"r") as init_py :
    version = match("__version__ = ['\"]([^'\"]+)['\"]", init_py.read()).group(1)
    
setup(
	name=package_name,
	version=version,
	author="Rohit T P",
	author_email="tprohit9@gmail.com",
	description="A utility to use Telegram as a backup solution.",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/rohittp0/GramUp",
	packages=[package_name],
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: GNU Affero General Public License v3",
		"Operating System :: OS Independent",
	],
	entry_points={
		"console_scripts": [ "gramup=gramup.__main__:main" ]
	},
	include_package_data=True,
	install_requires=[ "speedtest-cli", "python-telegram" ],
	python_requires='>=3.6',
)
