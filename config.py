# -*- coding: utf-8 -*-
from peewee import *
import urllib.parse as urlparse
import os

# Database config
if 'HEROKU' in os.environ:
    DEBUG = False
    urlparse.uses_netloc.append('postgres')
    url = urlparse.urlparse(os.environ['DATABASE_URL'])
    DATABASE = {
     'engine': 'peewee.PostgresqlDatabase',
     'name': url.path[1:],
     'user': url.username,
     'password': url.password,
     'host': url.hostname,
     'port': url.port,
    }
    database = PostgresqlDatabase(
        DATABASE.get('name'),
        user=DATABASE.get('user'),
        password=DATABASE.get('password'),
        host=DATABASE.get('host'),
        port=DATABASE.get('port')
    )
else:
    DEBUG = True
    DATABASE = 'quest.db'
    database = SqliteDatabase(DATABASE)

# Bot token
token = '1334067341:AAHlRSNcBd5HqbIzCt9Y-o_Lbwf_k_ZZsPU'

# Quest Part
ONLINE = 1
OFFLINE = 2

# Mode configuration
MODE = ONLINE

# data filling configuration
NEED_TO_FILL_DB = False

# fill-data paths
ON_POINT_PATH = 'data/on_point.txt'
OFF_POINT_PATH = 'data/off_point.txt'
TEAM_PATH = 'data/team.txt'
ON_REACTION_PATH = 'data/on_reaction.txt'
OFF_REACTION_PATH = 'data/off_reaction.txt'
FILE_PATH = 'data/file.txt'

# File types
TEXT_TYPE = 1
PHOTO_TYPE = 2
DOCUMENT_TYPE = 3
AUDIO_TYPE = 4

# Timer delta configuration
CHECKER_TIME = 15.0

# ID's for 'Sudo'-commands
ADMIN_USER_IDS = [75129762]

# Marker for end-of-file in fill-files
EOF_MARKER = '.'

# Online-game status
ONLINE_GAME_OFF = 1 # game disabled
ONLINE_GAME_ON = 2 # game is on
ONLINE_GAME_OVER = 3 # game over

# Offline-game status
OFFLINE_GAME_OFF = 4 # game disabled
OFFLINE_GAME_ON = 5 # game is on
OFFLINE_GAME_OVER = 6 # game over

# Answer status
RIGHT_ANSWER = 1
WRONG_ANSWER = 2
LAST_WRONG_ANSWER = 3

# Is attempt last?
ATTEMPT_WAS_LAST = 1
ATTEMPT_WAS_NOT_LAST = 2

# Offline-game attempt status
SLOW_ATTEMPT = 3
MIDDLE_ATTEMPT = 2
FAST_ATTEMPT = 1
RUN_ATTEMPT = 0

# Offline-game attempts count
OFFLINE_POINT_ATTEMPTS = 3

# Last points' numbers
LAST_ON_POINT_NUM = 10
LAST_OFF_POINT_NUM = 6

# Utils success
FAILURE = 'FAILURE'
SUCCESS = 'SUCCESS'
ERROR = 'ERROR'

# Messages dict keys
MSG_HELLO = 'hello'
MSG_ONLINE_START = 'online_start'
MSG_ONLINE_END = 'online_end'
MSG_OFFLINE_START = 'offline_start'
MSG_OFFLINE_END = 'offline_end'
MSG_HELP_ON = 'help_on'
MSG_HELP_OFF = 'help_off'
MSG_SOS = 'sos'
MSG_PINNED = 'pinned'
MSG_ONLINE_MODE = 'online_mode'
MSG_OFFLINE_MODE = 'offline_mode'
MSG_FINISHED = 'finished_note'
MSG_SUDO = 'sudo'
MSG_ANSWER = 'answer'
MSG_NOT_RUNNING = 'not_running'
MSG_NOT_OFF_RUNNING = 'not_off_running'
MSG_NEED_CODE = 'need_code'
MSG_WRONG_CODE = 'wrong_code'
MSG_WRONG_POINT = 'wrong_point'
MSG_NEED_CHECK_IN = 'check_in'
