import getpass
import argparse
from jira.client import GreenHopper

from issues import IssueFinder, IssueFormatter
import cards

class Generator:

    def __init__(self, arguments):
        options = {
            'server': arguments.server
        }

        if arguments.username:
            username = arguments.username
        else:
            username = raw_input('Username: ')
        password = getpass.getpass()
        auth = (username, password)

        self.jira = GreenHopper(options, basic_auth=auth)
        self.board_name = arguments.board

        self.format = arguments.format
        self.layout = arguments.layout
        self.style = arguments.style

    def generate(self):
        sprint_finder = IssueFinder(self.jira)

        if self.board_name:
            board_name = arguments.board
        else:
            print('Found boards:')
            for board in sprint_finder.get_board_names():
                print('  ' + str(board))
            board_name = raw_input('Select board: ')

        issues = sprint_finder.get_open_sprint(board_name)
        formatter = IssueFormatter(self.format)

        formatted_issues = []
        for issue in issues:
            formatted_issues.append(formatter.format(issue))
        cards.render(self.layout, self.style, formatted_issues)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate cards for open JIRA sprint')
    parser.add_argument('server', help='jira server to connect to')
    parser.add_argument('-u', '--username', help='username to authenticate as', default=None)
    parser.add_argument('-b', '--board', help='board name', default=None)
    parser.add_argument('-f', '--format', help='format template file', default='format/basic.html')
    parser.add_argument('-l', '--layout', help='layout template file', default='layout/basic.html')
    parser.add_argument('-s', '--style', help='stylesheet file', default='style/square-post-it.css')

    arguments = parser.parse_args()
    generator = Generator(arguments)
    generator.generate()