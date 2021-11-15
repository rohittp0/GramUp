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

import pickle
import sys
from shutil import rmtree

from enquiries import choose, confirm

try:
    from gramup.constants import CACHE_DIR, DATA_FILE, GRAMUP_DIR
    from gramup.utils import get_logger, get_folders
    from gramup.login import get_chat_id
except ModuleNotFoundError:
    from constants import CACHE_DIR, DATA_FILE, GRAMUP_DIR
    from utils import get_logger, get_folders
    from login import get_chat_id


def clear_cache(_):
    """
        This function clears all local caches.
    """

    if not confirm("Are you sure you want to clear all cache?"):
        return

    file_log = get_logger()

    try:
        rmtree(CACHE_DIR)
    except FileNotFoundError:
        file_log.warning("Cache already cleared")

    file_log.info("Cache cleared")
    input("Cache cleared. Press any enter to continue.")


def change_folder(_):
    """
        This function allows user to change backup folder.
    """

    file_log = get_logger()

    try:
        with open(DATA_FILE, "rb") as db_file:
            db_dict = pickle.load(db_file)

    except FileNotFoundError:
        file_log.warning("No backup folders to change")
        db_dict = {}

    if not confirm(f"Currently {','.join(db_dict['back_up_folders'])} are backedup.Do you want to change this?"):
        return

    db_dict["back_up_folders"] = get_folders()

    with open(DATA_FILE, "wb") as db_file:
        pickle.dump(db_dict, db_file)

    file_log.info("Backup Folders changed.")
    input("Backup Folders changed. Press any enter to continue.")


def change_chat(tg_client):
    """
        This function allows user to change backup folder.
    """

    file_log = get_logger()

    try:
        with open(DATA_FILE, "rb") as db_file:
            db_dict = pickle.load(db_file)

    except FileNotFoundError:
        file_log.warning("No backup folders to change")
        db_dict = {}
    if not confirm(
            "if you change the chat your have to again set the old chat for getting files in that chat."
            " would you lke to change the folder ? "):
        return

    get_chat_id(tg_client, db_dict["phone_number"], db_dict["back_up_folders"])

    input("backup chat changed. Press any enter to continue.")


def logout(tg_client):
    """
        This function logs the user out.
    """

    file_log = get_logger()

    if not confirm("Are you sure you want to Logout?"):
        return

    task = tg_client.call_method("logOut", {})
    task.wait()

    if task.error_info:
        print("Oops something went wrong")
        file_log.error(task.error_info)
        return

    try:
        rmtree(GRAMUP_DIR)
    except FileNotFoundError:
        file_log.warning("Cache already cleared")

    file_log.info("Logged out")
    input("Logged out. Press enter to continue.")
    sys.exit(0)


def settings(tg_client):
    """
        This function displays the settings menu.
    """

    options = ["Clear Cache", "Change Backup Folder", 'Change Backup chat', "Logout", "Go-Back", ]
    functions = [clear_cache, change_folder, change_chat, logout, ]

    try:
        while True:
            functions[options.index(choose("What do you want to do?", options))](tg_client)
    except IndexError:
        pass
