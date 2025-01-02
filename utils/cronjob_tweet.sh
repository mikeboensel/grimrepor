#!/bin/bash

THIS_FILEPATH="$(realpath "$0")"
REPO_ROOT="$(dirname "$(dirname "$THIS_FILEPATH")")"
CRON_TWEET_REALPATH="$REPO_ROOT"/scripts/tweet.py

echo "THIS_FILEPATH: $THIS_FILEPATH"
echo "REPO_ROOT: $REPO_ROOT"
echo "CRON_TWEET_REALPATH: $CRON_TWEET_REALPATH"

source "$REPO_ROOT"/venv/bin/activate
python3 "$CRON_TWEET_REALPATH"


# Required:
# create a cron job that calls this script
# $ crontab -e
# repo named 'grimrepor_cron' in this example
# Run every 1.5 hours because x.com tweet limit is 17 tweets per 24 hours
#0 */1 * * * /bin/bash $HOME/grimrepor_cron/utils/cronjob_tweet.sh
# Every minute - use for testing \/
# * * * * * /bin/bash $HOME/grimrepor_cron/utils/cronjob_tweet.sh >> $HOME/cronjob_debug.log 2>&1

# REFERENCE:

# crontab -l     # list all cron jobs
# crontab -e     # edit cron jobs

# ┌───────────── minute (0 - 59)
# │ ┌───────────── hour (0 - 23)
# │ │ ┌───────────── day of the month (1 - 31)
# │ │ │ ┌───────────── month (1 - 12)
# │ │ │ │ ┌───────────── day of the week (0 - 6) (Sunday to Saturday)
# │ │ │ │ │                                   OR sun, mon, tue, wed, thu, fri, sat
# │ │ │ │ │
# │ │ │ │ │
# * * * * *
