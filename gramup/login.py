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
import os
import sys
import threading

from telegram.client import Telegram
from enquiries import freetext, confirm

try:
    from gramup import VERSION
    from gramup.constants import DATA_FILE, FILES_DIR, API_ID, API_HASH, DATABASE_ENCRYPTION_KEY
    from gramup.utils import get_folders
except ModuleNotFoundError:
    from __init__ import VERSION
    from constants import DATA_FILE, FILES_DIR, API_ID, API_HASH, DATABASE_ENCRYPTION_KEY
    from utils import get_folders


def load_data():
    """
        This function tries to read phone number, chat id and
        list of backup folders from DATA_FILE. If they are not
        found it prompts user to enter them.
    """

    try:
        with open(DATA_FILE, "rb") as db_file:
            db_dict = pickle.load(db_file)
            return db_dict["phone_number"], db_dict["chat_id"], db_dict["back_up_folders"]

    except FileNotFoundError:
        ph_no = freetext("Enter your phone number with country code: ")
        print("Select folders to backup.")
        bup_folders = get_folders()
        chat_id = freetext("Enter the chat ID to be used for backup (leave blank if you are unsure): ")

        if not chat_id.isnumeric():
            chat_id = None

        os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
        os.makedirs(os.path.dirname(FILES_DIR), exist_ok=True)

        with open(DATA_FILE, "wb") as db_file:
            data = {"phone_number": ph_no, "chat_id": chat_id, "back_up_folders": bup_folders}
            pickle.dump(data, db_file)

        return ph_no, chat_id, bup_folders


def try_login_with_code(tg_client, max_tries=5, tries=0):
    try:
        tg_client.login()
    except RuntimeError as r_er:
        if "PHONE_NUMBER_INVALID" in str(r_er):
            print("Invalid Phone number")
        elif tries < max_tries:
            print("Incorrect code or password. Try again")
            return try_login_with_code(tg_client, max_tries, tries + 1)

        if os.path.exists(DATA_FILE):
            os.remove(DATA_FILE)
            sys.exit(0)


def get_chat_id(tg_client, ph_no, bup_folders):
    def message_handler(update):
        if update['message']['content'].get('text', {}).get('text', '').lower() != 'use this chat':
            return

        with open(DATA_FILE, "wb") as db_file:
            pickle.dump(
                {
                    "phone_number": ph_no,
                    "chat_id": update['message']['chat_id'],
                    "back_up_folders": bup_folders
                },
                db_file
            )

        tg_client.send_message(
            chat_id=update['message']['chat_id'],
            text='Chat selected for backup.'
        )

        done.set()

    done = threading.Event()
    tg_client.add_message_handler(message_handler)

    print("Send 'use this chat' to the chat you want to use for backup (case insensitive)")
    done.wait()

    try:
        with open(DATA_FILE, "rb") as new_db_file:
            db_dict = pickle.load(new_db_file)

    except FileNotFoundError:
        db_dict = {}

    return db_dict["chat_id"]


def login():
    """
        This function creates and authenticates Telegram client
        and calls the call_back with Telegram client, phone no
        and chat id as arguments.
    """

    (ph_no, chat_id, bup_folders) = load_data()

    tg_client = Telegram(
        api_id=API_ID,
        api_hash=API_HASH,
        files_directory=FILES_DIR,
        database_encryption_key=DATABASE_ENCRYPTION_KEY,
        tdlib_verbosity=0,
        phone=ph_no
    )

    tg_client.call_method(
        "setTdlibParameters",
        {
            "use_file_database": True,
            "use_chat_info_database": True,
            "use_message_database": True,
            "application_version": VERSION
        },
    )

    if chat_id is None:
        print("A code has been sent to you via telegram.")

    try_login_with_code(tg_client)

    if chat_id is None:
        chat_id = get_chat_id(tg_client, ph_no, bup_folders)

        if confirm("Do you want to load previously backed-up file list?"):
            print("Getting file list, this might take some time...")
            tg_client.get_chats().wait()

    return tg_client, chat_id, bup_folders
