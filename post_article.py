
import os
from os.path import basename, splitext

from write_markdown import write_markdown

def post_article(ftp, article_filename):
  # Upload the article.  Update the current pages list.
  basename_ = splitext(basename(article_filename))[0]
  with open(article_filename) as f:
    ftp.storlines('STOR %s/news/%s' % (root_path, article_filename), f)
  os.remove(article_filename)
  def download_(path):  return download(ftp, path)
  curr_pages = download_('curr_pages.txt')
  old_pages = download_('old_pages.txt')
  curr_pages.insert(0, basename_)
  old_article_base = curr_pages[-1]
  old_article_fname = old_article_base + '.shtml'

  # Update the old pages list.  Download from remote path, return lines.
  old_title = download_('news/%s' % old_article_fname)[0]
  old_title = old_title.split('>', 1)[1].rsplit('<', 1)[0]
  old_pages.insert(0, old_article_base + ' ' + old_title)
  curr_pages = curr_pages[:-1]
  return curr_pages, old_pages

def download(ftp, path):
  path = 'httpdocs/' + path
  print 'downloading: ', path
  def handle_download(block):  f.write(block)
  with open(basename(path), 'wb') as f:
    ftp.retrbinary('RETR ' + path, handle_download)
  with open(basename(path)) as f:  return f.read().strip().splitlines()