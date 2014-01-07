import pdfkit

class CardRenderer:

    def render(self, layout, stylesheet, issues):
        content = '\n'.join(issues)

        html = ''
        with open(layout, 'r') as layout_file:
            for line in layout_file:
                html += line.format(content=content, stylesheet=stylesheet)

        with open('issues.html', 'w') as output:
            output.write(html)

        pdfkit.from_file('issues.html', 'issues.pdf')

class CardFormatter:

    def __init__(self, format_name):
        self.format_name = format_name

    def format(self, issue):
        raw = issue.raw
        formatted = ''
        with open(self.format_name, 'r') as format_file:
            for line in format_file:
                formatted += line.format(**raw)
        return formatted