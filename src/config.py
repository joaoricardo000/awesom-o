import os

auth = (os.environ.get('WHATSAPP_LOGIN'), os.environ.get('WHATSAPP_PW'))

# If filter_groups is True, the bot only stays
# at groups that there is at least one admin on it.
# Otherwise will leave instantly if added.
filter_groups = True
admins = [os.environ.get('WHATSAPP_ADMIN'), ]

# Bing API for image search
bing_api_key = os.environ.get('BING_API_KEY')

# Path to download the media requests
# (audio recordings, printscreens, media and youtube videos)
media_storage_path = "/tmp/"

# Session shelve db path
session_db_path = "/tmp/sessions.db"


# Logging configuration.
# By default only logs the command messages.
# If logging_level set to logging.DEBUG, yowsup will log every protocoll message exchange with server.
import logging

log_format = '_%(filename)s_\t[%(levelname)s][%(asctime)-15s] %(message)s'
logging_level = logging.INFO
