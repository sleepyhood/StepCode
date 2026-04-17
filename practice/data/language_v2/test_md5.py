import markdownify
html = '<table><tr><td>a</td><td><img src="foo.png"></td></tr></table>'
print("OUTPUT:")
print(markdownify.markdownify(html, keep=['table', 'tr', 'td', 'thead', 'tbody'], keep_inline_images_in=['td', 'th']))
