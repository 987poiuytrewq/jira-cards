import pdfkit

def render(layout, stylesheet, issues):
    content = '\n'.join(issues)

    html = ''
    with open(layout, 'r') as layout_file:
        for line in layout_file:
            html += line.format(content=content, stylesheet=stylesheet)

    with open('issues.html', 'w') as output:
        output.write(html)

    pdfkit.from_file('issues.html', 'issues.pdf')