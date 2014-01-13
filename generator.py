import getpass
from jira.client import JIRA, GreenHopper

from issues import BlankFinder, BoardFinder, IssueFinder
from cards import CardFormatter, CardRenderer


class Generator:
    def __init__(self, arguments):
        issues = self.get_issues(arguments)

        if arguments.mode == 'blank':
            formatter = CardFormatter('format/blank.html')
        else:
            formatter = CardFormatter(arguments.format)
            if arguments.debug:
                for issue in issues:
                    flat_issue = formatter.flatten(issue.raw)

                    print('\n' + flat_issue['key'] + ':')
                    for item in sorted(flat_issue.items()):
                        print('  ' + str(item[0]) + ': ' + str(item[1]))

        formatted_issues = []
        for issue in issues:
            formatted_issues.append(formatter.format(issue))
        renderer = CardRenderer(arguments.layout, arguments.style)
        renderer.render(formatted_issues)
        print('Generated cards.html')

    def get_issues(self, arguments):
        if arguments.mode == 'blank':
            return BlankFinder().get_issues(arguments.number)
        else:
            if arguments.mode == 'board':
                jira = self.connect(GreenHopper, arguments)

                board_finder = BoardFinder(jira)
                if arguments.board:
                    board_name = arguments.board
                else:
                    print('Found boards:')
                    for board in board_finder.get_board_names():
                        print('  ' + str(board))
                    board_name = raw_input('Select board: ')

                return board_finder.get_open_sprint(board_name)

            if arguments.mode == 'issues':
                jira = self.connect(JIRA, arguments)

                issue_finder = IssueFinder(jira)
                return issue_finder.get_issues(arguments.issues)

    def connect(self, constructor, arguments):
        options = {'server': arguments.server}

        try:
            if arguments.anonymous:
                return constructor(options)
            else:
                auth = self.get_auth(arguments.username, arguments.password)
                return constructor(options, basic_auth=auth)
        except Exception as e:
            print('Could not connect to jira instance at ' + arguments.server)
            print(str(e))
            exit(1)

    def get_auth(self, username, password):
        if not username:
            username = raw_input('Username: ')
        if not password:
            password = getpass.getpass()
        return username, password

