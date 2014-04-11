# -*- coding: utf8 -*-
import os
from string import Formatter

class CardRenderer:
    def __init__(self, layout, stylesheet):
        self.layout = layout
        self.stylesheet = os.path.abspath(stylesheet)

    def render(self, issues):
        content = unicode('\n'.join(issues))

        html = unicode('')
        with open(self.layout, 'r') as layout_file:
            for line in layout_file:
                html += unicode(line).format(content=content, stylesheet=self.stylesheet)

        with open('cards.html', 'w') as output:
            output.write(html.encode('ascii', 'xmlcharrefreplace'))


class CardFormatter:
    def __init__(self, format_name):
        self.format_name = format_name

    def format(self, issue):
        formatter = CardFormatter.MissingFieldFormatter()
        issue.raw.pop('self', None)
        flat_issue = self.flatten(issue.raw)
        flat_issue = self.floats_to_ints(flat_issue)
        formatted = ''

        with open(self.format_name, 'r') as format_file:
            for line in format_file:
                formatted_line = formatter.format(line, **flat_issue)
                formatted += formatted_line
        return formatted

    def floats_to_ints(self, flat_issue):
        for key in flat_issue.keys():
            value = flat_issue[key]
            if isinstance(value, float) and value % 1 == 0:
                flat_issue[key] = int(value)
        return flat_issue


    def flatten(self, dictionary):
        def items():
            for key, value in dictionary.items():
                subdict = None
                if isinstance(value, dict):
                    subdict = value
                elif isinstance(value, list):
                    i = 0
                    subdict = {}
                    for list_item in value:
                        subdict[str(i)] = list_item
                        i += 1
                elif hasattr(value, '__dict__'):
                    subdict = value.__dict__

                if subdict:
                    for subkey, subvalue in self.flatten(subdict).items():
                        yield key + '/' + subkey, subvalue
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




