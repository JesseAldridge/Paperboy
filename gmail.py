
import smtplib, urllib2
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

from settings import gmailUser, gmailPassword, server_name

def send_email(article, title):
  # Parms.
  to = ''
  cc = []
  with open('mailing_list.txt') as f:  bcc = f.read().splitlines()

  subject = "New article:  " + title
  url = 'http://www.%s/?page=news/%s' % (server_name, article)
  text = '<p><a href="%url">%url</a></p><p style="font-size:75%;color:#888">(If you no longer wish to recieve these e-mails, please reply with the word "unsubscribe" in the subject line.)</p>'
  text = text.replace('%url', url)

  message = ("From: %s\r\n" % gmailUser
           +"Subject: %s\r\n" % subject
           +"Content-type: text/html\r\n"
           +"\r\n" + text)

  # Send the email.
  print 'connecting...'
  mailServer = smtplib.SMTP('smtp.gmail.com', 587)
  mailServer.ehlo()
  mailServer.starttls()
  mailServer.ehlo()
  print 'logging in...'
  mailServer.login(gmailUser, gmailPassword)
  mailServer.sendmail(gmailUser, [to] + cc + bcc, message)
  mailServer.close()
  print('Sent email to %s' % ([to] + cc + bcc))

def get_unread_msgs():
  # Look for unsubscribes.
  auth_handler = urllib2.HTTPBasicAuthHandler()
  auth_handler.add_password(
      realm='New mail feed',
      uri='https://mail.google.com',
      user=gmailUser,
      passwd=gmailPassword
  )
  opener = urllib2.build_opener(auth_handler)
  urllib2.install_opener(opener)
  feed = urllib2.urlopen('https://mail.google.com/mail/feed/atom')
  return feed.read()

if __name__ == '__main__':
  #send_email(article="University_reformers",
   #          title="University reformers advancing with 'Seven'")
  print get_unread_msgs()