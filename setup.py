from setuptools import setup,find_packages

with open("README.md", "r", encoding="utf-8") as fh:
	long_description = fh.read()

setup(
	name="gramup",
	version="0.0.5",
	author="Rohit T P",
	author_email="tprohit9@gmail.com",
	description="A utility to use Telegram as a backup solution.",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/rohittp0/GramUp",
	packages=find_packages("gramup"),
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: GNU Affero General Public License v3",
		"Operating System :: OS Independent",
	],
	include_package_data=True,
	install_requires=[ "speedtest-cli", "python-telegram" ],
	entry_points={
		"console_scripts": [ "gramup=gramup.main:main" ]
	},
	python_requires='>=3.6',
)
