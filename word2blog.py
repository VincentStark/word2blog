#!/usr/bin/env python

import codecs
import cgi
from jinja2 import Environment, PackageLoader
from bs4 import BeautifulSoup

# Prepare template
env = Environment(loader=PackageLoader('__main__', 'templates'))
template = env.get_template('blog.xml')

# Process input file
doc = BeautifulSoup(open('input/input.html'))

# Prepare array for data storage
entries = []

# Process every 'h1' tag
for section in doc.find_all('h1'):

  # Get published date from headers
  (day, month, year) = section.find_all(text=True)[0].split('.')
  published = year + '-' + month + '-' + day

  # Get content
  content = u""
  for p in section.find_next_siblings():

    # Find data between two 'h1' tags
    if p.name == 'h1':
      break
    
    # Clean unneeded tags
    if p.span:
      p.span.unwrap()
    del p['class']

    content += unicode(p).replace("\r\n", u' ')
    content += '<br/>'

  entries.append({ 'published': published, 'content': cgi.escape(content)})

# Output
output = open('output.xml', 'w')
output.write(template.render(entries = entries).encode('utf-8'))
output.close()
