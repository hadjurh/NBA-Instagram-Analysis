from instagram_scraper import InstagramScraper
import argparse
import textwrap
import re
import sys
import requests
import errno
import os
import pandas as pd

type_of_media = dict([(True, "Video"), (False, "Image")])


def get_simple_summary(scrape):
    if scrape.login_user and scrape.login_pass:
        scrape.login()
        if not scrape.logged_in and scrape.login_only:
            scrape.logger.warning('Fallback anonymous scraping disabled')
            return

    scrape.quit = False
    try:
        for username in scrape.usernames:
            scrape.posts = []
            scrape.last_scraped_filemtime = 0

            try:
                user = scrape.get_user(username)

                if not user:
                    continue

                username = user['username']
                user_dataframe = pd.DataFrame(columns=['LIKE', 'COMMENTS'])

                print(username)
                for i, item in enumerate(scrape.query_media_gen(user)):
                    if i % 200 == 0 and i > 0:
                        print(i)

                    likes = item['edge_media_preview_like']['count']
                    comments = item['edge_media_to_comment']['count']
                    likes_comments_df = pd.DataFrame([[likes, comments]], columns=['LIKE', 'COMMENTS'])
                    user_dataframe = user_dataframe.append(likes_comments_df, ignore_index=True)

                    # if not item['is_video']:
                    #     url = item['thumbnail_resources'][1]['src']
                    #     r = requests.get(url)
                    #
                    #     try:
                    #         os.makedirs(username)
                    #     except OSError as e:
                    #         if e.errno != errno.EEXIST:
                    #             raise
                    #     with open(username + '/img' + str(i + 1) + '.jpg', 'wb') as f:
                    #         f.write(r.content)
                try:
                    os.makedirs(username)
                except OSError as e:
                    if e.errno != errno.EEXIST:
                        raise
                user_dataframe.to_csv(username + '/likes_comments' + '.csv')

            except ValueError:
                scrape.logger.error("Unable to scrape user - %s" % username)

    finally:
        scrape.quit = True
        scrape.logout()


def main():
    parser = argparse.ArgumentParser(
        description="instagram-scraper scrapes and downloads an instagram user's photos and videos.",
        epilog=textwrap.dedent("""
        You can hide your credentials from the history, by reading your
        username from a local file:

        $ instagram-scraper @insta_args.txt user_to_scrape

        with insta_args.txt looking like this:
        -u=my_username
        -p=my_password

        You can add all arguments you want to that file, just remember to have
        one argument per line.

        """),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        fromfile_prefix_chars='@')

    parser.add_argument('username', help='Instagram user(s) to scrape', nargs='*')
    parser.add_argument('--destination', '-d', default='./', help='Download destination')
    parser.add_argument('--login-user', '--login_user', '-u', default=None, help='Instagram login user')
    parser.add_argument('--login-pass', '--login_pass', '-p', default=None, help='Instagram login password')
    parser.add_argument('--login-only', '--login_only', '-l', default=False, action='store_true',
                        help='Disable anonymous fallback if login fails')
    parser.add_argument('--filename', '-f', help='Path to a file containing a list of users to scrape')
    parser.add_argument('--quiet', '-q', default=False, action='store_true', help='Be quiet while scraping')
    parser.add_argument('--maximum', '-m', type=int, default=0, help='Maximum number of items to scrape')
    parser.add_argument('--retain-username', '--retain_username', '-n', action='store_true', default=False,
                        help='Creates username subdirectory when destination flag is set')
    parser.add_argument('--media-metadata', '--media_metadata', action='store_true', default=False,
                        help='Save media metadata to json file')
    parser.add_argument('--include-location', '--include_location', action='store_true', default=False,
                        help='Include location data when saving media metadata')
    parser.add_argument('--media-types', '--media_types', '-t', nargs='+', default=['image', 'video', 'story'],
                        help='Specify media types to scrape')
    parser.add_argument('--latest', action='store_true', default=False,
                        help='Scrape new media since the last scrape')
    parser.add_argument('--latest-stamps', '--latest_stamps', default=None,
                        help='Scrape new media since timestamps by user in specified file')
    parser.add_argument('--tag', action='store_true', default=False, help='Scrape media using a hashtag')
    parser.add_argument('--filter', default=None, help='Filter by tags in user posts', nargs='*')
    parser.add_argument('--location', action='store_true', default=False, help='Scrape media using a location-id')
    parser.add_argument('--search-location', action='store_true', default=False,
                        help='Search for locations by name')
    parser.add_argument('--comments', action='store_true', default=False, help='Save post comments to json file')
    parser.add_argument('--interactive', '-i', action='store_true', default=False,
                        help='Enable interactive login challenge solving')
    parser.add_argument('--retry-forever', action='store_true', default=False,
                        help='Retry download attempts endlessly when errors are received')
    parser.add_argument('--verbose', '-v', type=int, default=0, help='Logging verbosity level')

    args = parser.parse_args()

    if (args.login_user and args.login_pass is None) or (args.login_user is None and args.login_pass):
        parser.print_help()
        raise ValueError('Must provide login user AND password')

    if not args.username and args.filename is None:
        parser.print_help()
        raise ValueError('Must provide username(s) OR a file containing a list of username(s)')
    elif args.username and args.filename:
        parser.print_help()
        raise ValueError('Must provide only one of the following: username(s) OR a filename containing username(s)')

    if args.tag and args.location:
        parser.print_help()
        raise ValueError('Must provide only one of the following: hashtag OR location')

    if args.tag and args.filter:
        parser.print_help()
        raise ValueError('Filters apply to user posts')

    if args.filename:
        args.usernames = InstagramScraper.parse_file_usernames(args.filename)
    else:
        args.usernames = InstagramScraper.parse_delimited_str(','.join(args.username))

    if args.media_types and len(args.media_types) == 1 and re.compile(r'[,;\s]+').findall(args.media_types[0]):
        args.media_types = InstagramScraper.parse_delimited_str(args.media_types[0])

    if args.retry_forever:
        global MAX_RETRIES
        MAX_RETRIES = sys.maxsize

    scraper = InstagramScraper(**vars(args))

    # if args.tag:
    #     scraper.scrape_hashtag()
    # elif args.location:
    #     scraper.scrape_location()
    # elif args.search_location:
    #     scraper.search_locations()
    # else:
    #     scraper.scrape()
    get_simple_summary(scraper)


if __name__ == '__main__':
    main()
