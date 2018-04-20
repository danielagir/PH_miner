import os

import yaml
import csv
from ph_py import ProductHuntClient
from ph_py.error import ProductHuntError

config_file = 'credentials.yml'


def run(key, secret, uri, token):
    phc = ProductHuntClient(key, secret, uri, token)

    # Example request
    try:
        with open('output.csv', 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Name', 'Tagline', 'logo URL', 'product URL', 'Upvotes', 'Comments']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=";", quoting=csv.QUOTE_ALL)
            writer.writeheader()
            for post in phc.get_todays_posts():
                line = {'Name': post.name, 'Tagline': post.tagline, 'logo URL': post.screenshot_url, 'product URL': post.redirect_url,
                        'Upvotes': post.votes_count, 'Comments': post.comments_count}
                writer.writerow(line)

    except ProductHuntError as e:
        print(e.error_message)
        print(e.status_code)


if __name__ == '__main__':
    with open(os.path.join(os.getcwd(), config_file), 'r') as config:
        cfg = yaml.load(config)
        client_key = cfg['api']['key']
        client_secret = cfg['api']['secret']
        redirect_uri = cfg['api']['redirect_uri']
        dev_token = cfg['api']['dev_token']

    run(client_key, client_secret, redirect_uri, dev_token)
