"""
Twitter Bot for Repository Notifications

This script posts tweets to notify repository owners about build issues.
VERY IMPORTANT! There's a 17 post per 24 hour period limit.
Please make sure you add a delay on your side between calls.

Usage:
    1. Command line:
        (venv) $ python scripts/tweet.py -o owner_name -g repo_url -f repo_fork_url
        Example:
        (venv) $ python scripts/tweet.py -o nikhilbrijlal -g "https://github.com/nikhilbrijlal/my-repo" -f "https://github.com/sundai-club/my-repo"

    2. Import as module:
        ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        sys.path.append(ROOT)
        from scripts.tweet import main as tweet_main
        from scripts.tweet import update_table_in_db
        await tweet_main(
            owner_name="nikhilbrijlal",
            github_url="https://github.com/nikhilbrijlal/my-repo",
            github_fork_url="https://github.com/sundai-club/my-repo"
        )

    3. Testing (uses default values):
        (venv) $ python scripts/tweet.py

Note: Requires .env with keys, ping repo owner if API keys are needed.
"""

import os
from dotenv import load_dotenv
import asyncio
import tweepy
import sys
from datetime import datetime
import argparse
import subprocess
import random
import logging

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(ROOT)
from database.database_cmds import create_session, escape_value

logging.getLogger('tweepy').setLevel(logging.CRITICAL)
os.makedirs(os.path.join(ROOT, "logs"), exist_ok=True)

datetime_str = datetime.now().strftime("%H:%M:%S_%d-%m-%Y")
log_file = os.path.join(ROOT, "logs", f"tweet_{datetime_str}.log")
logging.basicConfig(filename=log_file, level=logging.DEBUG)


async def main(
        owner_name: str = "testperson",
        github_url: str = "https://github.com/testperson/test-repo",
        github_fork_url: str = "https://github.com/sundai-club/test-repo"
    ):
    """
    owner_name: repo owner name
    github_url: URL of the original repository
        last part of the URL is the repo_name
    github_fork_url: URL of the forked (and fixed) repository

    we need the github_url because in the db that field must be unique,
    so that let's us safely query and update the repo after tweeting
    """

    # Load environment variables
    load_dotenv()

    # Get Twitter API credentials
    API_KEY = os.getenv('TWITTER_API_KEY')
    API_KEY_SECRET = os.getenv('TWITTER_API_KEY_SECRET')
    ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN')
    ACCESS_TOKEN_SECRET = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')

    # Initialize Tweepy client with OAuth 1.0a
    client = tweepy.Client(
        consumer_key=API_KEY,
        consumer_secret=API_KEY_SECRET,
        access_token=ACCESS_TOKEN,
        access_token_secret=ACCESS_TOKEN_SECRET
    )

    parser = argparse.ArgumentParser(description='Tweet to notify repository owners about build issues')
    parser.add_argument('-o', '--owner_name', type=str, help='Repository owner name')
    parser.add_argument('-g', '--github_url', type=str, help='URL of the original repository')
    parser.add_argument('-f', '--github_fork_url', type=str, help='URL of the forked (and fixed) repository')
    args = parser.parse_args()

    if args is not None:
        owner_name = args.owner_name or owner_name
        github_url = args.github_url or github_url
        github_fork_url = args.github_fork_url or github_fork_url

    # ** do not continue if the record in the database is already marked as tweeted **
    MYSQL_DATABASE = os.getenv("MYSQL_DATABASE") or "grimrepor_db"
    TABLE_NAME = os.getenv('TABLE_NAME') or "papers_and_code"

    # Create a session
    session, schema = create_session(db_name=MYSQL_DATABASE)
    cmd_check_record = f"""
    SELECT tweet_posted
    FROM {TABLE_NAME}
    WHERE github_url = '{escape_value(github_url)}';
    """
    try:
        record = schema.get_collection(TABLE_NAME).find(cmd_check_record).execute()
        if record[0]['tweet_posted'] == 1:
            print(f"Tweet already posted for {github_url}.\n")
            logging.info(f"Tweet already posted for {github_url}.\n")
            return
        else:
            print(f"Tweet not yet posted for {github_url}.\n")
            logging.info(f"Tweet not yet posted for {github_url}.\n")
    except Exception as e:
        # not an issue if the db doesn't hold a test record
        if not owner_name.startswith("testperson"):
            print(f"Error checking record: {e}\n")
            logging.error(f"Error checking record: {e}\n")
            print(f'{cmd_check_record=}\n')
            logging.info(f'{cmd_check_record=}\n')
            return
    finally:
        session.close()

    # repo name is the last part of the url after the last slash
    repo_name = github_url.split("/")[-1]

    # This allows us to post for testing as duplicate tweets are not allowed
    if owner_name.startswith("testperson"):
        old_name = owner_name
        owner_name = owner_name + str(random.randint(1, 10000))
        github_url = github_url.replace(old_name, owner_name)

    logging.info(f'{owner_name=}\n{repo_name=}\n{github_url=}\n{github_fork_url=}\n')

    TWEET_TEXT = (
        f"Hey, @{owner_name}, your repository: {repo_name} can no longer be built!\n"
        f"We went ahead and fixed this for you at: {github_fork_url}\n"
        f"❤️ Grim Repo-r"
    )
    print("Waiting for 10 seconds before posting the tweet...")
    print(f"Tweet content to be posted:\n{TWEET_TEXT=}\n")
    logging.info(f'{TWEET_TEXT=}\n')

    await asyncio.sleep(10)

    x_response, tweet_id = None, None
    try:
        x_response = client.create_tweet(text=TWEET_TEXT)
    except tweepy.errors.TooManyRequests as e:
        print(f"Rate limit exceeded. Please wait and try again later.\n{e}\n")
        logging.error(f"Rate limit exceeded. Please wait and try again later.\n{e}\n")
        print(f"{log_file=}\n")
        return
    except Exception as e:
        print(f"Sadface homies. Misc Error posting tweet: {e}\n")
        logging.error(f"Misc Error posting tweet: {e}\n")
        print(f"{log_file=}\n")
        return

    if x_response is not None:
        tweet_id = x_response.data['id'] if x_response.data['id'] is not None else None

    tweet_url = f"https://x.com/GrimRepor/status/{tweet_id}"
    print(f"Tweet posted successfully!\n{tweet_url}\n")
    logging.info(f"Tweet posted successfully!\n{tweet_url}\n")

    update_table_in_db(github_url=github_url, tweet_posted=True, tweet_url=tweet_url)


