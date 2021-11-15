"""
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
"""

from enquiries import choose, confirm


def how_to_backup():
    """
        This function shows steps to backup.
    """
    print('steps to backup goes here')
   
def how_to_restore():
    """
        This function shows steps to restore.
    """
    print('steps to restore goes here')


def gramupHelp():
    """
        This function displays the help menu.
    """

    options = ["How To backup", "How to Restore", "Go-Back"]
    functions = [how_to_backup, how_to_restore,]

    try:
        while True:
            functions[options.index(choose("What do you want to do?", options))]()
    except IndexError:
        pass