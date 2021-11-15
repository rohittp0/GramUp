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
import sys

from enquiries import choose

try:
    from gramup.backup import backup
    from gramup.login import login
    from gramup.restore import restore
    from gramup.search import search
    from gramup.settings import settings
    from gramup.utils import get_logger, print_banner
except ModuleNotFoundError:
    from backup import backup
    from login import login
    from restore import restore
    from search import search
    from settings import settings
    from utils import get_logger, print_banner


def client_ready(tg_client, chat_id, bup_folders):
    """
        This function is called once required data is
        loaded and Telegram client is initialized.
    """
    if not (tg_client or chat_id or bup_folders):
        sys.exit(3)

    file_log = get_logger()

    file_log.info("Client ready.")

    options = ["Backup", "Restore", "Search", "Settings", "Quit"]

    try:
        while True:
            print_banner()
            choice = choose("What do you want to do?", options)

            if choice == options[0]:
                backup(tg_client, chat_id, bup_folders)
            elif choice == options[1]:
                restore(tg_client, chat_id)
            elif choice == options[2]:
                search(tg_client, chat_id)
            elif choice == options[3]:
                settings(tg_client)
            else:
                break

    except KeyboardInterrupt:
        print_banner()
        file_log.warning("Keyboard interrupt received.")

    file_log.info("End of execution.")
    sys.exit(0)


def main():
    """
        This function is called to start GramUp.
    """
    tg_client, chat_id, bup_folders = login()
    client_ready(tg_client, chat_id, bup_folders)


if __name__ == "__main__":
    main()