def update_table_in_db(github_url: str, tweet_posted: bool, tweet_url: str, table_name: str = "papers_and_code"):
    """
    Tweet about the repository and update the table with the tweet URL.

    need github_url (of the original repo) to match the correct record in the db

    table columns to update:
    tweet_posted           | tinyint(1)   | 1 for true (tweet posted)
    tweet_url              | varchar(255)
    """
    MYSQL_DATABASE = os.getenv("MYSQL_DATABASE") or "grimrepor_db"
    TABLE_NAME = os.getenv('TABLE_NAME') or table_name

    # Create a session
    session, schema = create_session(db_name=MYSQL_DATABASE)
    tweet_posted = 1 if tweet_posted else 0

    # Update the table with the tweet URL
    cmd_tweet_update = f"""
    UPDATE {TABLE_NAME}
    SET tweet_posted = {escape_value(tweet_posted)}, tweet_url = '{escape_value(tweet_url)}'
    WHERE github_url = '{escape_value(github_url)}';
    """

    cmd_view_record = f"""
    SELECT *
    FROM {TABLE_NAME}
    WHERE github_url = '{escape_value(github_url)}';
    """

    try:
        # mark the record with this github_url as tweeted and store the tweet url
        schema.get_collection(TABLE_NAME).modify(cmd_tweet_update).execute()
        session.commit()
        print("Table updated successfully!")
        logging.info("Table updated successfully!")
    except Exception as e:
        print(f"Error updating table: {e}\n")
        logging.error(f"Error updating table: {e}\n")
        print(f'{cmd_tweet_update=}\n')

    try:
        record = schema.get_collection(TABLE_NAME).find(cmd_view_record).execute()
        print(record)
    except Exception as e:
        print(f"Error viewing record: {e}\n")
        logging.error(f"Error viewing record: {e}\n")
        print(f'{cmd_view_record=}\n')
        logging.info(f'{cmd_view_record=}\n')

    session.close()
    print(f"{log_file=}\n")


if __name__ == "__main__":
    asyncio.run(main())
