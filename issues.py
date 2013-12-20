
class IssueFinder:

    def __init__(self, jira):
        self.jira = jira
        self.boards = {}
        for board in self.jira.boards():
            name = board.raw['name']
            id = board.raw['id']
            self.boards[name] = id

    def get_board_names(self):
        return self.boards.keys()

    def get_open_sprint(self, board_name):
        board_id = self.boards[board_name]

        sprint_id = None
        for sprint in self.jira.sprints(board_id):
            if not sprint.raw['closed']:
                sprint_id = sprint.raw['id']

        return self.jira.search_issues('Sprint = ' + str(sprint_id))


class IssueFormatter:

    def __init__(self, format_name):
        self.format_name = format_name

    def format(self, issue):
        raw = issue.raw
        formatted = ''
        with open(self.format_name, 'r') as format_file:
            for line in format_file:
                formatted += line.format(**raw)
        return formatted