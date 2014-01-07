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
            if arguments.debug:
                for issue in issues:
                    print(str(issue.raw))
                exit(0)
            formatter = CardFormatter(arguments.format)

        formatted_issues = []
        for issue in issues:
            formatted_issues.append(formatter.format(issue))
        renderer = CardRenderer()
        renderer.render(arguments.layout, arguments.style, formatted_issues)

    def get_issues(self, arguments):
        if arguments.mode == 'blank':
            return BlankFinder().get_issues(3)
        else:
            options = {'server': arguments.server}
            
            if arguments.mode == 'board':
                if arguments.noauth:
                    jira = GreenHopper(options)
                else:
                    jira = GreenHopper(options, basic_auth=self.get_auth(arguments))
                
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
                if arguments.noauth:
                    jira = JIRA(options)
                else:
                    jira = JIRA(options, basic_auth=self.get_auth(arguments))
                issue_finder = IssueFinder(jira)
                return issue_finder.get_issues(arguments.issues)

    def get_auth(self, arguments):
        if arguments.username:
            username = arguments.username
        else:
            username = raw_input('Username: ')
        if arguments.password:
            password = arguments.password
        else:
            password = getpass.getpass()
        return (username, password)

