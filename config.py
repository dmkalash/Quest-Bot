# -*- coding: utf-8 -*-


# Quest Part
ONLINE = 0
OFFLINE = 1


# Mode configuration
MODE = ONLINE


# fill-data paths
ON_POINT_KEY = 'on_point'
OFF_POINT_KEY = 'off_point'
TEAM_KEY = 'team'
REACTION_KEY = 'reaction'
FILE_KEY = 'file'
FILE_ID_PATH = 'file.txt'


# File types
TEXT_TYPE = 1
PHOTO_TYPE = 2
DOCUMENT_TYPE = 3
AUDIO_TYPE = 4


# Timer delta configuration
CHECKER_TIME = 15.0


# ID's for 'Sudo'-commands
ADMIN_USER_IDS = [75129762]


# CSV-data separator
CSV_SEP = ';'


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


# Last point name
LAST_POINT_NAME = 'LastPoint'


# Utils success
SUCCESS = 'Success'
ERROR = 'Error'
