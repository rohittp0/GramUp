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

from os.path import expanduser,join

API_ID="2754829"
API_HASH="57853ffaed0830f9c16b3a3bd44f17f7"
DATABASE_ENCRYPTION_KEY="".join([
	"MIIBCgKCAQEAwVACPi9w23mF3tBkdZz+zwrzKOaaQdr01vAbU4E1pvkfj4",
	"sqDsm6lyDONS789sVoD/xCS9Y0hkkC3gtL1tSfTlgCMOOul9lcixlEKzwK",
	"ENj1Yz/s7daSan9tqw3bfUV/nqgbhGX81v/+7RFAEd+RwFnK7a+XYl9slu",
	"zHRyVVaTTveB2GazTwEfzk2DWgkBluml8OREmvfraX3bkHZJTKX4EQSjBb",
	"bdJ2ZXIsRrYOXfaA+xayEGB+8hdlLmAjbCVfaigxX0CDqWeR1yFL9kwd9P",
	"0NsZRPsmoqVwMbMu7mStFai6aIhc3nSlv8kg9qv1m6XHVQY3PnEw+QQtqS",
	"IXklHwIDAQAB"
])
GRAMUP_DIR=join(expanduser("~"),".gramup")
RE_FOLDER=join(expanduser("~"),"Restored")
FILES_DIR=join(GRAMUP_DIR,"messages")
MESGS_DIR=join(FILES_DIR,"files")
DATA_FILE=join(GRAMUP_DIR,"saved")
CACHE_FILE=join(GRAMUP_DIR,"cache")
LOG_FILE=join(GRAMUP_DIR,"log.txt")
OTHER_FOLDER="Other"
