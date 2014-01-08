from string import Formatter
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
        formatter = CardFormatter.MissingFieldFormatter()
        issue.raw.pop('self', None)
        flat_issue = self.flatten(issue.raw)
        formatted = ''

        with open(self.format_name, 'r') as format_file:
            for line in format_file:
                formatted_line = formatter.format(line, **flat_issue)
                formatted += formatted_line
        return formatted

    def flatten(self, dictionary):
        def items():
            for key, value in dictionary.items():
                if isinstance(value, dict):
                    for subkey, subvalue in self.flatten(value).items():
                        yield key + "/" + subkey, subvalue
                else:
                    yield key, value

        return dict(items())

    class MissingFieldFormatter(Formatter):

        def get_field(self, field_name, args, kwargs):
            try:
                return super(CardFormatter.MissingFieldFormatter, self).get_field(field_name, args, kwargs)
            except:
                return None, None

        def get_value(self, key, args, kwargs):
            try:
                value = super(CardFormatter.MissingFieldFormatter, self).get_value(key, args, kwargs)
                if value is None or value == 'None':
                    value = ''
                return value
            except:
                return ''




