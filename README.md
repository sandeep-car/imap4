# imap4
Code to deal with IMAP4 messages.

gmail_munge.py logs into your gmail account and does some things :-) I used Python 3.9.5.

It takes two required arguments and one optional. The two required arguments are: \<buser\> and \<numdays\>
 
\<buser\> is the username of whoever you want to search for in your mailbox. MAILER_DAEMON for example would search for bounced email messages.
  
\<numdays\> is a parameter which describes the number of days you want the script to go back for. If \<numdays\> is 1, then it searches for all messages that match \<buser\> for the last 24 hours. If 2, then 48.
  
The third optional argument is "delete". If you pass in this parameter then the script will find all messages from \<buser\> for the last \<numdays\> days, 
and move them to trash. Use this with care. 
  
If you run this with the two required options, gmail.munge.py will log into your gmail account, search for messages from <buser> over \<numdays\> and spew out 
email addresses of the original recipients.
You can then take that list of recipients and remove them from your mailing list. 
  
After you're done removing the email addresses you can run gmail_munge.py with the optional delete parameter which will erase those messages from your gmail account. 

Room for improvement:
  
1. By default the script only looks in the INBOX mailbox. If you want it to search in other mailboxes, you'll need to modify the script. This could be another parameter.
  
2. You could modify the code where instead of searching (re.findall) for an email it could search for a particular pattern. This would make it similar to running 
a search from the gmail searchbar. Only advantage being that you could script other stuff with the output.

If you think this sounds interesting and want to play with it, drop me a note.
