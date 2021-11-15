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

import logging
import sys
from os import system, getcwd, listdir
from os.path import join, isdir
from pathlib import Path
from shutil import get_terminal_size

from enquiries import choose, confirm

try:
    from gramup import BANNER
    from gramup.constants import LOG_FILE, GRAM_IGNORE
except ModuleNotFoundError:
    from __init__ import BANNER
    from constants import LOG_FILE, GRAM_IGNORE


def get_folders(c_dir=None, selected_dirs=None):
    """
        This function shows a file chooser to select
        multiple directories.
    """

    if c_dir is None:
        c_dir = getcwd()

    selected_dirs = selected_dirs if selected_dirs else set([])

    dirs = {item for item in listdir(c_dir) if isdir(join(c_dir, item))}
    dirs = {item for item in dirs if join(c_dir, item) not in selected_dirs and item[0] != "."}

    options = ["Select This directory"]
    options.extend(dirs)
    options.append("⬅")

    info = f"You have selected : \n {','.join(selected_dirs)} \n" if len(selected_dirs) > 0 else "\n"
    choice = choose(f"{info}You are in {c_dir}", options)

    if choice == options[0]:
        selected_dirs.add(c_dir)

        if confirm("Do you want to select more folders?"):
            return get_folders(str(Path(c_dir).parent), selected_dirs)

        return selected_dirs

    if choice == options[-1]:
        return get_folders(str(Path(c_dir).parent), selected_dirs)

    return get_folders(join(c_dir, choice), selected_dirs)


def get_logger():
    """
        This enables logging to log file.
    """

    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(name)s %(message)s'
    )

    return logging.getLogger(__name__)


def print_banner():
    """
        This function prints the GramUp banner.
    """

    system('cls||clear')
    print(BANNER)


def download_file(tg_client, file_id):
    """
        This function downloads the file with given file id.
    """

    task = tg_client.call_method("downloadFile",
                                 {
                                     "file_id": file_id,
                                     "priority": 32,
                                     "offset": 0,
                                     "limit": 0,
                                     "synchronous": True
                                 }
                                 )
    task.wait()

    return task


def get_file_id(tg_client, chat_id, msg_id):
    """
        This function gets the file id using message id.
    """

    msg = tg_client.call_method("getMessage",
                                {
                                    "chat_id": chat_id,
                                    "message_id": msg_id
                                }
                                )
    msg.wait()

    if msg.error_info:
        get_logger().error("Error getting file id %s", msg.error_info)
        return None

    msg = msg.update["content"]

    if "document" in msg and msg["document"]["document"]["local"]["can_be_downloaded"]:
        return msg["document"]["document"]["id"]

    return None


def get_messages(tg_client, chat_id):
    """
        This function gets all messages from a chat.
    """

    all_messages, last_id, errors = (set([]), 0, 0)
    file_log = get_logger()

    while True:
        messages = tg_client.call_method(
            "getChatHistory",
            {
                "chat_id": chat_id,
                "offset": 0,
                "limit": 100,
                "only_local": False,
                "from_message_id": last_id
            }
        )

        messages.wait()
        try:
            if not messages.update["messages"] or not len(messages.update["messages"]) > 0:
                break

            for message in messages.update["messages"]:
                if "document" in message["content"]:
                    if message["content"]["document"]["document"]["local"]["can_be_downloaded"]:
                        all_messages.add((
                            message["id"],
                            message["content"]["document"]["document"]["id"],
                            message["content"]["caption"]["text"]
                        ))

            last_id = messages.update["messages"][-1]["id"]
            errors = 0

        except TypeError as t_er:
            errors += 1
            file_log.warning("Error getting messages %s", t_er)
            if errors > 10:
                print("Too many errors. Try again later.")
                file_log.error("Too many errors %s", messages.error_info)
                sys.exit(0)

    file_log.info("Got %s messages in total", len(all_messages))

    return all_messages


def get_new_files(root, old_files):
    """
        Returns the list of files in root directories that are
        not in old_files.
    """

    files = set([])
    grandparent = Path(root).parent
    excludes = []
    with open(GRAM_IGNORE) as ignore:
        excludes = [f"!{i}" for i in ignore.readlines()]
    exc = "| ".join(excludes)
    all_files = set(Path(root).rglob(f' ^({exc})'))
    for path in all_files:
        if path.is_file():
            files.add(str(path))

    return [(item, grandparent) for item in files - old_files]


def print_progress_bar(iteration, total, prefix='', suffix='', fill='█'):
    """
        Call in a loop to create terminal progress bar
        @params:
            iteration   - Required  : current iteration (Int)
            total	   - Required  : total iterations (Int)
            prefix	  - Optional  : prefix string (Str)
            suffix	  - Optional  : suffix string (Str)
            fill		- Optional  : bar fill character (Str)
    """

    percent = ("{0:." + str(1) + "f}").format(100 * (iteration / float(total)))
    styling = '%s |%s| %s%% %s' % (prefix, fill, percent, suffix)
    cols, _ = get_terminal_size(fallback=(100, 1))
    length = cols - len(styling)
    filled_length = int(length * iteration // total)
    p_bar = fill * filled_length + '-' * (length - filled_length)
    print('\r%s' % styling.replace(fill, p_bar), end='\r')
    # Print New Line on Complete
    if iteration == total:
        print()


def long_choice(prompt, options, multi=False):
    up, down = "⬆", "⬇"
    _, rows = get_terminal_size(fallback=(100, 1))

    if rows > len(options) - 4:
        return choose(prompt, options, multi)

    options_chunks = []
    chunk_index = 0

    for i in range(0, len(options), rows - 4):
        if i != 0:
            options_chunks.append([up, *options[i:min(i + rows - 4, len(options))], down])
        else:
            options_chunks.append([*options[i:min(i + rows - 4, len(options))], down])

    while True:
        choice = choose(prompt, options_chunks[chunk_index], multi)

        if choice == up:
            chunk_index = (chunk_index - 1) % len(options_chunks)
        elif choice == down:
            chunk_index = (chunk_index + 1) % len(options_chunks)
        else:
            return choice
