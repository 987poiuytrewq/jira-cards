# -*- coding: utf8 -*-

class BlankFinder:
    def get_issues(self, number):
        issues = []
        for i in range(number):
            issues.append(self.BlankIssue())
        return issues


    class BlankIssue:
        raw = {}


class BoardFinder:
    def __init__(self, jira):
        self.jira = jira
        self.boards = {}
        for board in self.jira.boards():
            name = board.name
            id = board.id
            self.boards[name] = id

    def get_board_names(self):
        return self.boards.keys()

    def get_open_sprint(self, board_name):
        board_id = self.boards[board_name]

        sprint_id = None
        for sprint in self.jira.sprints(board_id):
            if not sprint.closed:
                sprint_id = sprint.id

        if sprint_id is None:
            print('No open sprint for board ' + board_name)
            exit(1)
        return self.jira.search_issues('Sprint = ' + str(sprint_id) + ' AND Sprint not in closedSprints()')


class IssueFinder:
    def __init__(self, jira):
        self.jira = jira

    def get_issues(self, issue_ids):
        issues = []
        for issue_id in issue_ids:
            try:
                issues.append(self.jira.issue(issue_id))
            except:
                print('Issue ' + issue_id + ' not found')
        return issues
