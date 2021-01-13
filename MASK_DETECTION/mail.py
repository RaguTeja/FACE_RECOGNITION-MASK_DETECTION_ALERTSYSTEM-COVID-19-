import smtplib


class MailAlert:
    def mailAlert(self,SUBJECT,TEXT):

        message='Subject: {} \n\n{}'.format(SUBJECT,TEXT)

        mail=smtplib.SMTP('smtp.gmail.com',587)                    # defining smtp mail server

        # to get identified by server
        mail.ehlo()

        # activating transport layer security to encrypt any kind of data
        mail.starttls()

        # login credentials
        mail.login('abhi123manue456@gmail.com','R@ju1234')
        mail.sendmail('abhi123manue456@gmail.com','abhi123manue456@gmail.com',message)
        mail.close()


