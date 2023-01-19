#!/bin/python
import subprocess
import os
import json
import re
import pyperclip
import argparse
from termcolor import colored
from PyInquirer import prompt, Separator
from shutil import which


def is_tool(name):
    """Check whether `name` is on PATH and marked as executable."""
    return which(name) is not None


if is_tool('bw') is False:
    exit('bw bin not found in your path')

bw_path = which('bw')
command = '{} list items'.format(bw_path).split(' ')
my_env = os.environ.copy()
# Openssl fix https://github.com/bitwarden/clients/issues/2726
my_env['OPENSSL_CONF'] = '/dev/null'
#my_env['BW_SESSION'] = '<super_secret_key>'

parser = argparse.ArgumentParser(
    description='Find & copy passwords to your clipboard from Bitwarden vault'
)
parser.add_argument('string',
                    help='String to find')
args = vars(parser.parse_args())
to_find = args['string']

result = subprocess.Popen(command, env=my_env, stdout=subprocess.PIPE)
output = result.stdout.read().decode("utf-8")

vault_items = json.loads(output)

items = {}
# Re-arrange the items
for item in vault_items:
    if 'login' in item:
        items[item['name']] = item['login']

items_keys = list(items.keys())

r = re.compile(".*" + to_find + ".*", re.IGNORECASE)
match_items = list(filter(r.match, items_keys))

if len(match_items) > 1:
    action_question = [
        {
            'type': 'list',
            'name': 'item_selected',
            'message': 'Which credential do you need?',
            'choices': match_items,
        },
    ]
    action_selected = prompt(action_question)
    # print('selected:' + action_selected['item_selected'])
    item_name = action_selected['item_selected']
elif len(match_items) == 1 :
    item_name = match_items[0]
else:
    print('No credentials found.')
    exit(1)

item_credentials = items[item_name]
pyperclip.copy(str(item_credentials['password']))

if 'uris' in item_credentials:
    uri = item_credentials['uris'][0]['uri']
else:
    uri = 'None'

colored_passwd = colored(
    item_credentials['password'],
    'white',
    'on_white')

colored_item_name = colored(
    item_name,
    'yellow',
    attrs=["bold"],
    )

print('Full Item Name: {}'.format(colored_item_name))
print('URL: {}'.format(uri))
print('username: {}'.format(item_credentials['username']))
print('Password: {}'.format(colored_passwd))
print('Password copied to clipboard')