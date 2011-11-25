import time
import markdown

def write_markdown(text):
  text = text.strip()
  print 'writing markdown: ', text.encode('utf8')
  line = text.splitlines()[0]
  basename_ = u'_'.join(line.split(' ', 2)[:2]).encode('ascii', 'ignore')
  article_filename = basename_ + '_' + str(int(time.time())) + '.shtml'
  with open(article_filename, 'w') as f:
    f.write(markdown.markdown(text).encode('utf8'))
  return article_filename

if __name__ == '__main__':
  print write_markdown(
'''Senate Budget Committee
======
On a foo bar...
''')