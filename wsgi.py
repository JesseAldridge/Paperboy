
import ftplib, os

import web

from post_article import post_article, download
from gmail import send_email, get_unread_msgs
from write_markdown import write_markdown
from settings import server_name, ftp_username, ftp_password, root_path

# Get index.  Connect to ftp on post.
urls = ('/(.*)', 'Handler')
class Handler(object):
  def GET(self, after_slash):  return render.index()
  def POST(self, after_slash):
    input = web.input()
    ftp = ftplib.FTP(server_name)
    ftp.login(ftp_username, ftp_password)
    def download_(path):  return download(ftp, path)

    # Handle various requests.
    articles_path = '%s/news' % root_path
    if after_slash == 'articles':
      dir_lines = []
      ftp.cwd(articles_path)
      return '\n'.join(ftp.nlst())
    elif after_slash == 'mailing_list':
      return '\n'.join(download_('mailing_list.txt'))
    elif after_slash == 'download':
      return '\n'.join(download_('news/%s' % input['filename']))
    elif after_slash == 'inbox':
      return get_unread_msgs()
    elif after_slash == 'post_edit':
      article_filename = input['filename']
      with open(article_filename) as f:
        ftp.storlines('STOR %s/%s' % (articles_path, article_filename), f)
      os.remove(article_filename)

    elif after_slash == 'post_new':
      # Post article.  Upload new page files.  Cleanup.
      text = input['text']
      article_filename = write_markdown(text)
      curr_pages, old_pages = post_article(ftp, article_filename)
      for s in 'old_pages', 'curr_pages':
        filename = s + '.txt'
        l = eval(s)
        with open(filename, 'w') as f:  f.write('\n'.join(l))
        with open(filename) as f:
          ftp.storlines('STOR %s/%s' % (root_path, filename), f)
        os.remove(filename)
      article = curr_pages[0]
      title = text.split('===')[0].strip()
      send_email(article, title)

# Launch.
app = web.application(urls, globals())
render = web.template.render('templates/')
if __name__ == '__main__':
  app.run()
else:
  web.config.debug = False
  application = app.wsgifunc()