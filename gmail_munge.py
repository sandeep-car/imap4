#!/usr/local/bin/python
# Copyright Sandeep Cariapa (cariapa@gmail.com)
# This script logs into an IMAP account and munges messages matching a particular pattern.
# At the current time it is known to wotk with gmail, it may work with other IMAP servers (Outlook) also, with some modifications.
# Assumes that you either have marked your gmail account with less secure app access (not recommended)
# or that you have 2-step verification turned on and use an app password instead (recommended).
# More easy reading. Probably need to read the RFC also.
# https://medium.com/@yernagulahemanth/download-emails-from-gmail-using-python-31e9bc62e501
# https://coderwall.com/p/gorteg/python-s-imaplib

import imaplib,email
import datetime,os,re,time,sys
from pprint import pprint

imap_url = "imap.gmail.com"
# These are the credentials of the email account where your bounced emails land up.
user = "email@gmail.com"
password = "blahdeblahblah"
delete_maadi = False
# https://www.geeksforgeeks.org/check-if-email-address-valid-or-not-in-python/
email_regexp = r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}'

if ((len(sys.argv) != 3) and (len(sys.argv) != 4)):
  print ("<Usage>:",sys.argv[0],"<user> <number of days> delete")
  print ("Where <user> is the who you want to look for: e.g. 'MAILER-DAEMON' or 'complaints'.")
  print ("<number of days> is how far you want to go back, typically 1, maybe 2.")
  print ("delete is an optional argument which finds all messages with the preceding criteria and zaps them.")
  sys.exit(1)

if (len(sys.argv) == 4):
  if (sys.argv[3] == "delete"):
    delete_maadi = True
  else:
    print ("Your arg needs to be delete.")
    sys.exit(1)

# buser is the username of the bounced user :)
buser = sys.argv[1]
numdays = int(sys.argv[2])

conn = imaplib.IMAP4_SSL(imap_url)
try:
  conn.login(user,password)
  print ("Login Success!")
except Exception as ex:
  print("Login Failed!", ex)
  sys.exit(1)

# This block should list out your IMAP4 mailboxes (aka labels in gmail)
# Uncomment if you need to test this out.
#resp, data = conn.list()
#print ("Response code: ", resp)
#pprint(data)
#sys.exit(0)

# If we're going to delete then readonly must be False.
if (delete_maadi == True):
  conn.select('"INBOX"',readonly=False)
else:
  conn.select('"INBOX"',readonly=True)
# numdays is from the command line. Typically 1.
date = (datetime.date.today() - datetime.timedelta(numdays)).strftime("%d-%b-%Y")

# Search for all messages from sys.argv[1] sent in numdays!
resp, data = conn.search('utf-8', '(SENTSINCE {0})'.format(date), '(FROM {0})'.format(buser.strip()))
# print ("Response code: ", resp)
# pprint(data)

mail_id_list = data[0].split()
for j, i in enumerate(mail_id_list):
  ii = i.decode("utf-8")
  iii = int(ii)
  print ("J: ", j, "I: ", iii)
  if (delete_maadi == False):
    resp, data = conn.fetch(i, "(RFC822)")
    body = data[0][1].decode("utf-8")
#    print(body)
#    print("***************************************")
    # Original recipient's email has to be in there somewhere.
    match_list = re.findall("To: (" + email_regexp + ")", body)
#    print(match_list)
    for email in match_list:
      # Here we are stripping away the email address of the sender which is typically in a bounced message as well.
      if (email.strip() == "email@gmail.com"):
        continue
      print("EMAIL:", email.strip())
  # We are here if we were called to delete messages.
  else:
    # Sleep after zapping 50 messages so you don't overwhelm the IMAP server.
    if (((j % 50) == 0) and (j > 0)):
      print("sleeping for 2 seconds..")
      time.sleep(2)
    # This is gmail specific. If you use another IMAP host you may need to change this. Check Python docs and your IMAP server docs.
    resp, data = conn.store(i, '+X-GM-LABELS', '\\Trash')
    print ("Response code_store: ", resp)
    pprint(data)
    resp, data = conn.expunge()
    print ("Response code_expunge: ", resp)
    pprint(data)

conn.close()
conn.logout()
