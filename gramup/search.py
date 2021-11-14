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

import webbrowser
from shutil import move
from re import error as re_error
from re import search as re_search
from tempfile import gettempdir
from os.path import join, basename
from enquiries import choose, freetext

try:
    from gramup.utils import download_file, get_file_id, get_logger, get_messages
except ModuleNotFoundError:
    from utils import download_file, get_file_id, get_logger, get_messages


def show_file(tg_client, chat_id, files):
    """
        This function downloads and displays the file
        with id file_id.
    """

    for (msg_id, file_id, caption) in files:

        task = download_file(tg_client, file_id if file_id else get_file_id(tg_client, chat_id, msg_id))

        if task.error_info is None:
            temp_file = join(gettempdir(), basename(caption))
            move(task.update["local"]["path"], temp_file)
            webbrowser.open(f"file://{temp_file}", new=2)
        else:
            get_logger().error("Error showing file %s", task.error_info)
            freetext("Oops... Something went wrong.")


def delete_files(tg_client, chat_id, files):
    """
        This function deletes the file with id file_id.
    """

    if len(files) == 0:
        return False

    file_log = get_logger()

    question = "\n".join([f"  {caption_text}" for (_, _, caption_text) in files])
    question += "\n\nAre you sure you want to delete these files?"

    if choose(question, ["Yes", "No"]) == "No":
        return False

    task = tg_client.call_method("deleteMessages",
                                 {
                                     "chat_id": chat_id,
                                     "message_ids": [msg_id for (msg_id, _, _) in files],
                                     "revoke": True
                                 }
                                 )

    print("Deleting... Please wait.")
    task.wait()

    if task.error_info:
        file_log.error("Error showing file %s", task.error_info)
        freetext("Oops... Something went wrong.")
        return False

    freetext("Files deleted.")
    return True


def search(tg_client, chat_id):
    """
        This function searches for uploaded file using the
        RegEx provide by the user.
    """

    search_reg = freetext("Enter the file path to search for ( RegEx supported )")
    print("Searching...")
    files = []

    try:
        for (msg_id, file_id, caption) in get_messages(tg_client, chat_id):
            if re_search(search_reg, caption):
                files.append((msg_id, file_id, caption))
                print(f"{len(files)}){caption}")
    except re_error as re_er:
        get_logger().warning("Error searching %s", re_er)

    print()

    if len(files) == 0:
        return freetext("No files matched your search")

    options = ["View", "Delete", "Go Back"]
    functions = [show_file, delete_files]

    while True:
        try:
            chose = choose("What do you want to do?", options)
            if chose == options[2]:
                break

            if len(files) == 1:
                selected = files
            else:
                indexes = freetext("Enter indexes of files seperated by ',' or A to select all").split(",")
                selected = files if indexes[0].lower() == "a" else {files[int(i.strip()) - 1] for i in indexes}

            if functions[options.index(chose)](tg_client, chat_id, selected):
                break

        except (ValueError, IndexError) as v_er:
            get_logger().warning("Error reading index %s", v_er)
            print(f"Please enter number between 1 and {len(files)}")

    return None
