
import logging
from google.appengine.api import mail

############# KANDL #########################

def sendEmail(usersName, usersEmailAddress, usersMessage):
    logging.debug("usersName is %s" %usersName)
    logging.debug("usersEmailAddress is %s" %usersEmailAddress)
    logging.debug("usersMessage is %s" %usersMessage)

    # even though it is user that sends email to us, it has to be from our admin email...
    admin_email = "kirstine78@gmail.com"
    
    message = mail.EmailMessage(sender=admin_email, subject="VISITOR: %s - CONTACTING US" %usersName)

    message.to = "blogkirstine@gmail.com"
    message.body = usersEmailAddress +  " " + usersMessage

    message.send()
