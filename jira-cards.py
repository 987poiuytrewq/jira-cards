#!/usr/bin/env python

import argparse
from generator import Generator

parser = argparse.ArgumentParser(description='Generate cards from JIRA')
parser.add_argument('-f', '--format', help='format file', default='format/basic.html')
parser.add_argument('-l', '--layout', help='layout file', default='layout/basic.html')
parser.add_argument('-s', '--style', help='stylesheet file', default='style/oblong-post-it.css')

subparsers = parser.add_subparsers(title='mode of operation', dest='mode')

template_parser = subparsers.add_parser('blank', help='generate blank cards for print alignment')
template_parser.add_argument('-n', '--number', help='number of cards to generate', type=int, default=3)

board_parser = subparsers.add_parser('board', help='generate cards from an agile board')
issue_parser = subparsers.add_parser('issues', help='generate cards from a list of issue ids')

for subparser in [board_parser, issue_parser]:
    subparser.add_argument('server', help='jira server to connect to')
    subparser.add_argument('-n', '--noauth', help='authentication not required', action='store_true')
    subparser.add_argument('-u', '--username', help='username to authenticate as', default=None)
    subparser.add_argument('-p', '--password', help='password to authenticate with', default=None)
    subparser.add_argument('-d', '--debug', help='print available fields', action='store_true')

board_parser.add_argument('-b', '--board', help='name of agile board')
issue_parser.add_argument('issues', help='list of issue ids', nargs='+')

arguments = parser.parse_args()
Generator(arguments)
