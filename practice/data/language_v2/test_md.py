import markdownify
html = '<table><tr><td><img src="foo.png"></td></tr></table>'
print(markdownify.markdownify(html, keep=['table', 'tr', 'td', 'thead', 'tbody']))
